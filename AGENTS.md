# Repository guide for coding agents and people

The public gateway of the Research Harness (rambodambo). Read `README.md` first and
`docs/PUBLIC_THREAT_MODEL.md` before changing anything that faces the internet.

## Rules

- Import nothing from the harness; talk to its API over HTTP (`PUBLIC_PRIVATE_ORIGIN`, loopback only).
- Configured limits may only tighten the reviewed defaults (queue, daily quota, body size, deadlines).
- The public bundle must never contain private UI controls or endpoints (`make test` checks it).
- Never commit `.env`, Turnstile secrets or identity salts; never put secrets in `VITE_*` variables.
- `make test` before every commit.
