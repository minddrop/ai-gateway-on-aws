# Internal LLM gateway: Configuration reference

<!--
Answers: every setting the gateway reads, where it comes from, its value per environment, and what breaks if it is wrong.
Reader: platform engineers changing configuration, reviewers of configuration PRs, on-call engineers checking a value.
Owns: setting names and values, including timeouts, limits, budgets, key lifetimes, model configuration, secrets and feature switches. Refers to: the reasons behind them (02), the environment list (03 §2). The config repository is the source of truth: link to the file rather than pasting it whole.
Detail: every row names the exact key and its section. Settings marked security-critical name the launch gate that proves them (§4.2), and that gate runs again after every change to them.
Fill it in using the writing conventions in ../../README.md. Delete this comment when done.
-->

> Not started: written during build phase

## 1. How configuration is loaded

| Source | Holds | Changed by | Takes effect |
|---|---|---|---|
| `config.yaml` (in [fill: repo path]) | Models, router, LiteLLM and general settings, guardrails, callbacks | Pull request | [default: on deploy (restart)] |
| Environment variables (ECS task definition, from IaC) | Connection strings, feature switches | Pull request on IaC | On deploy |
| Secrets Manager (injected as ECS secrets) | Keys and passwords | [default: platform admins]; see §3 | On restart |
| LiteLLM database (Admin UI / API) | Teams, users, keys, budgets; models too if `STORE_MODEL_IN_DB` is on | Admins | Immediately |

**Precedence:** [fill: which wins when a setting exists in both the config file and the database]

**Drift rule:** [fill: is changing models or budgets in the UI allowed in production? If yes, how are UI changes recorded and reconciled with the repo?]

## 2. Environment variables

| Name | Type | Required | Default | Description | Security-critical |
|---|---|---|---|---|---|
| `DATABASE_URL` | string (secret) | Yes | — | PostgreSQL connection | Yes |
| `LITELLM_MASTER_KEY` | secret | Yes | — | Admin credential; see §3 | Yes |
| `LITELLM_SALT_KEY` | secret | Yes | — | Encrypts stored credentials. Never change it without re-encryption. | Yes |
| `LITELLM_LICENSE` | secret | Yes | — | Enterprise licence [CMP A-6] | No |
| `REDIS_HOST` / `REDIS_PORT` / `REDIS_PASSWORD` | string | Yes | — | Shared rate-limit and budget counters | No |
| `STORE_MODEL_IN_DB` | bool | No | [fill] | Whether models can be added in the UI | Yes |
| [fill: every other variable the gateway reads, one per row] | [fill] | [fill] | [fill] | [fill] | [fill] |

### 2.1 Values per environment

<!-- One row per variable in §2. The environments are those in 03 §2. For a secret, give the Secrets Manager name, never the value. -->

| Name | Local | Dev | Staging | Production | DR |
|---|---|---|---|---|---|
| EXAMPLE: `LITELLM_MASTER_KEY` | Random value in `.env` | Secret `llm-gw/dev/master-key` | Secret `llm-gw/stg/master-key` | Secret `llm-gw/prod/master-key` | Secret `llm-gw/prod/master-key`, replicated to Osaka |
| `DATABASE_URL` | [fill] | [fill] | [fill] | [fill] | [fill] |
| `LITELLM_MASTER_KEY` | [fill] | [fill] | [fill] | [fill] | [fill] |
| `LITELLM_SALT_KEY` | [fill] | [fill] | [fill] | [fill] | [fill] |
| `LITELLM_LICENSE` | [fill] | [fill] | [fill] | [fill] | [fill] |
| `REDIS_HOST` / `REDIS_PORT` / `REDIS_PASSWORD` | [fill] | [fill] | [fill] | [fill] | [fill] |
| `STORE_MODEL_IN_DB` | [fill] | [fill] | [fill] | [fill] | [fill] |
| [fill: every other variable in §2] | [fill] | [fill] | [fill] | [fill] | [fill] |

## 3. Secrets

| Secret | Used for | Who can read it | Rotation | Runbook |
|---|---|---|---|---|
| Master key | Admin API and UI password login | [default: platform admins only]. Everyone who can read it is in effect a proxy admin [CMP §2.3.5]. | [fill: schedule], and when an admin leaves | 07 §5 |
| Salt key | Encrypting credentials in the DB | [fill] | **Never**, unless a re-encryption plan is approved | — |
| DB credentials | Database | [fill] | [default: automatic, by Secrets Manager] | [fill] |
| Licence key | LiteLLM Enterprise | [fill] | On renewal | [fill] |
| [default: Provider keys, if any non-Bedrock backend] | [fill] | [fill] | [default: 90 days [CMP §4.8]] | [fill] |

Secrets are never committed. `.env` is git-ignored. [fill: secret-scanning tool] runs on every push.

## 4. `config.yaml` settings

### 4.1 Models (`model_list`)

<!-- One row per public model name. The routing design is in 02 §5.1; the catalog of what is needed is in 01 §6.5. -->

| `model_name` (what clients send) | Backend model / profile | Region | `rpm` / `tpm` | Pricing source | Requirement |
|---|---|---|---|---|---|
| EXAMPLE: `claude-opus` | `arn:aws:bedrock:ap-northeast-1:111122223333:application-inference-profile/a1b2c3d4e5f6` (copied from the `jp.` Claude Opus 5.5 profile) | ap-northeast-1 | 600 / 2,000,000 | Custom per-model pricing in `config.yaml`, checked by V-4 | MDL-001 |

### 4.2 Security- and privacy-critical settings

<!-- A wrong value here leaks prompts or lets callers bypass controls. Each row names the launch gate that proves it. -->

| Setting | Section | Required value | Why | Verified by |
|---|---|---|---|---|
| `turn_off_message_logging` | `litellm_settings` | `true` | Content is not sent to callbacks [CMP §2.8] | V-1 |
| `store_prompts_in_spend_logs` | `general_settings` | `false` | Content is not stored in spend logs [CMP §2.8] | V-1 |
| `global_disable_no_log_param` | `litellm_settings` | `true` | Clients cannot skip tracking [CMP §2.4] | V-6 |
| Response cache | `litellm_settings.cache` | Off | Cached responses hold content [CMP §2.8] | V-1 |
| `allow_requests_on_db_unavailable` | `general_settings` | [fill: true or false, from the V-8 result] | Behaviour on a DB outage; the route is internet-facing [CMP V-8] | V-8 |
| [fill: JWT auth settings for issuer, audience and team claim] | [default: `general_settings.litellm_jwtauth`] | [fill] | Accept only our tenant's tokens for this gateway, and map each one to the right team [CMP §2.3] | V-2, V-7 |
| [default: `key_generation_settings`] | [default: `litellm_settings`] | [default: personal keys by `proxy_admin` only; team keys by team admins] | Users must not create keys that skip Conditional Access [CMP §2.3.5] | V-2 |

### 4.3 Timeouts

<!-- Every layer must agree; the shortest one fires first [CMP §2.7]. -->

| Layer | Setting | Value |
|---|---|---|
| ALB idle timeout | IaC | [default: 600 s] |
| LiteLLM `request_timeout` | `litellm_settings` | [default: 570 s, below the ALB] |
| Target group deregistration delay | IaC | [default: 600 s or more] |
| Client (Claude Code, SDKs) | Client configuration | [fill] |

### 4.4 Router, budgets and limits

| Item | Setting | Value |
|---|---|---|
| Routing strategy | `router_settings.routing_strategy` | [fill] |
| Retries and cooldown | `router_settings`: `num_retries`, `allowed_fails`, `cooldown_time` | [fill] |
| Fallbacks | [fill: config key] | [fill: per model; Japan-only deployments (02 §5.1)] |
| Default team budget and period | [fill: where it is set] | [fill] |
| Default per-user and per-key limits (TPM, RPM, budget) | [fill: where it is set] | [fill] |
| Maximum lifetime and limits of a key | `upperbound_key_generate_params` [CMP §2.3.5] | [default: `duration` 90 days] |
| Maximum request size | `max_request_size_mb` [CMP §2.7] | [fill: MB] |

### 4.5 Guardrails and callbacks

| Name | Type | Mode (pre-call, post-call, during call) | Applies to | Failure behaviour (fail open or closed) |
|---|---|---|---|---|
| [default: PII masking] | [default: Presidio, in the VPC [CMP §4.8]] | [fill] | [fill] | [fill] |
| [default: Prompt-attack and content classifier] | [default: Japanese-capable classifier, in the VPC [CMP §4.8]] | [fill] | [fill] | [fill] |
| [default: S3 logging callback] | [fill] | [fill] | [fill] | [fill] |

## 5. Feature switches

| Switch | Default | Effect when on | Owner | Review or remove by |
|---|---|---|---|---|
| [default: mTLS required] | [default: off] | [default: the ALB rejects clients without an Intune or workload certificate] | [fill] | [fill: YYYY-MM-DD] |
| [default: Per-team content logging] | Off | [default: content is written to the opt-in store for that team only; needs legal approval [CMP A-10]] | [fill] | [fill: YYYY-MM-DD] |
