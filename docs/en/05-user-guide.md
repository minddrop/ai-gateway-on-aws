# Internal LLM gateway: User guide

<!--
Answers: how an engineer or a team lead gets access and does their job with the gateway.
Reader: engineers and team leads. Write in their words, organised by task, not by screen.
Owns: the rules on what may be sent, roles as users see them, tool setup, user tasks, notifications. Refers to: limits, timeouts and key lifetimes (04), API details (06), problems (08), notice periods (10 §1), contact details (11 §C).
Detail: every task in §5 follows the block template there, and a user can complete it without asking anyone. Client setup that Intune pushes says so: most users should have nothing to configure.
Fill it in using the writing conventions in ../../README.md. Delete this comment when done.
-->

> Not started: written during build phase

## 1. Getting started

- **Who can use it:** [default: employees in an `llm-team-*` group, on the corporate network [CMP A-13]]
- **How to get access:** [fill: request process; who approves team membership]
- **Which team you are charged to:** [fill: how it is decided; what to do if you are in two teams [CMP V-7]]
- **First thing to try:** [default: open Claude Code in a repository and ask it to explain a file; expect a response within seconds]

## 2. What you may and may not send

<!-- Short, plain rules. Link to the internal AI use policy (11 §B). -->

- **Allowed:** [fill: source code, internal documents up to classification …]
- **Not allowed:** [fill: secrets and credentials, customer personal data unless your team is approved for it, …]
- **What is recorded:** [default: who, which model, tokens and cost, and guardrail results. Prompt and response text are not stored unless your team has opted in [CMP A-10].]
- **Guardrails:** [fill: what is masked or blocked, and what you see when it happens]

## 3. Roles and permissions

| Role | Can do | Cannot do |
|---|---|---|
| User | Create, renew and delete your own keys in the Admin UI, each charged to one of your teams; call approved models with them; see your own usage and your team's spend, including each member's (02 D-26, R-52) | Create a key with no team, for another person or for a workload; use your key on management routes; change budgets (02 D-26) |
| Team lead | As a user, plus budget alerts; request workload keys and changes to budgets, members and models through a CI pull request (02 D-27) | Change teams, budgets or keys directly: there are no team admins in LiteLLM (02 D-27) |
| Platform viewer | [default: read-only view of every team, user, key and spend in the Admin UI (`proxy_admin_viewer`)] | [default: change anything; read prompt content (it is not stored)] |
| Platform admin | [default: production changes through CI only; emergencies through LiteLLM break-glass (02 D-27, D-28)] | [default: hold an admin role in production as a person; read prompt content (it is not stored)] |

## 4. Set up your tools

| Tool | How it is configured | What you need to do | Reference |
|---|---|---|---|
| Claude Code | `ANTHROPIC_BASE_URL` and `apiKeyHelper` set in managed settings pushed by Intune | [default: nothing; sign in to Windows or macOS as usual] | [CMP §2.3.4] |
| Codex CLI | Custom provider and `auth.command` in `~/.codex/config.toml`, pushed by Intune | [default: nothing] | [CMP §2.3.4] |
| SDKs (OpenAI / Anthropic) | Base URL from 06 §1; your personal key, sent as `x-api-key` or `Authorization: Bearer` | [fill: code snippet that reads the key without writing it to a file] | 06 §2 |
| IDE plugins that only accept a pasted key | Personal virtual key; its maximum lifetime is in 04 §4.4 | [fill: request process] | [CMP §2.3.4] |
| Workloads and agents | Service-account key created by CI after a pull request, kept in the workload's secret store (02 D-27) | Follow §5.2 | 06 §2 |

<!-- If mTLS is adopted, add per-tool certificate steps here [CMP §2.3.4]. -->

## 5. Tasks

Each task uses this block. Copy it for a new task, and keep every field.

```markdown
### 5.n <Task, starting with a verb>
- **Who:** <role from §3>
- **Before you start:** <what you need, or "Nothing">
- **Steps:**
  1. <action, with the exact link, command or form>
  2. <action>
- **Result:** <what you see when it worked, and how long it takes>
- **If something goes wrong:** <08 entry, or who to contact (11 §C)>
```

### 5.1 Check how much your team has spent
- **Who:** Any team member, team leads included; any user, for their own usage
- **Before you start:** [fill]
- **Steps:**
  1. [fill: open the Admin UI at … / the dashboard at …]
  2. [fill]
- **Result:** [default: spend by user and model for the current budget period]
- **If something goes wrong:** 08 §1

### 5.2 Request a key for a workload
- **Who:** Team lead
- **Before you start:** [default: the workload name, owner, team, models, expected volume and the expiry you need]
- **Steps:**
  1. [default: open a pull request in [fill: CI repository] that adds the key's definition with the details above]
  2. [default: after review, CI creates the service-account key and stores it in [fill: secret store] (02 D-27)]
- **Result:** [default: the key appears in your team's secret path. It expires on the date in the ticket, and the owner is reminded before it does (§6).]
- **If something goes wrong:** [fill]

### 5.3 Request a new model
- **Who:** Team lead
- **Before you start:** [default: the model, the use case and the expected volume]
- **Steps:**
  1. [default: open a ticket in [fill: queue] with the details above]
  2. [default: the platform team checks Japan availability and the legal position [CMP A-7], then adds the model to the catalog]
- **Result:** [default: the model appears in `GET /v1/models` and in the release notes (10)]
- **If something goes wrong:** [fill]

### 5.4 Request a budget increase
- **Who:** [default: Team lead, through a CI pull request (02 D-27)]
- **Before you start:** [fill]
- **Steps:**
  1. [fill]
- **Result:** [fill]
- **If something goes wrong:** [fill]

### 5.5 Leave a team or the company
- **Who:** [default: any user, and their team lead]
- **Before you start:** [fill]
- **Steps:**
  1. [fill]
- **Result:** [default: when you leave a team's `llm-team-*` group, the sync job removes you from that team and deletes your keys for it; when your Entra account is disabled, it blocks all your keys. Both happen within the target in 01 Q-8 (02 D-30, 01 TEN-007, IAM-006). After a team change, create a new key for your new team.]
- **If something goes wrong:** [fill]

## 6. Notifications

| Notification | When | Sent to | Channel |
|---|---|---|---|
| Budget threshold | [default: at 80 % and 100 % of the budget] | [default: team lead] | [fill: email / chat] |
| Key expiry | [fill: number of days before] | [default: key owner] | [fill] |
| Model retirement | The notice period in 10 §1 | [default: all users of the model] | [default: release notes and email] |

## 7. Limits and good practice

- **Maximum request duration:** 04 §4.3. Longer requests are cut; see 08 §1.
- **Rate and token limits for users and teams:** 04 §4.4.
- [default: Prefer prompt caching where the tool supports it; it lowers cost.]
- [default: Do not share your keys; they are tied to you and logged. Whether you may use your key on a server, a shared VM or a CI job is open (01 Q-18); workloads use service-account keys (§5.2).]
