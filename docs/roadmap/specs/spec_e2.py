from spec_e0_e1 import s
s("E2","Prove the kernel is genuinely language-neutral by running two independent ecosystems (C#/.NET with xUnit and Python with pytest) through the identical planner, over a stable plugin protocol.",
  ["`gbit.plugin/v1` JSON-RPC over stdio and a plugin host.","SQLite persistence of snapshots, evidence and plans.","Git change detection and discovery orchestration.","Analyzer and runner plugins for .NET and Python.","Working CLI: init, index, plan, test, explain, graph."],
  ["Both ecosystems use the same core planning engine on real repositories.","Selected tests execute reproducibly through native runners.","Each plugin can be installed and upgraded independently of the core."],
  notes="Exit criterion from the proposal: both ecosystems use the exact same core planning engine on real repositories with reproducible selected test execution.")
s("F11","The versioned contract between the core and every plugin.",
  ["Protocol specification.","Transport implementation.","Plugin host.","Conformance tests any plugin can run."],
  ["A plugin written in any language can implement the protocol (AC-07).","Core and plugins version independently."])
s("T034","Write the normative `gbit.plugin/v1` specification.",
  ["Methods: `initialize`, `getCapabilities`, `analyze`, plus discovery, run and evidence methods reserved by capability.","Message schemas for entities, edges, evidence, completeness, errors and progress.","Capability negotiation and version compatibility rules.","Manifest format (`apiVersion`, `id`, `version`, `capabilities`, `languages`, `methods`).","Published as `docs/protocol/gbit.plugin.v1.md` with JSON Schemas."],
  ["A reader can implement a minimal plugin from the spec alone.","Schemas validate all example messages.","Breaking-change policy is stated."],
  ["Schema validation tests over examples."],["T014","T016"])
s("T035","Implement stdio JSON-RPC transport in Gbit.Protocol.",
  ["Framing (Content-Length headers or newline-delimited; choose and document).","Request/response correlation, notifications, cancellation.","Per-call and global timeouts.","Robust handling of malformed messages, stderr passthrough, large payloads."],
  ["A hung plugin is cancelled and reported at the timeout.","Garbage output yields a protocol error, not a crash.","Throughput benchmark with a 50 MB analyze result."],
  ["Loopback tests with a fake plugin process; fuzz test on framing."],["T034"])
s("T036","Run plugins as managed child processes.",
  ["Discover installed plugins and read manifests.","Pin exact versions and verify checksums.","Start, health-check, restart on crash with backoff, and stop.","Apply CPU, memory and wall-clock limits where the OS allows."],
  ["Plugin crash during analyze produces a failure that feeds the safety policy (T027).","Two plugin versions can be installed side by side; config selects one."],
  ["Lifecycle integration tests using a stub plugin."],["T035"])
s("T037","A reusable conformance kit for plugin authors.",
  ["CLI/test harness `gbit plugin test <executable>` exercising initialize, capabilities, analyze and error paths.","Checks schema validity, determinism, cancellation and completeness reporting.","Published so third-party plugins can self-certify."],
  ["The .NET and Python plugins both pass the kit.","A plugin that omits completeness fails the kit."],
  ["Kit run against a known-good and a deliberately broken stub."],["T034","T035"])
s("F12","Treat plugins as potentially hostile code.",
  ["Filesystem and network restriction.","Secret stripping.","Untrusted PR policy."],
  ["No plugin receives CI secrets unless explicitly required.","Untrusted PRs cannot execute repository-defined plugins with privileges."])
s("T038","Sandbox plugin processes.",
  ["Default read-only access to the workspace, write access to a scratch directory only.","No network unless the manifest requests it and policy allows.","Use OS facilities (bubblewrap/landlock on Linux, job objects/AppContainer on Windows); degrade explicitly and loudly if unavailable."],
  ["A test plugin that writes outside scratch or opens a socket is blocked.","Missing sandbox support is surfaced in the plan's completeness status."],
  ["Escape-attempt plugin tests per OS."],["T036"])
s("T039","Give plugins a clean environment.",
  ["Allow-list environment variables; drop everything else, including `GITHUB_TOKEN`, cloud credentials and `*_SECRET`/`*_KEY` patterns.","Plugins request extra variables in the manifest; user approval recorded in config.","Redact secret-like values from logs."],
  ["A canary secret in the parent environment is not visible to a test plugin.","Allowed variables pass through."],
  ["Canary-secret test."],["T036"])
s("T040","Do not execute attacker-controlled plugins with privileges.",
  ["Plugins declared in the repository are untrusted on fork PRs.","Policy: refuse, run sandboxed without secrets, or use only pre-approved pinned plugins.","Default for fork PRs is pre-approved plugins only.","Document the threat model."],
  ["A fork PR that adds a malicious plugin definition does not execute it.","Behavior is covered by a documented decision table."],
  ["Table-driven policy tests."],["T038","T039"])
s("F13","Durable embedded storage for graphs, evidence and plans.",
  ["Schema.","Migrations and indexes.","Performance baseline."],
  ["Incremental update p95 below 30 s on a 100,000-node graph.","Schema changes are migrated, never lost."])
s("T041","Design the relational schema.",
  ["Tables: Entities, Relationships, GraphSnapshots, TestInventory, CoverageEvidence, ExecutionHistory, SelectionPlans.","Keys and constraints enforce provenance (analyzer, version, revision).","Snapshots share unchanged rows structurally to keep storage small.","Document with an ER diagram in `docs/`."],
  ["Schema can represent every field in T016 and T028.","Review checklist: indexes for reverse adjacency and per-revision reads."],
  ["Schema validation tests."],["T016","T028"])
s("T042","Implement migrations and adjacency indexes.",
  ["Versioned forward-only migrations in `Gbit.Storage.Sqlite/Migrations`.","Covering indexes for incoming/outgoing edges by type and snapshot.","WAL mode, foreign keys on, busy timeout.","Repository API implementing the core's storage interfaces."],
  ["Fresh database and every upgrade path produce the same schema.","Round trip: save snapshot, load, equals original."],
  ["Migration tests; round-trip property test."],["T041"])
s("T043","Benchmark the store at the target scale.",
  ["BenchmarkDotNet suite generating a 100,000-node graph.","Measure full index, incremental update, reverse traversal and plan lookup.","Fail CI on regression beyond a stated tolerance."],
  ["Incremental update p95 under 30 s; planning latency p95 under 2 s (proposal 1.2).","Results are recorded in `docs/benchmarks`."],
  ["The benchmark suite itself."],["T042"])
s("F14","Find what changed and what exists.",
  ["Git revision diff.","Plugin discovery orchestration."],
  ["Added, modified, deleted, moved and renamed artifacts are recognized (AC-04)."])
s("T044","Compute change sets from two git revisions.",
  ["Use libgit2 or `git diff --name-status -M` with rename detection thresholds.","Map files to artifacts via plugin hints.","Handle shallow clones, merge bases and detached HEAD.","Resolve base as merge-base of target branch."],
  ["Rename with edits is reported as rename when similarity passes the threshold.","Behavior on shallow clone is explicit (fetch deeper or widen)."],
  ["Tests against scripted temporary repositories."],["T018"])
s("T045","Coordinate discovery across plugins.",
  ["Ask each plugin which files it owns (via languages and globs).","Run analyzers in parallel with bounded concurrency.","Merge results into snapshots; detect ID conflicts.","Report per-plugin completeness."],
  ["Two plugins on one repo produce one merged snapshot.","A failing plugin follows T027."],
  ["Orchestration tests with stub plugins."],["T036","T044"])
s("F15","First ecosystem: C#/.NET.",
  ["Roslyn or SCIP-based analyzer.","xUnit discovery.","dotnet test filter translation."],
  ["Real .NET repositories index and plan correctly."])
s("T046","Extract symbols and references from C# projects.",
  ["Prefer SCIP (`scip-dotnet`) where it meets precision needs, else Roslyn directly.","Emit symbols, calls, references, implements, project and package dependencies.","Report incomplete analysis (source generators, reflection) as partial completeness.","Plugin id `gbit.analyzer.dotnet`."],
  ["Fixture solutions yield expected edges.","Source-generator and reflection cases are flagged partial."],
  ["Golden tests on sample solutions."],["T034","T037"])
s("T047","Discover xUnit tests with stable IDs.",
  ["Enumerate tests, theories and data rows without executing them where possible.","ID stable across builds and reorderings.","Map tests to defining symbols."],
  ["Renaming a test method changes its ID only in a detectable way.","Theory rows are individual or grouped consistently with T048."],
  ["Discovery tests against sample test projects."],["T046"])
s("T048","Translate plans to `dotnet test` filters.",
  ["Build `--filter` expressions from selected IDs.","Report runnable granularity back to the plan (T031).","Collect TRX/JUnit results, durations and exit status."],
  ["Selected tests, and only those, run.","Over-selection (class-level) is recorded."],
  ["End-to-end run against a sample solution."],["T047","T031"])
s("F16","Second ecosystem: Python.",
  ["Analyzer.","pytest discovery.","Selector translation."],
  ["Same planner, independent ecosystem (AC-01, AC-07)."])
s("T049","Extract symbols and references from Python code.",
  ["Use SCIP (`scip-python`) with Tree-sitter fallback.","Resolve imports, calls and class hierarchies as far as statically possible.","Flag dynamic features (getattr, eval, monkeypatching) as partial.","Plugin id `gbit.analyzer.python`; implemented in Python."],
  ["Fixture packages yield expected edges.","Dynamic constructs reduce completeness rather than being ignored."],
  ["Golden tests."],["T034","T037"])
s("T050","Discover pytest tests with stable IDs.",
  ["Collect with `pytest --collect-only` or the collection API in a subprocess.","Handle parametrization, fixtures and conftest files.","Map tests to defining functions."],
  ["Parametrized tests have stable per-case IDs.","conftest changes affect the right tests."],
  ["Discovery tests."],["T049"])
s("T051","Translate plans to pytest node IDs.",
  ["Emit node-id arguments or `-k` expressions as needed.","Parse JUnit XML results.","Report runnable granularity (T031)."],
  ["Selected tests only are executed.","Results map back to graph test IDs."],
  ["End-to-end run on a sample project."],["T050","T031"])
s("F17","The developer-facing commands.",
  ["init/index.","plan/test.","explain/graph."],
  ["The workflow in proposal section 8 works end to end."])
s("T052","Implement `gbit init` and `gbit index --full`.",
  ["`init`: detect projects, installed plugins and runners; write `gbit.yml`.","`index --full`: build and store the baseline graph.","Progress output and non-interactive mode for CI."],
  ["Works on a repository with both .NET and Python.","Re-running is idempotent."],
  ["CLI integration tests in a temp repository."],["T033","T042","T045"])
s("T053","Implement `gbit plan` and `gbit test`.",
  ["`plan --base --head` prints and optionally writes the plan (JSON and human-readable).","`test` executes through runner plugins and propagates exit status.","Exit codes distinguish success, widened and failed (T027)."],
  ["Output format matches the proposal's illustrative summary.","`test` runs exactly the planned runnable units."],
  ["End-to-end tests with both ecosystems."],["T021","T048","T051"])
s("T054","Implement `gbit explain` and `gbit graph --affected`.",
  ["`explain test:<id>` shows inclusion path or bounded exclusion statement.","`graph --affected` emits DOT and JSON for the impacted subgraph.","Stable ordering for diffing."],
  ["Included and excluded cases both produce explanations.","Graph output renders in Graphviz."],
  ["Golden-file tests."],["T029","T030"])
