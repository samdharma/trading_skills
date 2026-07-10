# Troubleshooting

This page lists common issues and how to fix them.

## Installation issues

### `uv: command not found`

| Cause | Fix |
|-------|-----|
| `uv` is not installed | Install from [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/) |

### `No module named tscli`

| Cause | Fix |
|-------|-----|
| Dependencies not installed | Run `bash scripts/install-kimi-skill.sh` from the repo root |

## Skill loading issues

### `kimi-trading-skills` is not loaded

| Cause | Fix |
|-------|-----|
| Wrong `--skills-dir` path | Use `kimi --skills-dir ./skills` from the repo root, or `kimi --skills-dir ~/.kimi-code/skills` from anywhere |
| Symlink missing | Re-run `bash scripts/install-kimi-skill.sh` |

## Broker issues

### Broker check fails

| Cause | Fix |
|-------|-----|
| OpenD / IB Gateway not running | Start the gateway and log in |
| Wrong host or port | Check `TSCLI_OPEND_HOST`, `TSCLI_OPEND_PORT`, `TSCLI_IBKR_HOST`, `TSCLI_IBKR_PORT` |
| Missing environment variables | Export the variables and restart Kimi |

### Reports are empty or contain only fixtures

| Cause | Fix |
|-------|-----|
| Running in `manual` mode | Set broker environment variables and run with `--broker opend` or `--broker ibkr` |

## LLM issues

### LLM synthesis is skipped

```text
ERROR: LLM API key not found. Set TSCLI_LLM_API_KEY environment variable.
```

**Fix:**

1. Verify the variable is set: `echo $TSCLI_LLM_API_KEY`
2. Add `export TSCLI_LLM_API_KEY=sk-...` to `~/.zshrc` or `~/.bashrc`
3. Reload your shell config: `source ~/.zshrc`
4. Restart Kimi

Full LLM environment variables:

```bash
export TSCLI_LLM_API_KEY=sk-...
export TSCLI_LLM_BASE_URL=https://api.openai.com/v1
export TSCLI_LLM_MODEL=gpt-4o-mini
```

## Report issues

### Downstream command fails with schema error

| Cause | Fix |
|-------|-----|
| Upstream report is malformed or outdated | Re-run the upstream command and check the JSON report |

## Getting more help

- Run `bash scripts/run_all_tests.sh` to verify the CLI is healthy.
- Read the design spec: `docs/superpowers/specs/2026-07-09-kimi-trading-skills-design.md`
- Read the skill file: `skills/kimi-trading-skills/SKILL.md`
