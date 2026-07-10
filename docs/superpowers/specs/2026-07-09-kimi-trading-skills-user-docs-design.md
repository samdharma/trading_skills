# Kimi Trading Skills — User Documentation Redesign

## Goal

Replace the single `docs/user/user-guide.md` with a GitHub Docs–style user documentation set modeled on [Claude Trading Skills / Getting Started](https://tradermonty.github.io/claude-trading-skills/en/getting-started/).

## Scope

- In scope: `docs/user/` content, navigation, and `README.md` links.
- Out of scope: changing CLI code, automated doc generation, or publishing to a web host.

## Proposed structure

```text
docs/user/
├── README.md              # Docs home + table of contents
├── getting-started.md     # Install, first skill, quick win (Claude-style)
├── commands.md            # Command reference grouped by domain
├── brokers.md             # Futubull OpenD, IB Gateway, manual mode
├── workflows.md           # YAML workflow manifests and decision gates
├── reports.md             # JSON + Markdown report format
├── troubleshooting.md     # Common errors and fixes
└── safety.md              # No-live-orders policy and decision gates
```

## Design choices

1. **GitHub Docs theme.** Clean Markdown, navigation file, tables for prerequisites/options, code blocks for commands, admonitions via `> **Note:**` / `> **Important:**`.
2. **Mermaid diagrams.** Architecture, data flow, daily workflow, and broker setup flow where a diagram is clearer than text.
3. **Keep existing facts.** Reuse command names, env vars, report envelope, and safety rules already in `SKILL.md` and `user-guide.md`.
4. **Single source of truth.** Command tables derive from `SKILL.md` so the two files do not diverge.
5. **Reference Claude explicitly.** README notes that this is a Kimi port of Claude Trading Skills with the link.

## Mermaid diagrams to include

- `getting-started.md`: install → symlink → start Kimi → run first command.
- `commands.md`: user request → `tscli` → JSON report → optional LLM → summary.
- `brokers.md`: broker choice (OpenD / IB Gateway / manual) → env vars → broker check.
- `workflows.md`: manifest → sequential steps → decision gate → human approval.

## Validation

- `ruff` does not run on Markdown, so manual review: all links work, all commands match `SKILL.md`, all Mermaid blocks are syntactically valid.
- Run `uv run tscli --help` to confirm command names.
