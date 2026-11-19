# Internal LLM gateway on AWS: system documentation

Documentation for the internal LLM gateway: one OpenAI- and Anthropic-compatible endpoint, built on LiteLLM Proxy, that gives engineers and internal workloads access to models processed only in Japan. It runs on AWS in Tokyo (`ap-northeast-1`), with Osaka (`ap-northeast-3`) as the warm-standby DR region. Users sign in with Entra ID (Okta Verify MFA, Intune-compliant device) to create a personal LiteLLM virtual key, and every API call comes from an allowlisted office or DC network. Each call is charged to a team and held to budgets and rate limits.

The design analysis behind it is in [`../llm-gateway-comparison`](../llm-gateway-comparison/README.md) (English is authoritative), cited as `[CMP §n.n]`, `[CMP A-n]` (assumption) and `[CMP V-n]` (launch gate). Its recommendation, [CMP §7.2](../llm-gateway-comparison/docs/en/06-comparison.md#72-recommendation), is the starting point for this set. The set follows the template in [`../llm-gateway-docs-template`](../llm-gateway-docs-template/README.md).

**Status: design phase.** Nothing is built yet, and this repository holds no gateway code or IaC; the only code is the cost estimate generator in [`cost/tools/`](cost/tools/). 00, 01, 02 and 11 are written as Drafts for review. 03–10 are stubs that keep the template text and are written during the build phase.

| # | Document | Answers | Owner |
|---|---|---|---|
| 00 | [Overview](docs/en/00-overview.md) | What it is, scope, owners, service levels | Product owner |
| 01 | [Requirements](docs/en/01-requirements.md) | What it must do and how well; assumptions; model catalog | Product owner, with security, legal, FinOps |
| 02 | [Architecture and design](docs/en/02-architecture-and-design.md) | How it is built; data model; security design; DR; verification and traceability | Platform engineering |
| 03 | [Installation and setup](docs/en/03-installation.md) | Local stack; bootstrapping a new AWS environment; teardown | Platform engineering |
| 04 | [Configuration reference](docs/en/04-configuration.md) | Every setting, secret and switch, and which are security-critical | Platform engineering |
| 05 | [User guide](docs/en/05-user-guide.md) | Getting access, tool setup, tasks for users and team admins | Product owner |
| 06 | [API reference](docs/en/06-api-reference.md) | Endpoints, auth, errors, limits, versioning | Platform engineering |
| 07 | [Operations runbook](docs/en/07-operations-runbook.md) | Deploy, rollback, alerts, incidents, DR, maintenance | On-call / SRE |
| 08 | [Troubleshooting and FAQ](docs/en/08-troubleshooting-faq.md) | Symptoms, causes, fixes; common questions | Support + platform |
| 09 | [Development guide](docs/en/09-development-guide.md) | Repo layout, workflow, LiteLLM upgrades, tests | Platform engineering |
| 10 | [Release notes](docs/en/10-release-notes.md) | What changed and what callers must do | Platform engineering |
| 11 | [Appendices](docs/en/11-appendices.md) | Glossary, links, contacts, approval checklist | Documentation owner |

## Cost estimate

[`cost/`](cost/) holds the v0.1 budget estimate for building the gateway and running it for 24 months, made from the template in [`../cost-estimate-template`](../cost-estimate-template/README.md). The workbooks are the master (English and Japanese); the markdown files are generated read-only snapshots of them.

| File | What it is |
|---|---|
| `CostEstimate_InternalLLMGateway_v0.1.xlsx`, `…_jp.xlsx` | The estimate workbooks: the template filled with this estimate's line items, assumptions and parameters |
| `cost_estimate_InternalLLMGateway_v0.1.md`, `…_jp.md` | Snapshots: the workbook sheets (sections 1–6) plus model usage, options, sizing detail, open items and findings (7–11) |
| `tools/model.py` | Every price, quantity and assumption of this estimate: the single source of its numbers |
| `tools/ja.py`, `tools/tr.py` | Japanese text for this estimate |
| `tools/md.py` | The snapshot: the template's sections 1–6 with this estimate's notes, and sections 7–11 |
| `tools/make.py` | Builds all four files and checks them |

The generic work (filling the template, checking a filled workbook, calculating the Summary, rendering sections 1–6) is done by the scripts in the template repository's `tools/`. To regenerate the estimate after changing `model.py`, with `cost-estimate-template` cloned next to this repository (or `COST_ESTIMATE_TEMPLATE` set to its path):

```sh
pip install -r cost/tools/requirements.txt
python cost/tools/make.py
```

`make.py` fills both workbooks, checks them against the template, recalculates their Summary and compares it with the model, and writes both snapshots. It fails if a check fails or a Japanese string is missing from `ja.py`. openpyxl does not calculate formulas, so open each workbook in Excel and check its totals before you share it.

## Who reads what

| Reader | Start with | Then |
|---|---|---|
| New team member | 00, 02 | 03, 09 |
| Engineer using the gateway | 05 | 08 |
| Integrator / workload owner | 06 | 05 §4, 04 |
| On-call | 07 | 08, 04 |
| Security / privacy reviewer | 02 §4, §7, §8 | 01 §7, 04 §4.2 |
| FinOps | 01 §6.4 | 02 §5, 07 §5 |
| Manager / stakeholder | 00 | 10 |

## Where each fact lives

Each fact has one home. Other documents refer to it (for example "see 04 §4.3") instead of repeating it. The set then cannot contradict itself, and each fact is written once, to one level of detail.

| Fact | Home | Referred to from |
|---|---|---|
| System name, production hostname, document owners, review cadence | 00 Document control | Used as they are everywhere |
| Who is responsible for what | 00 §1.3 | 11 §C |
| Scope and non-goals, with reasons | 01 §1.3 | 00 §1.1 names them only |
| Assumptions and constraints | 01 §3–4 | 00 §1.5 summarises the main ones |
| Targets (SLO, RTO/RPO, latency) and requirement text | 01 | 00 §1.4 quotes the IDs only |
| Model catalog: what is needed | 01 §6.5 | 02 §5.1, 04 §4.1 |
| Data classification and retention periods | 01 §8 | 02 §7.1 (how retention is enforced) |
| Design decisions, components, data stores, threat model | 02 | 03, 07 |
| Requirement ↔ design ↔ test links | 02 §11.3 | 01 §10 |
| Launch gate results | 02 §11.2 | 07, 09, 10 |
| Environments: URLs, accounts, regions | 03 §2 | 02 §10, 04 §2.1, 07 |
| Setting names and values, including timeouts, limits, budgets, key lifetimes and model configuration | 04 | 02 names the settings it depends on; 05, 06, 07 and 08 refer to them |
| Status codes and what callers do about them | 06 §4 | 02 §3.2 (metering and logging only), 08 |
| Step-by-step procedures | 03 (one-time), 07 (operational), 09 (change) | 02 |
| Notice periods for breaking changes and model retirements | 10 §1 | 05 §6, 06 §5 |
| Terms | 11 §A | 01 §12 and every other document |
| Contact details | 11 §C | 00 §1.3, 07 §7, 08 §4 |

## Workflow

1. Approve 00 and 01 first. Start with use cases, constraints, assumptions and the model catalog.
2. Write 02 against a named requirements version.
3. Write 03–09 as the system is built. The pilot fills 08.
4. Before launch, run the launch gates (02 §11.2) and tick the checklist in 11 §D.
5. After launch, update 10 with every release, and run the gates again after every LiteLLM upgrade.

## Writing conventions

These rules keep the level of detail the same across the set, whoever writes each part. The comment at the top of each file adds what is specific to that document.

### Markers in the template

| Marker | Means | What to do |
|---|---|---|
| `[fill]`, `[fill: hint]` | No value yet. The hint says what is wanted. | Replace the whole marker with the value. |
| `[default: value]` | A proposed value, usually from the comparison. | Keep the value and remove the marker, or replace it. |
| `EXAMPLE:` at the start of a row, block or diagram (after the ID, in a row that has one) | An illustration of the expected detail. | Replace it with real content, or delete it. |
| `<…>` inside a code span or code block | The part that changes each time the line or block is used. | Leave the template as it is; replace the `<…>` parts in your copy. |
| Text with no marker | Already decided for this gateway, mostly from the comparison. | Check that it is still true. Change it only through review. |

A citation keeps its own brackets inside a marker: `[default: remote and home access [CMP A-13]]`.

### Finished cells and fields

Every table cell and every field in a block ends in one of these states:

- a value;
- `—`, where "none" is a correct answer (for example, a setting with no default);
- `n/a: <reason>`, where the item does not apply to this system;
- `TBD (<owner>, <YYYY-MM-DD>)`, for a known gap. It is allowed while a document is Draft or In review. An approved document keeps a TBD only if the gap is also tracked in 01 §9 or 02 §14.

Never leave a cell blank, and never delete a field from a block or a pre-filled row from a table: write `n/a: <reason>` instead. A blank cell cannot be told apart from a forgotten one.

### Detail standard

- **Specific to this system.** Name the real thing: the resource, setting key, dashboard link, group or team. "The dashboard" or "configure appropriately" is not enough.
- **Numbers carry units and scope.** A target also states its window and where it is measured.
- **Procedures are runnable.** Each step is one action, then a `Run:` line with the exact command or console path, then an `Expect:` line with what the reader sees when it worked. A new team member can follow it without asking anyone.
- **Tables are complete.** One row per item, every column filled. A table that the template leaves empty has one `EXAMPLE` row to copy the detail from.
- **Owners are teams or roles.** People are named only in document control and status lines, approvals, change logs and 11 §C.
- **Prose stays short.** A summary or problem statement is two to five sentences. Anything longer becomes a table or a list.
- **One fact, one home.** Where another document owns a fact, write the reference, not the value (see [Where each fact lives](#where-each-fact-lives)).

### Repeated blocks

Some sections are a list of entries with the same fields: user tasks (05 §5), endpoint details (06 §3.4), incident procedures (07 §6) and releases (10 §3). Each of these sections starts with a block template in a code block. Copy it for each entry, and keep every field, in the same order.

### References

| Reference to | Write it as | Example |
|---|---|---|
| A section in another document of the set | File number and section | `04 §4.2` |
| A section in the same document | Section only | `§4.2` |
| A whole document of the set | File number and title | `04 Configuration reference` |
| A requirement, test, gate, decision or risk | Its ID | `RES-001`, `T-001`, `V-1`, `D-1`, `R-1` |
| The comparison analysis | `CMP` and the section, assumption or gate, in square brackets | `[CMP §2.7]`, `[CMP A-13, A-14]`, `[CMP V-7]` |
| Anything outside the set | A Markdown link | `[LiteLLM proxy docs](https://docs.litellm.ai/docs/proxy/prod)` |

The launch gates in 02 §11.2 keep the comparison's IDs: `V-1` names our gate and its results, and `[CMP V-1]` names its definition in the comparison.

### Document status and IDs

- 01 and 02 are approved baselines, so each carries its own version, approvers and change log. The other documents are living documents: they follow the release in 10, carry an owner and a last-reviewed date in the status line at the top, and are reviewed on the cadence set in 00.
- Requirement IDs (`RES-001`, `AVL-M01`, …) are never reused or renumbered.
- English is authoritative. To keep a Japanese set, follow the comparison repo: same filenames under `docs/jp/`, updated in the same PR.

### Checking a document

Before a document goes to review, this prints nothing (replace `NN` with the file number):

```sh
grep -nE '\[(fill|default)[]:]|EXAMPLE|<!--|\|[[:space:]]*\|' docs/en/NN-*.md
```

It finds markers that were not replaced, examples, instruction comments and blank table cells. `grep -n 'TBD (' docs/en/NN-*.md` lists the gaps that are still open. Before the set is approved, run both over `docs/` and tick the checklist in 11 §D.
