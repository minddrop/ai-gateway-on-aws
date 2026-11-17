# Internal LLM gateway: Development guide

<!--
Answers: how the repository is organised and how a change gets from a laptop to production.
Reader: engineers changing configuration, IaC, guardrails or tests. Pair it with 03 for setup.
Owns: the repository layout, standards, the change workflow, LiteLLM upgrade steps, test levels, the definition of done. Refers to: deploys (07 §1), design (02), settings (04).
Detail: every check and test has its exact command. "Development" here is mostly configuration, IaC, guardrails and tests: we do not fork LiteLLM. If that changes, record it as a design decision (02 §13).
Fill it in using the writing conventions in ../../README.md. Delete this comment when done.
-->

> Not started: written during build phase

## 1. Repository layout

```text
[fill: repo name]/
├── config/            # LiteLLM config.yaml per environment
├── infra/             # IaC modules and per-environment variables
├── guardrails/        # In-VPC guardrail service (if built here)
├── clients/           # litellm-token helper; Intune payloads for Claude Code and Codex CLI
├── tests/
│   ├── smoke/         # Post-deploy checks
│   └── gates/         # Automated launch gates V-1 … V-n
├── scripts/
└── docs/              # This documentation set
```

## 2. Standards

- **Formatting and linting:** [fill: tools and commands]
- **IaC:** [fill: module conventions]; tags required on every resource, including cost tags
- **Config:** every security-critical setting in 04 §4.2 is set explicitly, never left to a default
- **Secrets:** never in the repo; [fill: secret-scanning tool]
- **Region:** resources only in `ap-northeast-1` / `ap-northeast-3` (the SCP also enforces this)

## 3. Workflow

1. Branch from `main`, named [default: `<type>/<ticket-id>-<short-name>`].
2. Make the change, with tests.
3. Run the checks locally: `[fill: lint, test and IaC plan commands]`.
4. Open a pull request. The template asks:
    - Which requirement IDs does this change?
    - Does it change a security-critical setting (04 §4.2)? Which gate verifies it?
    - Are the docs updated (and the Japanese translation, if kept)?
5. [fill: number] approvals, and CI passes. Changes to `config/` or `infra/` for production also need [fill: role] approval.
6. Merge with [default: squash]. Deployment follows 07 §1.

### 3.1 LiteLLM upgrades

1. Read the upstream release notes between the pinned and the target version. Look for changes to logging, auth, key management, spend tracking and DB migrations.
2. Update the pinned image digest (02 §1.3).
3. Deploy to staging and run every launch gate (02 §11.2). Record the results there.
4. Plan the rollback (07 §2), including the migration plan (02 §7.5).

## 4. Testing

| Level | What it checks | Command | Runs | Target |
|---|---|---|---|---|
| Config validation | `config.yaml` parses; security-critical values are as required | [fill] | Every PR | 100 % of 04 §4.2 |
| IaC checks | Plan, policy checks (region, tags, public exposure) | [fill] | Every PR | [fill] |
| Smoke | JWT call, key call, streaming, spend row written | [fill] | After every deploy | [fill] |
| Launch gates | V-1 … V-n | [fill] | Before release; every LiteLLM upgrade | All pass |
| Load | Throughput and latency overhead | [fill] | [default: before launch; quarterly] | PRF-M01 … PRF-M04 |
| DR drill | Failover to Osaka | [fill] | [default: twice a year] | AVL-M02, AVL-M03 |

## 5. Dependencies

- **LiteLLM:** pinned by image digest; upgraded as in §3.1.
- **Other images and packages:** [fill: scanning; update bot; approval for new dependencies; licence check]

## 6. Definition of done

- [ ] Code and config reviewed and merged
- [ ] Tests added; affected launch gates pass
- [ ] Requirement IDs linked in the PR
- [ ] Documentation updated: this set, release notes, translation if kept
- [ ] Monitoring and alerts cover the new behaviour, with an incident entry in 07 §6
