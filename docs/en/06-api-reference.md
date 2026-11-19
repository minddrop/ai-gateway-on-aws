# Internal LLM gateway: API reference

<!--
Answers: everything an integrator needs to call the gateway: base URL, authentication, endpoints, errors, limits, and how the API changes over time.
Reader: developers integrating workloads, SDKs and tools.
Owns: the caller-facing contract: endpoints enabled and blocked, authentication headers, status codes and what callers should do about them. Refers to: request and response bodies (LiteLLM's docs for the pinned version), timeout, limit and key-lifetime values (04), notice periods (10 §1).
Detail: document only what our deployment adds, removes or restricts, and link upstream for the rest. Every endpoint that differs from upstream gets a block from §3.4, with a working example request.
Fill it in using the writing conventions in ../../README.md. Delete this comment when done.
-->

> Not started: written during build phase

## 1. Overview

| Item | Value |
|---|---|
| Base URL | `https://llm.corp.example` (OpenAI style under `/v1`) |
| Reachable from | Office and DC egress IPs only [CMP A-13, A-14] |
| Upstream reference | [fill: link to the LiteLLM proxy docs for the pinned version (02 §1.3)] |
| Format | JSON over HTTPS (TLS 1.2+); streaming as server-sent events |
| Maximum request duration | 04 §4.3 |

## 2. Authentication

| Caller | Credential | Header | How to get it | Lifetime |
|---|---|---|---|---|
| Person (Claude Code, Codex CLI, IDE plugin, SDK) | Personal virtual key, charged to one of the user's teams and valid only on the model routes (02 D-26) | `x-api-key: <key>` or `Authorization: Bearer <key>`; both are tested on the pinned version (02 T-001, T-002) | Created in the Admin UI (05 §5); Claude Code and Codex CLI read it through the key helper (05 §4) | Maximum in 04 §4.4 |
| Workload | Service-account key created by CI (02 D-27) | `x-api-key: <key>` or `Authorization: Bearer <key>` | 05 §5.2 | Maximum in 04 §4.4 |
| Browser (Admin UI) | Entra sign-in, then a LiteLLM session cookie | Cookie set at `/sso/callback` | 05 §1 | `LITELLM_UI_SESSION_DURATION` (04 §4.2) |
| mTLS (if adopted) | Client certificate, in addition to the above | TLS handshake | [fill: Intune / Private CA] | [fill] |

## 3. Endpoints

<!-- List only what is enabled. State explicitly which LiteLLM endpoints are blocked at the WAF or not exposed, and why. -->

### 3.1 Model endpoints

| Method | Path | Purpose | Streaming | Notes |
|---|---|---|---|---|
| POST | `/v1/chat/completions` | OpenAI-style chat | Yes | — |
| POST | `/v1/messages` | Anthropic-style messages (Claude Code) | Yes | See §3.4 |
| POST | `/v1/embeddings` | Embeddings | No | [default: only if an embedding model is in the catalog] |
| GET | `/v1/models` | Models your team may use | No | — |
| [fill: any other enabled endpoint, one per row] | [fill] | [fill] | [fill] | [fill] |

### 3.2 Management and health endpoints

| Method | Path | Who may call | Reachable through the ALB? | Purpose |
|---|---|---|---|---|
| GET | `/health/liveliness`, `/health/readiness` | [default: load balancer, monitoring] | [fill] | Health |
| POST | `/key/generate` | Users from an Admin UI session, for their own keys on their own teams; the CI identity (02 D-26, D-27). Keys that users create are refused on it. | [default: yes, on the WAF path allowlist (02 D-31), with a stricter WAF rule set on `/key/*` [CMP §4.8]] | Issue a virtual key |
| GET | `/key/info`, `/user/info`, `/team/info` | [default: users for their own keys and user record; members of a team for that team's keys and spend, including each member's (02 R-52); platform viewers and admins] | [default: yes, on the WAF path allowlist (02 D-31)] | Inspect |
| GET | `/spend/logs`, [fill: report endpoints] | [default: users for their own spend; platform viewers and admins. FinOps uses Athena and Quick Sight, not this API.] | [fill] | Usage |
| GET | `/ui`, `/sso/*` | All users (Entra SSO: CA-GW-01, and CA-GW-02 for the admin and viewer groups) | [default: yes, on the WAF path allowlist (02 D-31), with a stricter WAF rule set [CMP §4.8]] | Admin UI |
| GET | `/metrics` | The Prometheus collector, on the dedicated metrics port only (02 D-32) | No: refused at the WAF (02 D-31, D-32) | Metrics |
| GET | `/`, `/docs`, `/redoc`, `/openapi.json`, `/routes` | Nobody | No: refused at the WAF (02 D-31); the documentation pages are also turned off (04 §4.2) | API documentation and route list |
| POST | `/config/*`, guardrail writes, team callback writes | Nobody through the ALB: configuration is deployed from `config.yaml` (02 D-19) | No: refused at the WAF (02 D-31) | Runtime settings |
| Any | `/scim/v2/*` | Nobody: LiteLLM SCIM is not used (02 D-30) | No: refused at the WAF (02 D-31) | User provisioning |
| POST | `/login`, `/v2/login` | Nobody: password sign-in is off while SSO is configured (04 §4.2) | [fill: refused at the WAF if the pinned Admin UI does not need it (02 V-3)] | Password sign-in |

### 3.3 Not available

| Endpoint / feature | Reason |
|---|---|
| [default: image generation, audio, files, batches, assistants, …] | [default: not in the catalog, or residency not checked [CMP §10.8.7]] |
| Pass-through routes (`/bedrock/*`, `/anthropic/*`, `/openai/*`, `/azure/*`, `/vertex_ai/*`, `/gemini/*` and the other provider prefixes) | Refused at the WAF: any valid key could call them, and LiteLLM has no switch to turn them off (02 D-31, 01 FUN-006) |
| Any path not on the WAF path allowlist | Refused at the edge (02 D-31); the list is kept with the WAF rules: [fill: location] |
| Client-set charging fields (`user`, request tags) | [fill: ignored for chargeback, or showback only [CMP V-7]] |
| `no-log` parameter | Ignored; every request is logged [CMP V-6] |

### 3.4 Endpoint details

Add one block for each endpoint whose behaviour differs from upstream. Copy this template, and keep every field.

```markdown
#### <METHOD> <path>
- **Differences from upstream:** <what our deployment adds, removes or restricts>
- **Allowed `model` values:** <list, or "see GET /v1/models">
- **Request size limit:** <"04 §4.4", or a stricter limit for this endpoint>
- **Example request:** <curl command with a placeholder token>
- **Example response:** <trimmed>
```

#### EXAMPLE: POST /v1/messages
- **Differences from upstream:** request-body tags and the `user` field do not change the team that is charged [CMP V-7]; the `no-log` parameter is ignored [CMP V-6].
- **Allowed `model` values:** see `GET /v1/models`, for example `claude-opus`.
- **Request size limit:** 04 §4.4.
- **Example request:**
  ```sh
  curl -sS https://llm.corp.example/v1/messages \
    -H "x-api-key: <your-key>" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{"model": "claude-opus", "max_tokens": 64, "messages": [{"role": "user", "content": "Say hello"}]}'
  ```
- **Example response:** `{"type": "message", "role": "assistant", "content": [{"type": "text", "text": "Hello!"}], "stop_reason": "end_turn", …}`

## 4. Errors

<!-- The caller's view of the design decisions in 02 §3.2. -->

| HTTP status | When | What the caller should do |
|---|---|---|
| 400 | Invalid request, unknown or unapproved model | Fix the request; check `GET /v1/models` |
| 401 | Missing, unknown, expired or blocked key | Check the key's expiry; renew it in the Admin UI (05 §5) |
| 403 | Source IP not allowlisted, WAF block, no mTLS certificate, model not allowed for the team, or a key used on a route it may not call (02 D-26) | See 08 §1 |
| 429 | Rate or token limit reached | Retry after `Retry-After`; ask for a higher limit |
| [fill: status code] | Budget exceeded | [default: wait for the next budget period, or request an increase (05 §5.4)] |
| [default: 400] | Guardrail blocked the request | [default: remove the blocked content; the message says which rule] |
| 5xx | Gateway or upstream fault | Retry with backoff; report the request ID |
| 504 | A timeout in front of LiteLLM fired | See 08 §1 |

Every response carries a request ID in [fill: header name]. Include it in support requests.

## 5. Limits and versioning

- **Rate and token limits:** 04 §4.4 (per user, key and team).
- **Request body size:** 04 §4.4 (`max_request_size_mb`). The WAF inspects only the first 8 KB of a body, so it cannot enforce a total size; LiteLLM does [CMP §2.7].
- **Versioning:** the API follows the upstream OpenAI and Anthropic formats. A gateway release can change behaviour when LiteLLM is upgraded or a model is retired. Breaking changes are announced in 10 Release notes, with the notice period set in 10 §1.
- **Model names:** public model names are stable aliases. [fill: how a change of the backend model behind an alias is announced]
