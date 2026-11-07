# Contributing to GBIT

Thanks for your interest in GBIT. The project is at an early, scaffold-only stage, so the most useful contributions right now follow the [roadmap](docs/roadmap).

## Ways to contribute

- Pick an open issue (roadmap tasks are labelled by epic, e.g. `e1`) and comment that you are working on it.
- Report bugs or propose changes by opening an issue first for anything non-trivial.
- Improve documentation, conformance scenarios or plugin protocol tests.

## Development

Requires the .NET 10 SDK.

```bash
dotnet build
dotnet test
```

## Principles

- **Test first.** GBIT's acceptance tests are its executable specification. Add or update a failing test in `tests/Gbit.Conformance` or `tests/Gbit.Core.Tests` before the implementation.
- **Language-neutral kernel.** `Gbit.Core` must contain no language- or framework-specific logic; that belongs in plugins.
- **Correctness before optimization.** Unknown dependencies widen the selection; they never justify excluding tests.
- Read the [architecture proposal](docs/GBIT_Architecture_Proposal.html), especially the locked decisions in section 12.

## Pull requests

1. Fork the repository and create a branch from `main`.
2. Keep the change focused; one concern per PR.
3. Make sure `dotnet build` and `dotnet test` pass with no warnings.
4. Describe what changed and why, and link the issue or roadmap task (e.g. `T012`).

## License

By contributing you agree that your contributions are licensed under the [MIT License](LICENSE).
