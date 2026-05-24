# Prototype Integration Mapping

## Status

Planning artifact. Map of how to use the external `table-map-editor-canvas-local-fixed` prototype.

## Purpose

Зафиксировать, как внешний прототип использовать в основном проекте без
подмены архитектуры:

- что от него можно брать;
- что нельзя брать;
- что брать только как UX reference;
- что брать как isolated utility;
- что лучше не брать совсем.

## Classification

Treat the prototype as:

- reference prototype;
- selective donor for future Map Editor surface;
- not a direct product-code foundation;
- not a substitute for canonical architecture.

It is useful. It is not the base of the whole product.

## Reusable Parts

### Exact reuse

Possible only after local review:

- Vite bootstrap shape;
- static demo setup;
- GitHub Pages base-path idea;
- some utility helpers;
- some localStorage draft persistence patterns.

### Adapted reuse

Strong candidates to adapt, not copy blindly:

- left object list + right inspector layout;
- canvas selection/edit interaction;
- map layer / object manipulation UX;
- validation affordances;
- export affordances;
- zoom/pan and snap behavior ideas.

### Concept-only reuse

Use only as ideas, not code:

- spaces;
- connections;
- zones;
- layers;
- inspector structure;
- map-editor feedback loop.

## Dangerous Carryovers

Do not carry these into the main repo blindly:

- single large `App.jsx` as product architecture;
- prototype state as source of truth;
- prototype-local save format as canonical format;
- any structure that overrides `GameState`;
- any structure that bypasses `Action/Event`;
- any structure that bypasses `RulesHooks`;
- any structure that blurs authoring and runtime.

## Best Integration Strategy

Recommended strategy:

```text
controlled reference + selective extraction
```

Meaning:

- keep prototype as reference;
- extract only the behaviors and ideas that fit canon;
- rewrite implementation inside the main architecture;
- do not promote the whole prototype wholesale.

## Relation To Main Product

The prototype belongs mainly to the future `Map Editor` surface inside the
`Module Authoring Workspace`.

It should not define:

- runtime shell;
- package model;
- canonical file contract;
- `Action/Event` backbone;
- `RulesHooks` boundary;
- product-wide UX model.

## Recommended Pre-Code Action

Before product code starts, create a short integration inventory:

- what to reuse exactly;
- what to reuse after adaptation;
- what to use only as concept;
- what to discard;
- what should be rewritten from scratch.

This inventory should stay small and practical.

## Relation To Other Docs

Read together with:

- `module_authoring_workflow.md`
- `module_product_ux_model.md`
- `table_sandbox_0_1_milestone_plan.md`
- `post_0_1_platform_roadmap.md`

## Final Recommendation

Use the prototype as a reference and selective donor for the Map Editor surface.
Do not let it become the starting architecture of the whole product.

## Role Freeze Before Code

Before the first product-code block starts, the prototype role should be
considered closed:

- reference prototype;
- selective donor;
- not product-code foundation;
- not runtime architecture authority.

This role freeze belongs to the short pre-code closure, so that the first
implementation slice does not drift into prototype-led architecture.

The freeze should be repeated explicitly inside
`../implementation/first_product_code_block.md`, so the first coding brief does
not silently reopen the prototype question.
