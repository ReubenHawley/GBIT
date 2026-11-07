# GBIT — Graph-Based Impact Testing

Language-agnostic, plugin-driven test impact analysis. See [`docs/GBIT_Architecture_Proposal.html`](docs/GBIT_Architecture_Proposal.html) for the design and [`docs/roadmap`](docs/roadmap) for the plan.

> Status: scaffold only. No functionality is implemented yet.

## Layout

| Path | Purpose |
|---|---|
| `src/Gbit.Core` | Language-neutral kernel: entities, graph, change model, impact, policy, planning, explanation |
| `src/Gbit.Protocol` | `gbit.plugin/v1` JSON-RPC over stdio contracts and transport |
| `src/Gbit.Storage.Sqlite` | SQLite graph store |
| `src/Gbit.Cli` | `gbit` command-line tool |
| `tests/Gbit.Core.Tests` | Unit tests |
| `tests/Gbit.Conformance` | Executable specification: graph fixtures, scenarios, protocol tests |
| `plugins/` | Out-of-process analyzers, runners and contract plugins |
| `ci/` | Thin CI provider wrappers |

## Build

```bash
dotnet build
dotnet test
```

## Contributing

Contributions are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md) and pick a task from the [roadmap](docs/roadmap). Please open an issue before starting large changes.

## License

Released under the [MIT License](LICENSE).
