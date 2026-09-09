#!/usr/bin/env python3
"""Install and inspect a plugin copy using an isolated Codex home, without model turns."""
from __future__ import annotations

import json
import os
from pathlib import Path
import selectors
import shutil
import subprocess
import tempfile
import time

from skill_manager import Catalog, DEFAULT_ROOT, tree_digest


def verify() -> None:
    catalog = Catalog(DEFAULT_ROOT)
    expected = catalog.selected('mattpocock')
    with tempfile.TemporaryDirectory(prefix='matt-codex-check-') as temporary:
        root = Path(temporary).resolve()
        plugin = root / 'plugins/vendor-mattpocock'
        shutil.copytree(catalog.root / 'plugins/vendor-mattpocock', plugin)
        home = root / 'codex-home'
        home.mkdir()
        market = root / '.agents/plugins/marketplace.json'
        market.parent.mkdir(parents=True)
        market.write_text(json.dumps({'name': 'matt-verification', 'plugins': [{
            'name': 'vendor-mattpocock',
            'source': {'source': 'local', 'path': './plugins/vendor-mattpocock'},
            'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'},
            'category': 'Developer Tools'}]}))
        with (root / 'server.log').open('w') as log:
            process = subprocess.Popen(['codex', 'app-server', '--stdio'], stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=log, text=True,
                env={**os.environ, 'CODEX_HOME': str(home)})
            selector = selectors.DefaultSelector()
            selector.register(process.stdout, selectors.EVENT_READ)

            def rpc(number, method, params):
                process.stdin.write(json.dumps({'id': number, 'method': method, 'params': params}) + '\n')
                process.stdin.flush()
                deadline = time.monotonic() + 40
                while time.monotonic() < deadline:
                    if not selector.select(1):
                        continue
                    line = process.stdout.readline()
                    if not line:
                        raise RuntimeError('Codex server closed before response')
                    response = json.loads(line)
                    if response.get('id') == number:
                        if 'error' in response:
                            raise RuntimeError(f'{method}: {response["error"]}')
                        return response['result']
                raise TimeoutError(method)

            try:
                init = rpc(1, 'initialize', {'clientInfo': {'name': 'matt-verification', 'version': '1.0'},
                    'capabilities': {'experimentalApi': True}})
                params = {'pluginName': 'vendor-mattpocock', 'marketplacePath': str(market)}
                detail = rpc(2, 'plugin/read', params)['plugin']
                expected_names = {'vendor-mattpocock:' + item['name'] for item in expected}
                assert {s['name'] for s in detail['skills']} == expected_names, 'plugin/read selection mismatch'
                rpc(3, 'plugin/install', params)
                data = rpc(4, 'skills/list', {'cwds': [str(root)], 'forceReload': True})['data'][0]
                # User-level skills may be discoverable even with an isolated CODEX_HOME.
                # Inspect only this isolated plugin; never report unrelated local contents.
                loaded = [s for s in data['skills'] if s.get('pluginId') == 'vendor-mattpocock@matt-verification']
                assert {s['name'] for s in loaded} == expected_names, 'installed selection mismatch'
                for skill in loaded:
                    assert skill['enabled'], skill['name']
                    item = next(i for i in expected if 'vendor-mattpocock:' + i['name'] == skill['name'])
                    assert tree_digest(Path(skill['path']).parent) == tree_digest(catalog.root / item['path']), skill['name']
                    assert skill['interface']['displayName'] == item['codex']['displayName'], skill['name']
                relevant_errors = [e for e in data.get('errors', []) if 'vendor-mattpocock' in json.dumps(e)]
                assert not relevant_errors, relevant_errors
                print(json.dumps({'runtime': init['userAgent'], 'discovered': len(detail['skills']),
                    'installedAndEnabled': len(loaded), 'contentParity': True,
                    'pluginErrors': relevant_errors, 'userInstallationModified': False}, indent=2))
            finally:
                selector.close()
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()


if __name__ == '__main__':
    verify()
