# Internal LLM gateway: Operations runbook

<!--
Answers: how to deploy, roll back, monitor, recover and maintain the gateway.
Reader: the on-call engineer at 3 a.m. who has never touched the system. Exact commands, exact dashboards, no assumed knowledge.
Owns: operational procedures, alerts and their thresholds, incident procedures, the escalation path, the maintenance schedule. Refers to: design (02), setting values (04), environments (03 §2), contact details (11 §C).
Detail: every alert in §3 has an entry in §6, written from the block template there with every field filled. Every entry says whether prompt content could be involved, because that changes who is called. Every procedure step has Run: and Expect: lines.
Fill it in using the writing conventions in ../../README.md. Delete this comment when done.
-->

> Not started: written during build phase

## 1. Deployment

| Item | Value |
|---|---|
| Pipeline | [fill: CI/CD tool and link] |
| Release unit | LiteLLM image digest + `config.yaml` version + IaC version (02 §10) |
| Trigger | [default: merge to `main` → dev; tag → staging; approval → production] |
| Strategy | 02 §10; the drain time is the deregistration delay in 04 §4.3 |
| Expected duration | [default: up to 10 min per batch, because of the drain [CMP §4.9]] |
| Change window | [fill] |

**Before deploying to production:**
- [ ] Staging runs the same release unit.
- [ ] If the LiteLLM version changed: launch gates passed on staging (02 §11.2), database migration reviewed (02 §7.5), upstream release notes read for security and logging changes.
- [ ] If `config.yaml` changed a security-critical setting (04 §4.2): the gate that verifies it passed.
- [ ] Change ticket raised in [fill: change system] and linked in the pipeline run.

**After deploying:**
- Run: `[fill: smoke test command]` (virtual-key call on each API style, streaming call)
- Expect: all checks pass, and [fill: dashboard link] shows no rise in errors or latency for 15 minutes.

## 2. Rollback

1. **Redeploy the previous release unit.**
   - Run: `[fill: command or pipeline button]`
   - Expect: [fill: what the pipeline shows when it is done]
2. **Deal with database migrations.** A LiteLLM upgrade can migrate the schema. Follow the rollback plan recorded for this release (02 §7.5): if the previous version cannot run on the new schema, restore the snapshot taken before the upgrade. That loses spend rows written since the snapshot.
   - Run: [fill: snapshot restore command or runbook link]
   - Expect: [fill]
3. **Confirm.**
   - Run: `[fill: smoke test command]`
   - Expect: the smoke test passes, the error rate is back to baseline, and spend rows are being written.

## 3. Monitoring and alerts

Severity levels are defined in [fill: link to the incident severity definitions].

| Signal | Source | Threshold | Severity | Runbook |
|---|---|---|---|---|
| 5xx rate at ALB | CloudWatch | [default: > 2 % for 5 min] | [default: P1] | §6.1 |
| 504 / timeouts | ALB, LiteLLM | [fill] | [default: P2] | §6.2 |
| Bedrock throttling (429 from backend) | LiteLLM metrics, CloudWatch | [fill] | [default: P2] | §6.3 |
| Healthy ECS tasks below minimum | ECS | [default: < 3] | [default: P1] | §6.1 |
| Database unavailable / failover | RDS events | Any | [default: P1] | §6.4 |
| Redis unavailable | ElastiCache | Any | [default: P2] | §6.4 |
| Token validation failures spike (Entra reachability) | LiteLLM logs | [fill] | [default: P1] | §6.5 |
| Licence check failing | LiteLLM logs | Any | [default: P2] | §6.5 |
| Guardrail service errors / fail-open | Guardrail metrics | Any | [default: P1] | §6.6 |
| Spend not written (requests without spend rows) | [fill: reconciliation query] | [fill] | [default: P2] | §6.7 |
| Prompt content found outside approved stores | [fill: canary or DLP scan] | Any | **P1, privacy incident** | §6.8 |
| WAF blocks spike | WAF | [fill] | [default: P3] | §6.9 |
| Certificate or CRL expiry | [fill] | [default: 30 days before] | [default: P3] | §6.10 |

- **Logs:** [fill: CloudWatch log group; example Logs Insights query by request ID]
- **Metrics and dashboards:** [fill: Managed Prometheus / Grafana links]
- **Synthetic probe:** [fill: what it calls, from where, how often]

## 4. Backups, recovery and DR

| Data | Backup | Where | Restore last tested |
|---|---|---|---|
| LiteLLM database | [default: Aurora snapshots]; PITR window [fill] | Tokyo, copied to Osaka | [fill: YYYY-MM-DD] |
| Config and IaC | Git | [fill] | n/a: rebuilt from Git |
| Secrets | [fill: replicated to Osaka?] | [fill] | [fill: YYYY-MM-DD] |
| Logs and spend exports | S3 [fill: replication] | Japan only | [fill: YYYY-MM-DD] |

### 4.1 Failover to Osaka

The trigger, the decision owner and the known differences in Osaka (models, quotas) are in 02 §9.

1. **Promote the database.**
   - Run: [fill]
   - Expect: [fill]
2. **Start the gateway tasks in Osaka.**
   - Run: [fill]
   - Expect: [fill]
3. **Switch DNS.**
   - Run: [fill]
   - Expect: [fill]
4. **Confirm models are available in Osaka.**
   - Run: [fill]
   - Expect: [fill]

### 4.2 Failback to Tokyo

1. [fill: step, with Run: and Expect: lines]

### 4.3 DR drills

| Last drill | Result | Measured RTO / RPO, against AVL-M02 / AVL-M03 | Next drill |
|---|---|---|---|
| EXAMPLE: 2027-05-14 | Passed, with one finding: the Osaka quota for `claude-opus` was too low | RTO 42 min, RPO 2 s | 2027-11-12 |

## 5. Routine maintenance

| Task | Frequency | How | Owner |
|---|---|---|---|
| LiteLLM upgrade, including launch gates | [default: monthly, and on a security advisory] | 09 §3.1, 02 §11.2 | [fill] |
| Japan model availability re-check | Quarterly and before onboarding [CMP §7.2] | [fill] | [fill] |
| Master key rotation | [fill: schedule], when an admin leaves, and after every LiteLLM break-glass use (02 D-28) | New value, then restart every task [CMP §2.3.5] | [fill] |
| Virtual key expiry review | [default: monthly] | [fill] | [fill] |
| Monthly reconciliation of LiteLLM spend with CUR | Monthly | [default: Athena query; report the residual [CMP §7.2]] | FinOps |
| Egress IP allowlist review | [default: quarterly, and on any network change] | Update the allowlist **before** the IPs change [CMP A-14] | [fill] |
| mTLS trust store and CRL update | [fill] | [fill] | [fill] |
| Spend-log table size and retention | [default: monthly] | [fill] | [fill] |
| Access review (admins, secret readers) | [default: quarterly] | [fill] | [fill] |
| LiteLLM licence renewal | Yearly | [fill] | [fill] |

## 6. Incident procedures

One entry per alert in §3. Each entry uses this block; copy it for a new alert, and keep every field.

```markdown
### 6.n <Alert, as named in §3>
- **What it means:** <what is broken, and what the launch gates showed about this failure>
- **Impact:** <who is affected, and how>
- **Prompt content involved?** <No / Possibly / Yes, and why. If not No, call security and privacy (11 §C).>
- **Diagnose:** <dashboards, queries and commands, in order>
- **Mitigate:** <actions, in order, with commands or links>
- **Escalate:** <to whom (§7), and after how long>
- **Follow-up:** <what to check or re-run afterwards>
```

### 6.1 Gateway errors or unavailable
- **What it means:** [fill]
- **Impact:** [default: all users lose model access]
- **Prompt content involved?** No
- **Diagnose:** [default: dashboards; recent deploys; ECS task health; `/health/readiness`]
- **Mitigate:** [default: roll back (§2); scale out; fail over (§4.1)]
- **Escalate:** [fill: after how many minutes, to whom]
- **Follow-up:** [fill]

### 6.2 Timeouts and 504s
- **What it means:** [default: a layer in front of LiteLLM fired before LiteLLM did, so LiteLLM may have logged no error [CMP §2.7]]
- **Impact:** [default: long requests fail with 504]
- **Prompt content involved?** No
- **Diagnose:** [default: compare the timeouts at each layer with 04 §4.3; compare the ALB 504 count with LiteLLM's error log]
- **Mitigate:** [fill]
- **Escalate:** [fill]
- **Follow-up:** [fill]

### 6.3 Model backend throttled or unavailable
- **What it means:** [fill]
- **Impact:** [default: requests to the affected model fail with 429 or 5xx, or slow down]
- **Prompt content involved?** No
- **Diagnose:** [fill]
- **Mitigate:** [default: fall back within Japan only, never to a non-Japan profile; request a quota increase]
- **Escalate:** [fill]
- **Follow-up:** [fill]

### 6.4 Database or Redis unavailable
- **What it means:** [fill: what fails for key callers and Admin UI sessions, and for how long, as measured by V-8]
- **Impact:** [fill]
- **Prompt content involved?** No
- **Diagnose:** [fill]
- **Mitigate:** [fill]
- **Escalate:** [fill]
- **Follow-up:** [fill]

### 6.5 Entra or licence endpoint unreachable
- **What it means:** [fill: how long validation keeps working on cached signing keys (V-10), and what a task restart does while the licence endpoint is unreachable (V-9)]
- **Impact:** [fill]
- **Prompt content involved?** No
- **Diagnose:** [fill]
- **Mitigate:** [default: do not restart or scale in tasks until the licence endpoint is reachable, unless V-9 showed that a restart is safe [CMP §2.5]]
- **Escalate:** [fill]
- **Follow-up:** [fill]

### 6.6 Guardrail failure
- **What it means:** [fill: the configured failure behaviour (04 §4.5), and what it means for requests in flight]
- **Impact:** [fill]
- **Prompt content involved?** [fill]
- **Diagnose:** [fill]
- **Mitigate:** [fill: who can change fail-open or fail-closed during an incident, and how]
- **Escalate:** [fill]
- **Follow-up:** [fill]

### 6.7 Spend not recorded
- **What it means:** [fill]
- **Impact:** [default: a chargeback gap]
- **Prompt content involved?** No
- **Diagnose:** [fill]
- **Mitigate:** [fill: how to backfill from provider usage]
- **Escalate:** [fill]
- **Follow-up:** [fill]

### 6.8 Prompt content found where it must not be
- **What it means:** a setting or code path wrote prompt or response content outside the approved stores.
- **Impact:** [fill]
- **Prompt content involved?** **Yes. This is a privacy incident.** Call security and privacy (11 §C) immediately.
- **Diagnose:** [fill]
- **Mitigate:** [default: stop the writer; restrict access to the store]. **Do not delete evidence** until security decides; note any Object Lock on the store.
- **Escalate:** security and privacy, at once (§7)
- **Follow-up:** re-run V-1; find the setting or code path that wrote the content.

### 6.9 WAF blocks spike
- **What it means:** [default: legitimate requests are matching body rules, or an attack is under way [CMP §2.7]]
- **Impact:** [fill]
- **Prompt content involved?** [fill: whether WAF logs record the matched request text]
- **Diagnose:** [default: find which rule fires in the WAF logs; compare with recent rule changes]
- **Mitigate:** [fill]
- **Escalate:** [fill]
- **Follow-up:** [fill]

### 6.10 Certificate or CRL about to expire
- **What it means:** [fill]
- **Impact:** [fill: what fails for clients if the certificate, trust store or CRL expires]
- **Prompt content involved?** No
- **Diagnose:** [fill]
- **Mitigate:** [fill]
- **Escalate:** [fill]
- **Follow-up:** [fill]

## 7. Escalation

Contact details for every role below are in 11 §C.

| Level | Who | Escalate when |
|---|---|---|
| 1 | On-call engineer | An alert in §3 fires |
| 2 | Platform lead | [fill: after how many minutes without mitigation; any P1] |
| Security / privacy | Security / SOC, Legal / privacy | Prompt content may be involved (§6.8), or a security control fails |
| AWS | AWS Support ([fill: plan]) | [fill] |
| LiteLLM | LiteLLM Enterprise support | [fill] |
| Network | Network team | Egress IPs, secure web gateway, TLS inspection |
| Identity | Identity team | Entra ID, Okta or Intune |
