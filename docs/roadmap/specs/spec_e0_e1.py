S = {}
def s(i, summary, req, acc, tests=(), deps=(), notes=""):
    S[i] = dict(summary=summary, requirements=list(req), acceptance=list(acc), tests=list(tests), depends_on=list(deps), notes=notes)

# ---------------- E0 ----------------
s("E0","Establish the repository, build, CI and contribution conventions that every later epic relies on.",
  ["Reproducible .NET 10 solution with pinned SDK and shared build settings.","CI that builds, tests and format-checks every pull request.","Documented test-first workflow, ADRs and issue/PR templates."],
  ["`dotnet build` and `dotnet test` pass from a clean clone.","Every PR runs CI; `main` is protected and squash-merge only.","Architectural decisions are recorded as ADRs."])
s("F01","Solution and project layout for the modular monolith with out-of-process plugins.",
  ["Projects: Gbit.Core, Gbit.Protocol, Gbit.Storage.Sqlite, Gbit.Cli, test projects.","Shared `Directory.Build.props`, `global.json`, `.editorconfig`, `.gitignore`.","Placeholder folders for plugins and CI wrappers."],
  ["Clean clone builds with zero warnings (warnings are errors).","Project references follow the dependency rule: Core depends only on Protocol."],
  notes="Delivered in the initial scaffold commit (T001-T003 are Done).")
s("F02","Continuous integration with coverage and dependency updates.",
  ["Workflow builds and tests on Linux and Windows.","Coverage collected and gated.","Automated dependency update PRs."],
  ["A failing test, format error or build error turns the PR red.","Coverage threshold is enforced once tests exist."])
s("F03","Contributor-facing conventions that make test-first, language-neutral development the default.",
  ["CONTRIBUTING.md describing the workflow.","ADR template plus records of the locked decisions.","Issue and PR templates."],
  ["A new contributor can find how to build, test and propose a change in under five minutes.","The seven decisions from proposal section 12 each have an ADR."])
s("T004","Run build, test and format checks on every pull request.",
  ["Workflow on `pull_request` and push to `main`.","Matrix: ubuntu-latest and windows-latest.","`dotnet format --verify-no-changes` job.","Test results and coverage uploaded as artifacts."],
  ["All jobs pass on a clean PR.","Introducing a formatting violation fails the format job."],
  ["Open a PR with a deliberate format error and confirm it is red."],
  notes="Delivered in PR #116. Remaining work: mark the three jobs as required status checks in branch protection, then close this issue.")
s("T005","Report code coverage and fail the build below a threshold.",
  ["Collect coverage with the existing coverlet collector.","Publish a summary on each PR.","Set an initial line-coverage threshold, raised as the kernel grows."],
  ["Coverage appears on every PR.","A PR that drops coverage below the threshold fails CI.","The threshold is documented and is never lowered to make a check pass."],
  ["Temporarily add untested code and confirm the gate trips."],["T004"])
s("T006","Keep NuGet and GitHub Actions dependencies current.",
  ["Dependabot config for nuget and github-actions ecosystems, weekly.","Group minor and patch updates.","Labels `dependencies`."],
  ["Dependabot opens PRs that pass CI.","Action versions are updated."],deps=["T004"])
s("T007","Document the contribution workflow with emphasis on test-first development.",
  ["CONTRIBUTING.md covers build, test, branch and PR flow.","States the principles: test first, language-neutral kernel, correctness before optimization.","Describes how to claim a roadmap issue."],
  ["File exists at repository root and is linked from the README.","Instructions work on a fresh machine."],
  notes="A first version exists on `main`. Remaining work: add the conformance-scenario authoring guide once T010 lands, then close.")
s("T008","Record the locked architectural decisions as ADRs.",
  ["`docs/adr/0000-template.md` (context, decision, consequences, status).","One ADR per decision in proposal section 12 (seven total).","Index in `docs/adr/README.md`."],
  ["Each ADR cites the proposal section and the acceptance criteria it supports.","ADRs are numbered and immutable once accepted; changes supersede."])
s("T009","Standardize how work is reported and reviewed.",
  ["Issue forms: bug report, roadmap task, plugin proposal.","Pull request template with test-plan checklist and roadmap ID field.","Config disabling blank issues except security contact."],
  ["Templates appear in the GitHub UI.","The PR template links the roadmap ID and mentions the test-first rule."])

# ---------------- E1 ----------------
s("E1","Build the language-neutral graph kernel and the conformance suite that defines its behavior, tests first. This is the core of GBIT: every later epic plugs into it.",
  ["Typed, versioned property graph with provenance.","Base/head-aware reverse-dependency impact analysis.","Safety policy: uncertainty widens selection.","Deterministic, explainable execution plan."],
  ["All 12 conformance scenarios from proposal section 1.3 pass.","The monotonicity property holds: adding a possible edge never shrinks the selection.","Identical inputs produce byte-identical plans.","The kernel contains no language- or framework-specific code."],
  notes="Exit criterion from the proposal: all language-neutral selection, versioning, deletion, uncertainty and determinism scenarios pass.")
s("F04","The executable architecture specification: fixtures and scenarios written before the implementation.",
  ["A declarative fixture format for graphs, changes and expected impact sets.","One scenario per row of proposal table 1.3.","Property-based and determinism tests."],
  ["Scenarios run against the planner via a single entry point.","Failing scenarios identify the violated requirement (AC-xx)."])
s("T010","Define the fixture format used by every conformance test.",
  ["Versioned file format (`gbit.fixture/v1`, JSON or YAML) describing base graph, head graph, change set, test inventory, policy and expected outcome.","Expected outcome lists selected tests, excluded tests, fallback tests and completeness status.","Loader and validator in `tests/Gbit.Conformance`.","Fixtures live under `tests/Gbit.Conformance/Fixtures`."],
  ["Malformed fixtures fail with a clear message naming the file and field.","A sample fixture round-trips through load and serialize unchanged.","The format can express every scenario in section 1.3, including deleted and renamed entities."],
  ["Loader unit tests for valid and invalid fixtures."],["T014"])
s("T011","Encode the 12 scenarios of proposal section 1.3 as failing tests.",
  ["One fixture and one test per scenario: isolated method, shared utility, interface change, comment-only edit, rename, deletion, new test, dependency version change, OpenAPI change, test-config change, analyzer unavailable, unknown dynamic relationship.","Tests call the planner API and assert on selected, fallback and excluded sets.","Tests are initially red and tracked by trait `Conformance`."],
  ["Exactly 12 scenario tests exist and each references its AC ids.","Each is red until the corresponding implementation task lands, then green.","No scenario is skipped or deleted to make CI pass."],
  notes="CI should treat not-yet-implemented scenarios as expected failures until E1 completes; do this with an explicit allow-list, not by skipping.",deps=["T010"])
s("T012","Prove the safety invariant with a property-based test.",
  ["Generate random graphs, change sets and edge additions.","Property: adding a possible dependency edge, all else equal, yields a superset of the previous selection.","Use FsCheck or CsCheck with a fixed seed in CI and a random seed nightly."],
  ["The property passes for at least 10,000 generated cases.","Failing cases are shrunk and printed as fixtures."],
  ["The property test itself, plus a deliberately broken planner to prove it can fail."],["T010","T021"])
s("T013","Guarantee deterministic plans.",
  ["Run the planner repeatedly and with shuffled input order on the same logical input.","Plans must be byte-identical when serialized.","Define a canonical ordering for tests, edges and paths."],
  ["100% of runs produce identical plan bytes (AC-13).","Shuffled entity, edge and test input order does not alter output."],
  ["Determinism test over all conformance fixtures."],["T010","T028"])
s("F05","The graph's vocabulary: entities, relationship types and edge metadata.",
  ["Canonical entity ID scheme.","Edge type catalog with traversal semantics.","Edge properties for provenance and confidence."],
  ["The model can represent source, verification, contract and environment entities.","Direction convention is documented and enforced."])
s("T014","Define stable, language-neutral entity identities.",
  ["Proposed ID shape: `<kind>:<scope>/<path-or-name>` (for example `symbol:Pricing/PricingService.Calculate(decimal)`).","Entity kinds: repository, project, file, symbol, test, contract, resource, package, config, flag.","IDs are stable across revisions unless the entity is renamed or moved.","Plugins mint IDs; the kernel treats them as opaque but validates syntax and uniqueness."],
  ["IDs round-trip through parse and format.","Same entity at base and head resolves to the same ID.","Collisions between plugins are rejected."],
  ["Unit tests for parsing, equality and ordering."],notes="Record the final ID grammar in an ADR.")
s("T015","Fix the dependency edge catalog and direction convention.",
  ["Edge types: CALLS, REFERENCES, IMPLEMENTS, IMPORTS, READS, WRITES, DEPENDS_ON, CONSUMES_CONTRACT, EXECUTES, VALIDATES.","Dependency edges point Consumer -> Dependency.","Each edge type declares whether it propagates impact in reverse, and whether it is a dependency or a verification observation.","Verification edges (EXECUTES, VALIDATES) are not interchangeable with dependency edges."],
  ["Constructing a dependency edge with reversed semantics is a compile-time or validation error.","The catalog is table-driven so new types require no traversal code changes."],
  ["Tests asserting traversal semantics for each type."],["T014"])
s("T016","Attach provenance and uncertainty metadata to every edge.",
  ["Properties: source/target IDs, type, evidence source (static, runtime, build, contract), analyzer ID and version, revision, confidence/completeness, validity scope.","Confidence distinguishes definite, possible and incompletely observed.","Validity scope covers build target, platform, runtime, configuration and environment."],
  ["An edge without analyzer id/version or revision is rejected.","Scope mismatch makes an edge not applicable rather than silently applicable."],
  ["Validation tests; serialization snapshot test."],["T015"])
s("F06","Versioned snapshots, change modeling and incremental invalidation.",
  ["Immutable base and head snapshots.","Change classification.","Hash-driven reanalysis."],
  ["Impact analysis can read both snapshots (AC-04).","Only changed artifacts and necessary dependents are reanalyzed (AC-08)."])
s("T017","Hold immutable base and head graphs in memory.",
  ["`GraphSnapshot` with entity table, outgoing and incoming adjacency indexes, snapshot ID and revision.","Immutable after build; builder API for plugin output ingestion.","Merged read-only view for traversals across base and head."],
  ["Lookups by ID and neighbors by edge type are O(1) amortized.","Mutating a snapshot after build is impossible."],
  ["Unit tests for build, lookup and merged view."],["T014","T016"])
s("T018","Represent and detect how artifacts changed between revisions.",
  ["Change kinds: added, modified, deleted, moved, renamed.","Rename and move carry old and new IDs.","Unresolved renames are reported as delete plus add with an uncertainty flag.","Behavioral vs non-behavioral classification supplied by analyzers (for comment-only edits)."],
  ["A ChangeSet can be built from fixtures and from git (via T044).","Renames resolved reliably preserve identity; ambiguous ones expand selection."],
  ["Unit tests for each change kind and for ambiguous rename."],["T014"])
s("T019","Reanalyze only what changed.",
  ["Content-hash per file and per analysis unit.","Invalidation key includes compiler settings, plugin version, configuration and revision.","Invalidate dependents of changed units only when their inputs changed."],
  ["Changing one file reanalyzes that file and necessary dependents only.","Changing a plugin version invalidates all of its evidence."],
  ["Invalidation tests with synthetic graphs; counts of reanalyzed units asserted."],["T017","T018"])
s("F07","Reverse-dependency traversal and selection across base and head.",
  ["Type-aware traversal.","Selection formula.","Deleted and new entity handling."],
  ["Transitive consumers are found (AC-05).","Deleted functions' former consumers are found from the baseline."])
s("T020","Walk consumers of a changed entity using both snapshots.",
  ["Traverse reversed dependency edges from changed entities.","Use the union of base and head edges relevant to each changed entity.","Honor edge-type propagation rules and validity scope.","Record the path for each reached entity."],
  ["Shared-utility scenario selects all transitive consumers.","Cycles terminate.","Traversal is deterministic."],
  ["Scenario and cycle tests; benchmark on a 100k-node graph."],["T015","T017"])
s("T021","Compute the set of tests to run.",
  ["T_run = T_changed U T_related U T_fallback.","T_changed: tests whose own definition changed. T_related: tests reached through dependency or verification evidence. T_fallback: tests added by safety policy.","Output records which rule selected each test."],
  ["Selection is a superset of each component.","New tests are always in T_changed."],
  ["Unit tests per component; run the monotonicity property (T012)."],["T020","T025"])
s("T022","Use baseline relationships so deletions do not hide consumers.",
  ["For deleted entities, seed traversal from the entity in the base snapshot.","Consumers found only in base are selected with reason `deleted-dependency`."],
  ["Function-deleted scenario selects former consumers.","Analyzing the head graph alone would fail this test."],
  ["Conformance scenario 6."],["T020"])
s("T023","Always run new tests even without coverage history.",
  ["Tests absent from base inventory are classified as new and selected.","Selection reason is `new-test`."],
  ["New-test scenario passes.","A new test with no edges is still selected."],
  ["Conformance scenario 7."],["T021"])
s("F08","The safety layer that turns uncertainty into wider selection.",
  ["Completeness model.","Boundary fallback.","Operating modes.","Plugin failure handling."],
  ["Unknown relationships never shrink the selection (AC-10).","An empty selection is never reported as an automatic pass."])
s("T024","Track how completely each entity and edge was observed.",
  ["Completeness levels: complete, partial, unknown.","Analyzers report completeness per entity and per edge.","Aggregate graph completeness exposed in the plan."],
  ["Partial or unknown completeness on a reached entity triggers fallback.","Plan reports `Graph completeness`."],
  ["Unit tests over mixed-completeness graphs."],["T016"])
s("T025","Widen selection to a safe boundary when impact cannot be bounded.",
  ["Boundary hierarchy: test suite, project, repository.","Policy chooses the smallest boundary containing the uncertainty.","Fallback tests carry the triggering evidence."],
  ["Dynamic-relationship-unknown scenario selects the suite boundary.","Fallback is reported in the plan with its reason."],
  ["Conformance scenarios 11 and 12."],["T024"])
s("T026","Implement shadow, conservative and optimized modes.",
  ["Shadow: compute plan, run everything, compare.","Conservative: impacted plus widened scopes.","Optimized: precise selection only on validated evidence.","Mode resolved from config, overridable by CLI flag."],
  ["The same input differs between modes only in the documented ways.","Optimized refuses to run when evidence validation is absent."],
  ["Per-mode tests on the same fixture."],["T025"])
s("T027","Never turn plugin failure into silent success.",
  ["A required plugin that fails, times out or is missing causes widening or an explicit failure.","The plan states which plugin failed and the resulting fallback.","Exit code distinguishes `success`, `widened` and `failed`."],
  ["Analyzer-unavailable scenario passes.","No path exists where a failed required plugin yields an empty dependency set."],
  ["Conformance scenario 10; fault-injection tests."],["T025"])
s("F09","Plans that explain themselves.",
  ["Plan schema.","Causal paths and provenance.","Exclusion explanations.","Requested vs runnable granularity."],
  ["100% of selections and fallbacks have explanations (AC-09)."])
s("T028","Specify and implement the execution plan model.",
  ["Fields: base/head revisions, snapshot IDs, policy, analyzer versions, completeness, selected tests with runner selectors, fallback boundaries, excluded tests, causal paths, predicted vs actual counts and durations.","Versioned JSON schema (`gbit.plan/v1`).","Canonical serialization."],
  ["Schema validates every plan produced by conformance tests.","Serialization is canonical (supports T013)."],
  ["Schema validation and snapshot tests."],["T021"])
s("T029","Record why each test was selected.",
  ["Store path from changed entity to test, with edge types and provenance references.","Keep the shortest path and a count of alternatives.","Support `gbit explain test:<id>`."],
  ["Every selected test has at least one path or fallback reason.","Paths reference real edges and analyzer versions."],
  ["Property: every selected test is explained."],["T020","T028"])
s("T030","Explain exclusions without overclaiming.",
  ["For an excluded test, state the analysis bounds: which analyzers ran, completeness, and that no edge was found.","Never phrase absence of an edge as proof of independence.","Include the nearest reached entity when helpful."],
  ["Every excluded test has a bounded explanation.","Wording is covered by golden-file tests."],
  ["Golden tests for exclusion text."],["T029"])
s("T031","Separate what the graph asks for from what the runner can run.",
  ["Plan lists requested test cases and actual runnable units.","Runner reports selector granularity (case, class, file).","Mismatch is recorded as over-selection."],
  ["Parameterized test with class-only selector shows requested vs runnable difference.","Counts in the plan add up."],
  ["Tests with a fake runner of each granularity."],["T028"])
s("F10","User-facing configuration.",
  ["`gbit.yml` schema.","Loading and policy resolution."],
  ["Invalid config is rejected with actionable errors.","Defaults work for a conventional repository."])
s("T032","Define the `gbit.yml` schema and validate it.",
  ["Top-level: apiVersion, policy (mode, fallback boundaries), plugins (id, version, required), include/exclude globs, runner settings.","Publish a JSON Schema for editor support.","Unknown keys are errors."],
  ["Sample config in the repo validates.","Errors include line, key and fix suggestion."],
  ["Valid and invalid config tests."])
s("T033","Load configuration and resolve effective policy.",
  ["Layering: defaults, `gbit.yml`, environment, CLI flags.","Effective policy printed by `gbit plan --show-policy`.","Plugin requirement flags feed T027."],
  ["Precedence is documented and tested.","Same inputs resolve to the same policy."],
  ["Precedence matrix tests."],["T032"])
