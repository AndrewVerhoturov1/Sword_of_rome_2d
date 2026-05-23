# Notebook Entry

- External Question ID: `V1-20260523-124734`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-23_V1-20260523-124734_planning-only-sequencing-answer-for-table-sandbox-0.md`

## Context Links

- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/domain_schemas_contract.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/rules_hooks_interface.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/action_event_contract.md`

## Candidate Navigation Entry

Topic: Planning-only sequencing answer for `Table Sandbox 0.1`
Summary: Recommendation: start with canonical sample files, load module/scenario into `GameState`, build the Action/Event dispatcher and permissive RulesHooks, then prove the first thin vertical slice: moving one piece between two spaces through action → validation → resolution → event commit → reducer → log → render.

## Raw Response

## External Question ID

V1-20260523-124734

## Context Readback

* `external_chat_rules.md` — fully read. ([GitHub][1])
* `repo_navigation.md` — fully read. ([GitHub][2])
* Project `architecture.md` — fully read. ([GitHub][3])
* Project `decisions.md` — fully read. ([GitHub][4])
* `domain_schemas_contract.md` — fully read. ([GitHub][5])
* `rules_hooks_interface.md` — fully read. ([GitHub][6])
* `action_event_contract.md` — fully read. ([GitHub][7])
* Navigation-discovered links from central `repo_navigation.md`: none opened beyond the required `external_chat_rules.md` already provided in the prompt.

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

Central `/v1` rules require honest source separation: claims about the local consumer repo must rely only on explicitly provided project-specific links or excerpts, and the answer must separate central-doc conclusions from project-specific conclusions and not verified material. ([GitHub][1])

Central navigation confirms it is only a guide to central `ai-workflow-core` files and does not grant authority to claim anything about the consumer repo unless project-specific files are passed separately. ([GitHub][2])

For this answer, central docs confirm only the external-chat workflow contract and navigation boundary. They do **not** decide the implementation order for `Table Sandbox 0.1`; that must come from the provided project-specific documents.

### Confirmed from provided excerpts

The project-specific base is already fixed enough to move from architecture planning to milestone sequencing. The accepted direction is: build universal editor/runtime capabilities first, then assemble a Sword of Rome-like test module on top; do not start as a hardcoded single-game implementation. ([GitHub][3])

The accepted product decisions confirm the 4-layer architecture, `RulesHooksInterface`, the split between `Module Content` and `Module Rules/Hooks`, and the requirement that `Table Sandbox 0.1` be planned as universal modules, not as a Sword of Rome-specific runtime. ([GitHub][4])

The domain/data contract fixes the canonical file set and core invariants: `project.json`, `module.json`, `map.json`, `scenario.json`, `rules.metadata.json`, `savegame.json`; definitions vs runtime state; `Action` vs `Event`; `Phaser` is not source of truth; runtime state changes only through action/event pipeline. ([GitHub][5])

The rules hook contract fixes the runtime/module-rules boundary: runtime asks, module rules answer, runtime applies and logs. It also says early `Table Sandbox 0.1` should target `manual` to `assisted`, not strict enforcement. ([GitHub][6])

The action/event contract fixes the runtime backbone: input becomes `Action`, validation produces allow/warn/block, rules resolution returns proposed events, runtime commits events, reducer applies them to `GameState`, event log records them, renderer redraws from committed state. ([GitHub][7])

**Recommended implementation order for `Table Sandbox 0.1`:**

1. **Milestone boundary lock**

   * Define `Table Sandbox 0.1` as: manual tabletop sandbox over canonical data/action/event architecture.
   * Success means: can load a small module, show map/spaces/pieces, move/create/delete pieces, change control, save/load, and see event log.
   * Not success criteria: full Sword of Rome rules, combat, cards, strict legality, online play, AI, polished module content.

2. **Minimal canonical data seed**

   * Create the smallest usable sample module:

     * one `project.json`;
     * one `module.json`;
     * one `map.json`;
     * one `scenario.json`;
     * one `rules.metadata.json`;
     * one empty or generated `savegame.json`.
   * This comes first because all later runtime/editor work needs stable ids, references, definitions, scenario state and save state.
   * Use generic names and fake/test content where possible so the test module does not distort universal layers.

3. **Runtime state bootstrap**

   * Load definitions and scenario state into initial `GameState`.
   * Keep `MapDefinition`, `ScenarioState`, and `SaveGameState` separate.
   * Do not render from raw JSON files directly; runtime should render from `GameState` or derived view state.

4. **Action/Event backbone**

   * Implement the canonical dispatcher conceptually before feature-specific tools:

     * input/request;
     * `Action`;
     * validation;
     * resolution to proposed events;
     * runtime commit;
     * reducer;
     * event log;
     * render refresh.
   * This must exist before drag/drop becomes "real", otherwise drag/drop will create a hidden mutation path outside the accepted architecture.

5. **Default permissive RulesHooks implementation**

   * Add the minimal manual sandbox hooks:

     * `getAllowedActions`;
     * `validateAction`;
     * `resolveAction`;
     * `checkWinCondition`.
   * `getPhaseActions` and `onPhaseStart` can be stubs.
   * In 0.1, rules mostly allow valid-shaped actions and block only broken references or malformed actions.

6. **First thin vertical slice**

   * The first real slice should be:

     * load sample module;
     * load sample scenario;
     * show one map background or simple board surface;
     * show several spaces;
     * show one or more piece instances;
     * drag one piece from one space to another;
     * produce `move_piece_requested`;
     * validate permissively;
     * resolve to `piece_moved`;
     * commit event;
     * update `GameState`;
     * append event log;
     * redraw from `GameState`.
   * This is the best first slice because it exercises every accepted boundary without requiring full editor UI, combat rules, cards, or phase logic.

7. **Manual table actions**

   * Add remaining first-set manual actions from the action/event contract:

     * create piece;
     * delete piece;
     * change control;
     * create space;
     * update space;
     * create connection;
     * save snapshot;
     * load save.
   * Dependency: do this after the first move-piece vertical slice proves the pipeline.

8. **Basic authoring tools over the same pipeline**

   * Add minimal authoring controls for spaces, connections and pieces.
   * These tools should not bypass the action/event backbone.
   * Authoring changes that affect canonical definitions need a clear mode boundary: either definition-editing mode or runtime manual event mode. Do not silently mix them.

9. **Save/load and event log hardening**

   * Save current `GameState` plus event log into `savegame.json`.
   * Load a save back and redraw the same state.
   * Ensure save does not redefine map graph or piece definitions.
   * Dependency: useful only after several event types exist.

10. **Validation and reference integrity pass**

* Add checks for id uniqueness, reference integrity, known action/event types, valid piece locations, and schema versions.
* Keep this as runtime/data safety, not game-rule strictness.

11. **Minimal test module pass**

* Only after universal flow works, add a tiny Sword of Rome-like reference layer:

  * a few named spaces;
  * a few faction/piece definitions;
  * one scenario.
* The test module should be used to validate the platform, not to introduce special cases into universal runtime.

12. **Milestone closeout**

* Freeze 0.1 as "manual playable/editor sandbox".
* Record what is still manual, what is assisted, and what is not implemented.
* Produce the next milestone plan only after 0.1 proves the full loop.

**Dependency order:**

```text
canonical files
→ load module/scenario
→ initial GameState
→ Action/Event dispatcher
→ permissive RulesHooks
→ move-piece vertical slice
→ remaining manual actions
→ save/load
→ validation hardening
→ tiny Sword of Rome-like test module
→ 0.1 closeout
```

**First thin vertical slice:**

The first slice should be **one piece moved between two spaces through the full canonical pipeline**. It is small, but it proves all critical architectural decisions at once: data loading, `GameState`, action/event split, rules boundary, reducer, log, and render-from-state.

**What to consciously defer until after `Table Sandbox 0.1`:**

* full Sword of Rome rules;
* strict legality enforcement;
* combat resolution;
* cards/decks/hands;
* response/interrupt windows;
* hidden information/player-specific views;
* online room sync;
* server-authoritative runtime;
* AI/opponent automation;
* advanced stack model, unless simple derived stacking is insufficient;
* module dependencies;
* migration engine;
* exact save compatibility policy beyond version/hash warning or simple block;
* polished production UI;
* full scenario library.

**Anti-scope-creep rule:**

For 0.1, every feature should answer one question: "Does this strengthen the universal table sandbox loop?" If the answer is "it only makes the Sword of Rome-like module more accurate," defer it. The accepted decisions explicitly warn against letting the test module become the center of the platform. ([GitHub][4])

**Best next planning artifact:**

Create **`table_sandbox_0_1_milestone_plan.md`**.

Recommended contents:

```text
1. Milestone goal
2. Non-goals
3. Required vertical slice
4. Step-by-step implementation order
5. Dependency graph
6. Required first action/event types
7. Required first files and sample data
8. Acceptance checks
9. Deferred features
10. Risks / anti-scope-creep rules
```

After that, the next artifact should be **`first_vertical_slice_spec.md`**, focused only on the move-piece loop.

### Not available / not verified

* I did not inspect the local repository, local branch, runtime, tests, build, or actual product-code state.
* It is not verified whether any product-code skeleton already exists locally.
* Exact frontend stack, folder layout, component structure, test framework, and implementation details are not available in the provided context.
* Stack model remains unresolved in the domain contract.
* Save compatibility policy remains unresolved.
* Response windows remain unresolved.
* Module dependency policy remains unresolved.
* Exact shape of JSON/Zod schemas is not fixed by the provided planning docs.

## Candidate Navigation Entry

V1-20260523-124734: Planning-only sequencing answer for `Table Sandbox 0.1`. Recommendation: start with canonical sample files, load module/scenario into `GameState`, build the Action/Event dispatcher and permissive RulesHooks, then prove the first thin vertical slice: moving one piece between two spaces through action → validation → resolution → event commit → reducer → log → render.

[1]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md "raw.githubusercontent.com"
[2]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md "raw.githubusercontent.com"
[3]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md "raw.githubusercontent.com"
[4]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md "raw.githubusercontent.com"
[5]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/domain_schemas_contract.md "raw.githubusercontent.com"
[6]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/rules_hooks_interface.md "raw.githubusercontent.com"
[7]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/action_event_contract.md "raw.githubusercontent.com"
