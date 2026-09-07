---
name: learn-anything
description: Turn a named topic into a structured, evidence-aware learning guide. Use when the user supplies a subject, tool, concept, system, practice, or question and wants to learn, understand, get an introduction, build a knowledge map, or create a study roadmap. Do not use for requests that only ask to perform the task without teaching it.
---

# Learn Anything

Help the user build a usable mental model of the topic, not merely collect facts.

## Start from the topic

When the user provides only a topic name, begin immediately with a useful first learning card. Do not block on questions about level or goals. Infer likely depth from the conversation, briefly state any important assumption, and invite the user to choose a deeper branch at the end.

Reply in the user's language. Prefer concise notes, concrete examples, small text diagrams, and comparison tables only when they make a relationship clearer.

## Shape the explanation

Adapt the guide to the topic rather than forcing every section into the answer. Usually cover the most useful subset of:

1. **一句话抓住本质** — Define the thing in plain language. Expand abbreviations and distinguish closely related terms before using them.
2. **它解决什么问题** — Explain the need, context, and why it exists.
3. **它怎样运作** — Show the key parts, responsibility boundaries, data or control flow, and one concrete example.
4. **为什么这样设计** — For engineered systems, explain historical pain points, evolution, alternatives, and trade-offs rather than listing only current features.
5. **边界与误区** — State what it is not, when it does not apply, and common misleading simplifications.
6. **如何真正学会** — Give a compact progression from foundational concepts to practice, with one small exercise or observation task when useful.
7. **下一步** — Offer 2–4 meaningful directions the user can choose, not a generic invitation.

Lead with the essence and keep the first answer proportionate. A narrow topic should not become a textbook chapter. If the user asks for "笔记", "路线图", or "简化", compress the result into scan-friendly headings, ordered stages, and learning objectives; omit personal-style justification unless requested.

## Adapt by topic type

- **Technical concept or system:** emphasize vocabulary, component boundaries, execution flow, engineering evolution, and trade-offs.
- **Tool or product:** emphasize what it adds beyond the base system, the highest-value workflows, limitations or account/cost constraints, and a short getting-started path.
- **Broad field:** produce a dependency-aware knowledge map and staged roadmap; explain what each stage enables instead of dumping a resource list.
- **Practical skill or habit:** emphasize goal, observable signals, decisions, a safe first routine, and failure modes.
- **High-stakes topic:** distinguish education from personalized advice and ask for the minimum context needed before giving individualized medical, legal, or financial guidance.

## Evidence and freshness

Browse when facts may have changed, when the topic is niche or uncertain, when recommendations could cost meaningful time or money, or when medical, legal, or financial accuracy matters. For technical and scientific explanations, prefer official documentation, standards, source repositories, or research papers. Put citations beside the claims they support.

Separate established facts from inference. Do not invent exact dates, feature limits, prices, or historical motivations. If a stable conceptual explanation does not need browsing, teach it directly.

## Maintain continuity

Use the user's follow-up questions to deepen the same mental model. Preserve terminology and diagrams that are already working; revise them explicitly when a simplification no longer holds. When the user reveals a preference such as engineering-history framing, note form, or example-first teaching, apply it to later parts of the same learning thread.
