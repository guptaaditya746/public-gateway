# public-gateway

The narrow internet-facing gateway of the [Research Harness](https://github.com/guptaaditya746/rambodambo):
anonymous visitors ask a question and watch a Fast or Adaptive run, with Turnstile, quotas, capacity
reservations and a projection that shows only sourced answers. It talks to the harness's private API
over HTTP on loopback and imports no harness code; the harness keeps the API side
(`/internal/public/*`, `HARNESS_MAX_CONCURRENT_PUBLIC_RUNS`).

It lived in the harness as `packages/public_gateway` until the harness's decision 0002 ("the public
gateway moves to its own repository"): it is internet-facing with its own threat model, so its
releases and security fixes no longer ride on harness commits. Its history came along.

## Layout

| Path | What |
|---|---|
| `src/harness_public_gateway/app.py` | the gateway app and its configuration (`PUBLIC_*` variables) |
| `web/` | the public UI (React + Vite): `src/PublicApp.tsx`; `public/_headers` is the Pages CSP |
| `scripts/public-preview.sh` | a temporary preview: harness corpus server and API on loopback, this gateway on 127.0.0.1:8787 |
| `scripts/export_public_examples.py` | reviewed runs (`config/public-examples.json`) → the public examples |
| `docs/` | API, deployment, operations, threat model |

## Use

```sh
make setup                                   # Python env and the web dependencies
make test                                    # ruff, pytest, web build and the bundle check
HARNESS_ROOT=~/thesis/rambodambo make preview
```

See [docs/PUBLIC_DEPLOYMENT.md](docs/PUBLIC_DEPLOYMENT.md) for a named-tunnel deployment and every
variable, and [docs/PUBLIC_THREAT_MODEL.md](docs/PUBLIC_THREAT_MODEL.md) for what it defends against.
