from spec_e0_e1 import s
# ---------------- E3 ----------------
s("E3","Measure GBIT against reality before anyone relies on it: run full suites beside planned subsets, replay history, inject faults and quantify misses and savings.",
  ["CI wrappers for GitHub Actions, Azure DevOps and GitLab CI.","Shadow-mode comparison with `gbit verify --full`.","Historical replay and mutation datasets.","Metric computation and observability."],
  ["Empirical missed-regression and wall-clock metrics meet an explicit rollout threshold on representative projects.","Zero confirmed omitted failure-detecting tests during shadow evaluation (a validation target, not a guarantee)."],
  notes="Exit criterion from the proposal: thresholds met across representative projects.")
s("F18","Run GBIT inside real CI systems with thin wrappers.",
  ["Provider wrappers.","No hosted dependency."],
  ["GitHub Actions, Azure DevOps, GitLab CI and the local CLI can all invoke the engine (AC-11)."])
s("T055","Provide a GitHub Actions integration.",
  ["Composite action `gbit/plan` and `gbit/test` wrapping the CLI.","Resolves base/head from the event; handles fork PR trust policy (T040).","Publishes the plan as a job summary and artifact.","Example workflow in `ci/github`."],
  ["A sample repo adopts GBIT with under 15 lines of YAML.","Fork PRs follow the safe policy."],
  ["Dogfood on this repository."],["T053","T040"])
s("T056","Provide an Azure DevOps integration.",
  ["Pipeline template (`ci/azure-devops`) wrapping the CLI.","Maps PR variables to base/head.","Publishes plan and JUnit results to the Tests tab."],
  ["Sample pipeline runs selected tests and reports results."],
  ["Run on a sample Azure DevOps project."],["T053","T066"])
s("T057","Provide a GitLab CI integration.",
  ["Include template (`ci/gitlab`).","Merge-request pipeline variable mapping.","JUnit report artifact and plan summary."],
  ["Sample `.gitlab-ci.yml` runs selected tests in an MR pipeline."],
  ["Run on a sample GitLab project."],["T053","T066"])
s("F19","Shadow mode: the safety net that proves selection quality.",
  ["Compare plan to full-suite outcomes.","`gbit verify --full`.","Persist predicted vs actual."],
  ["Every miss is detected and recorded with its cause (AC-12)."])
s("T058","Compare planned subsets to full-suite results.",
  ["Run all tests, then classify each failing test as selected or omitted.","Omitted failing tests are recorded as misses with the change, plan and graph snapshot.","Flaky tests excluded via reruns policy to avoid false misses."],
  ["A seeded miss is detected.","Flakiness handling is explicit and logged."],
  ["Replay on fixture repos with known failures."],["T053"])
s("T059","Implement `gbit verify --full`.",
  ["Executes the full suite, builds the comparison, prints and stores a report.","Exit status is non-zero on any miss.","Produces JSON for dashboards."],
  ["Output states miss rate, saved time, fallback rate.","Runs unattended in CI."],
  ["End-to-end test with a deliberately wrong plan."],["T058"])
s("T060","Persist prediction accuracy over time.",
  ["Store predicted and actual counts and durations in ExecutionHistory.","Query API for trends per repository and per policy.","Retention policy configurable."],
  ["History survives index rebuilds.","Trend query returns data for the last N builds."],
  ["Store tests."],["T042","T058"])
s("F20","Data to decide whether the planner is trustworthy.",
  ["Historical regressions.","Mutation harness.","Thresholds and reference repos."],
  ["Rollout criteria are explicit before enabling optimized mode."])
s("T061","Replay known historical regressions.",
  ["Select reference repositories with bug-fix commit history.","For each regression, rebuild the pre-fix state, plan the fix's inverse change, and check the failing test is selected.","Store results as a reusable dataset."],
  ["At least N regressions per ecosystem replayed (N set in T063).","Misses are triaged into missing-edge classes."],
  ["Replay harness tests on synthetic history."],["T058","T063"])
s("T062","Inject controlled faults to enrich the dataset.",
  ["Mutation operators covering interface changes, config shifts, schema changes, reflection, generated code and package upgrades.","Run mutants through plan and full suite; record kills and misses.","Budget-limited sampling for large repos."],
  ["Harness reports mutation-selection coverage per operator class.","Results reproducible with a seed."],
  ["Harness tests on a toy project."],["T058"])
s("T063","Decide rollout thresholds and the reference set up front.",
  ["Pick representative reference repositories (size, language mix, test style).","Set numeric thresholds: max miss rate, minimum time savings, max fallback rate, per proposal 1.2.","Document how thresholds gate moving from shadow to conservative to optimized."],
  ["Thresholds and repos recorded in an ADR before measurements begin.","Thresholds are not edited after seeing results without a recorded decision."],
  deps=["T008"])
s("F21","Make performance and correctness measurable.",
  ["Metric definitions.","Telemetry.","JUnit interchange."],
  ["Reports are comparable across repositories and releases."])
s("T064","Compute the four headline metrics.",
  ["Regression miss rate; selection efficiency net of indexing and planning overhead; fallback rate; explanation completeness.","Definitions documented with formulas.","CLI `gbit report` emits JSON and Markdown."],
  ["Metrics match hand-calculated values on fixtures.","Overhead is included in efficiency."],
  ["Unit tests with known inputs."],["T060"])
s("T065","Emit OpenTelemetry traces and metrics.",
  ["Spans for index, plan, plugin calls and test runs.","Metrics for latency and counts aligned with CI/CD semantic conventions where applicable.","OTLP export optional; off by default."],
  ["Planning p95 can be read from emitted metrics.","No telemetry leaves the machine unless configured."],
  ["In-memory exporter tests."],["T053"])
s("T066","Exchange results as JUnit XML.",
  ["Import runner JUnit results; export GBIT's normalized results.","Preserve durations, failures and test IDs.","Handle large files."],
  ["Round-trip fidelity on sample files from xUnit and pytest."],
  ["Round-trip tests."],["T048","T051"])
# ---------------- E4 ----------------
s("E4","Extend impact analysis across language boundaries and use runtime evidence to select tests in CI with enforced safety.",
  ["Contract analyzers (OpenAPI, JSON Schema, migrations).","TypeScript ecosystem.","Per-test runtime evidence.","Enforced optimized selection and a local visualization UI."],
  ["Contract changes select appropriate tests in other languages.","CI enforces the computed plan safely, with fallback."],
  notes="Exit criterion from the proposal: contract changes select tests in other languages and CI safely enforces the computed plan.")
s("F22","Contracts as first-class graph nodes.",
  ["Contract analyzers.","Public-vs-internal change classification."],
  ["A cross-language contract change propagates to consumers (AC-14)."])
s("T067","Analyze OpenAPI documents.",
  ["Parse OpenAPI 3.x; emit contract entities per operation and schema.","Link producers (server implementations) and consumers (clients) via CONSUMES_CONTRACT.","Detect added, removed and changed operations and schemas."],
  ["C# Pricing API -> OpenAPI -> TypeScript client scenario from the proposal selects C#, TS and Python tests."],
  ["Conformance scenario 9."],["T034"])
s("T068","Analyze JSON Schema and database migrations.",
  ["JSON Schema entities and `$ref` edges.","Migration scripts as changes to table entities with READS/WRITES edges from code where detectable.","Event/message schemas where present."],
  ["Changing a table column selects code and tests that read or write it, with uncertainty flagged where inferred."],
  ["Golden tests."],["T034"])
s("T069","Distinguish contract-visible changes from internal ones.",
  ["Rules: a change is public only if it alters the contract surface.","Plugins supply classification; kernel applies propagation accordingly.","Unknown classification defaults to public (safe)."],
  ["Internal implementation changes do not select consumers.","Unknown classifications widen selection."],
  ["Positive and negative fixtures."],["T067"])
s("F23","Third ecosystem: TypeScript.",
  ["Analyzer.","Jest/Vitest runner.","Client contract edges."],
  ["Three ecosystems run through the same planner."])
s("T070","Extract symbols and references from TypeScript/JavaScript.",
  ["Use SCIP (`scip-typescript`) or the TypeScript compiler API.","Resolve imports, re-exports and type references.","Flag dynamic imports and `any`-typed boundaries as partial."],
  ["Fixture projects yield expected edges."],
  ["Golden tests."],["T034","T037"])
s("T071","Discover and run Jest and Vitest tests.",
  ["Stable test IDs from file and describe/it names.","Translate plans to runner filters.","Parse JUnit/JSON results."],
  ["Selected tests only are run for both runners."],
  ["End-to-end runs."],["T070","T031"])
s("T072","Link TypeScript clients to the contracts they consume.",
  ["Detect generated clients and direct HTTP calls against known contract paths.","Emit CONSUMES_CONTRACT edges with confidence.","Unresolved calls to unknown endpoints mark partial completeness."],
  ["Changing an OpenAPI operation selects the TypeScript client tests."],
  ["Conformance scenario 9 across languages."],["T067","T070"])
s("F24","Observed test-to-code evidence, scoped and versioned.",
  ["Collector capability.","Per-test contexts.","Environment scoping.","Merge into snapshots."],
  ["Execution produces versioned relationship evidence (AC-12)."])
s("T073","Add the evidence-collector capability to the protocol.",
  ["Protocol methods to start instrumentation, receive per-test observations and finish.","Observation schema: test ID, entities touched, environment, revision.","Backward-compatible protocol minor version."],
  ["Existing plugins continue to work unchanged.","A stub collector can be driven by the host."],
  ["Protocol conformance additions."],["T034"])
s("T074","Collect per-test coverage for .NET and Python.",
  ["Python: coverage.py dynamic contexts per test.","`.NET`: per-test coverage via a collector that isolates test execution contexts.","Aggregate coverage alone is not accepted."],
  ["Coverage data maps individual tests to code entities.","Overhead is measured and documented."],
  ["Tests on sample projects; overhead benchmark."],["T073"])
s("T075","Prevent evidence from applying where it does not belong.",
  ["Tag evidence with build target, platform, runtime, configuration, instrumentation version.","Planner ignores or widens when scope differs.","Expire evidence on compiler/plugin changes."],
  ["Evidence collected on Linux debug does not silently justify exclusions for Windows release."],
  ["Scope-mismatch tests."],["T016","T074"])
s("T076","Feed runtime observations back into the graph.",
  ["Merge runtime edges as EXECUTES/VALIDATES-style verification evidence with provenance.","Never remove static edges because they were not observed.","Next snapshot includes accepted evidence."],
  ["After an instrumented run, the planner uses the new edges.","A path never observed is not treated as safe to skip."],
  ["Merge tests; monotonicity property still holds."],["T073","T075"])
s("F25","Safe, enforced selective execution.",
  ["Enforcement.","Optimized-mode gate.","Visualization."],
  ["Optimized mode runs only with validated evidence."])
s("T077","Make CI execute the plan and nothing less.",
  ["Wrapper verifies the executed set equals the planned set (including fallback).","Detects tampering or drift.","On plan failure, widens to the configured boundary."],
  ["A job that skips planned tests fails.","Plan generation failure never yields success with zero tests."],
  ["CI integration tests."],["T055","T027"])
s("T078","Permit optimized selection only with proof from validation.",
  ["Optimized mode requires recorded shadow-mode metrics meeting T063 thresholds for that repository.","Thresholds re-evaluated on a rolling window; auto-downgrade to conservative on breach.","Decision logged in the plan."],
  ["Enabling optimized mode without qualifying history is refused.","A breach downgrades the mode on the next run."],
  ["Policy tests with synthetic histories."],["T063","T064","T026"])
s("T079","Provide a local web UI to inspect impact.",
  ["`gbit ui` serves a local-only page showing the affected subgraph, selected/excluded tests and explanations.","No external network calls; works offline.","Accessible and keyboard navigable."],
  ["A user can click a test and see why it was selected.","Large graphs are paginated or collapsed."],
  ["UI smoke tests."],["T054"])
# ---------------- E5 ----------------
s("E5","Future direction: grow GBIT from a test selector into a change-impact verification platform that also selects agent evaluations affected by prompts, tools, schemas and workflows. Starts only after E1-E4 are validated.",
  ["Agent-native entity types.","Evaluation datasets and runners.","Evaluation of hosted and distributed options."],
  ["Changing a prompt, tool definition or workflow selects the relevant evaluations.","Hosted options are decided from measured need, not speculation."],
  notes="Gated: do not begin before the core graph kernel is validated (proposal section 11).")
s("F26","Extend the graph to agent systems.",
  ["Prompt/model/tool/workflow entities.","Evaluation datasets.","Prototype runner."],
  ["Agent artifacts propagate impact like code does."])
s("T080","Model agent artifacts as entities.",
  ["Entity kinds: prompt, model-config, mcp-tool, workflow-transition.","Edge types for prompt-uses-tool, workflow-invokes-prompt.","Plugin that extracts them from a sample agent repository."],
  ["A prompt edit reaches the workflows and evaluations that depend on it."],
  ["Fixture-based tests."],["T015"])
s("T081","Represent evaluation datasets and what they validate.",
  ["Dataset and scenario entities.","VALIDATES edges to prompts, tools and workflows.","Per-dataset cost and duration metadata."],
  ["Impact traversal returns affected evaluation scenarios."],
  ["Conformance-style scenarios for agent artifacts."],["T080"])
s("T082","Prototype running selected evaluations.",
  ["Runner plugin that executes a subset of an evaluation suite.","Reports pass/fail and scores in normalized form.","Time-boxed prototype with findings written up."],
  ["End-to-end selection and execution on a sample agent project."],
  ["Prototype demo and write-up."],["T081"])
s("F27","Decide on scale-out options with evidence.",
  ["PostgreSQL evaluation.","gRPC evaluation."],
  ["Each option has a recorded decision backed by measurements."])
s("T083","Evaluate PostgreSQL for centralized deployments.",
  ["Prototype the storage interface on PostgreSQL.","Benchmark against SQLite on the T043 suite with concurrent writers.","Write an ADR with a go/no-go recommendation."],
  ["ADR states measured trade-offs and migration impact."],
  ["Benchmark suite results."],["T043"])
s("T084","Evaluate gRPC as a plugin transport for remote execution.",
  ["Prototype a gRPC transport implementing the same protocol.","Measure latency/throughput against stdio and assess security (auth, TLS).","ADR with recommendation."],
  ["ADR states whether remote plugins are warranted and under what threat model."],
  ["Prototype benchmark."],["T035"])
