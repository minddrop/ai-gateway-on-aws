"""Markdown snapshot of the Internal LLM gateway estimate, in English or Japanese.

Sections 1-6 (Summary, Estimate details, Rates, Assumptions, Lists, Calculation
rules) come from the template's snapshot.py, with this estimate's notes.
Sections 7-11 (model usage, optional items, sizing detail, open items,
findings) are this estimate's own. Numbers are computed from model.py with the
workbook's formulas (estimate.compute), so the markdown matches the workbook.

Run make.py to write it; render(lang) returns (text, untranslated strings).
"""
import model as M
import template_tools  # noqa: F401  (puts the template's tools/ on sys.path)
import tr
from estimate import compute
from ja import JA, RX
from snapshot import Notes, Snapshot, Translator, n

NOTES = Notes(
    parameters=[
        "Template default kept; the design docs give no reason to change it.",
        "Template default kept. Identified risks from 02 §14 are added as line items (§2, Contingency).",
        "Template default.",
        "Calculated once on each total and rounded down to JPY 1.",
        "Operation period of 2 years (2027-08 to 2029-07). 12- and 36-month views are in the multi-year table below.",
    ],
    views=[("Initial + first year", 12), ("Initial + operation period (grand total)", 24), ("Initial + 3 years", 36)],
    views_intro="The same initial cost with 12, 24 (the grand total above) and 36 months of recurring cost. Model inference is excluded in every view.",
    check_notes={"noprice": "CHECK (deliberate): the LiteLLM Enterprise licence placeholder has no price yet (01 Q-17, owner: Product owner). All other rows are priced."},
    checks_footer="The workbook could not be recalculated with LibreOffice in this environment (not installed). The Summary values above were computed independently in Python with the workbook's formulas (unit cost lookup, ROUND for PM and contingency, ROUNDDOWN for tax); Excel recalculates the workbook when it is opened.",
    category_notes={"mig": "No rows: no data migration in 01/02 (A16)", "pm": "No bottom-up PM rows",
                    "lic": "LiteLLM Enterprise licence not priced yet", "con": "Identified risks at expected value (02 §14)"},
    empty_categories={"mig": "*No line items: 01 and 02 define no data migration; what the gateway replaces is open (01 Q-2).*"},
    details_note="[PL] = AWS Price List API offer file for the region, checked 2026-11-17; USD amounts are converted at JPY 160/USD.",
    rates_note="**OPEN ITEM (FinOps): there are no internal rates yet. These are the template's sample rates (indicative blended market rates, excl. tax), kept unchanged; replace them on the Rates sheet.**",
)


def estimate(lang, T):
    """The estimate as snapshot.py and fill.py take it, with Japanese row text for jp."""
    rows, envs = M.estimate_rows()
    if lang == "jp":
        rows = tr.translate(rows, T, envs)
    est = dict(project=M.PROJECT, params=M.PARAMS, rates=M.RATES, days=M.DAYS, items=rows,
               assumptions=M.ASSUMPTIONS, exclusions=M.EXCLUSIONS)
    return est, envs


def render(lang):
    LANG = lang
    T = Translator(lang, JA, RX)
    est, (PT, DR, DEV, STG) = estimate(lang, T)
    res = compute(est["items"], M.RATES, M.DAYS, M.PARAMS)
    monthly, MON = res.monthly, M.PARAMS.months
    doc = Snapshot(est, res, lang, T, NOTES)
    w, table = doc.w, doc.table

    # ------------------------------------------------------------------ header
    XLSX = "CostEstimate_InternalLLMGateway_v0.1.xlsx"
    if LANG == "en":
        w("# Cost Estimate — Internal LLM gateway on AWS, v0.1")
        w("")
        w(f"> **Generated, read-only snapshot of the estimate model.** The master is the Excel workbook built from the cost estimate template (`{XLSX}`; Japanese workbook: `CostEstimate_InternalLLMGateway_v0.1_jp.xlsx`); it holds the formulas, dropdowns, rate lookups and checks. Numbers here do not recalculate — change the workbook instead. A Japanese version is in `cost_estimate_InternalLLMGateway_v0.1_jp.md`.")
        w("")
        w(f"> Purpose: internal budget approval in the design phase — **a budget estimate, not a quote** · Currency: JPY (line items excl. tax) · Prices: AWS list prices checked {M.CHECKED}, JPY {M.FX}/USD · Parameters: PM 10%, contingency 15% (applied to recurring: Yes), tax 10%, **{MON} recurring months in grand total** (24-month operation period). Model inference (Bedrock tokens charged back to teams) is **not** in the totals; see §7.")
        w("")
        w("Sections 1–6 mirror the workbook sheets (Summary · Estimate · Rates · Assumptions · Lists · Calculation rules). Sections 7–11 are additions for this estimate: model usage, separately priced options, infrastructure sizing detail, open pricing items by owner, and findings for the design documents.")
    else:
        w("# 費用見積 — 社内LLMゲートウェイ（AWS） v0.1")
        w("")
        w(f"> **本ファイルは見積モデルから自動生成した参照用スナップショットです。** 正本は費用見積テンプレートから作成したExcelブック（`CostEstimate_InternalLLMGateway_v0.1_jp.xlsx`。英語版のブックは`{XLSX}`）で、数式・プルダウン・単価参照・チェックを持ちます。本ファイルの数値は再計算されないため、変更はExcel側で行ってください。英語版は `cost_estimate_InternalLLMGateway_v0.1.md` です。")
        w("")
        w(f"> 目的：設計フェーズにおける社内予算承認用 — **予算見積であり見積回答ではない** · 通貨：円（明細は税抜） · 価格：AWS定価（{M.CHECKED}確認）、1USD＝{M.FX}円 · パラメータ：PM費率10%、予備費率15%（継続費用にも適用：Yes）、消費税10%、**総額に含める継続月数{MON}か月**（運用期間24か月）。モデル利用料（チームに配賦するBedrockトークン料金）は合計に**含めない**（§7参照）。")
        w("")
        w("1〜6章はExcelのシート構成（Summary・Estimate・Rates・Assumptions・Lists・計算ルール）に対応します。7〜11章は本見積の追加情報：モデル利用料の試算、別途試算のオプション、インフラのサイジング明細、オーナー別の価格未決事項、設計文書への指摘事項です。")
    w("")

    # ------------------------------------------------------------------ 1-6: the workbook sheets
    doc.sections()

    # 7 Model usage
    U = M.usage()
    w("## 7. Model usage (Bedrock tokens) — not in the totals" if LANG == "en" else "## 7. モデル利用料（Bedrockトークン） — 合計に含めない")
    w("")
    w(T("Model inference is a variable cost that LiteLLM charges back to the teams that use it (01 CST-007, 02 §5), so it is an exclusion (B1) and not part of the totals above. This table sizes it for budgeting by the teams and FinOps. Prices are the Bedrock on-demand prices for the `jp.` geographic cross-Region profiles (the non-global 'Standard' SKUs, about 10 % above Global) and the In-Region Tokyo prices, from [PL] AmazonBedrock and AmazonBedrockFoundationModels, ap-northeast-1, checked 2026-11-17."))
    w("")
    w("### 7.1 Prices used (USD per 1 million tokens)" if LANG == "en" else "### 7.1 使用した単価（USD／100万トークン）")
    w("")
    hd = ["Catalog ID", "Model", "How processed in Japan (01 §6.5)", "Input", "Cache write", "Cache read", "Output"] if LANG == "en" else \
         ["カタログID", "モデル", "日本国内での処理（01 §6.5）", "入力", "キャッシュ書込", "キャッシュ読込", "出力"]
    proc = {m: ("`jp.` profile" if m.startswith(("Claude", "Amazon")) else "In-Region Tokyo") for m in M.BR}
    if LANG == "jp":
        proc = {m: ("`jp.` プロファイル" if v.startswith("`jp.`") else "東京リージョン内") for m, v in proc.items()}
    f = lambda v: f"{v:g}" if v else "-"
    table(hd, [(M.MDL[m], m, proc[m], f(p["inp"]), f(p["cw"]), f(p["cr"]), f(p["out"])) for m, p in M.BR.items()], "lllrrrr")
    w(T("Note: [PL] lists Claude Haiku 5.5 at USD 0.11 / 0.55 per million input / output tokens, below Claude Haiku 4.5 (USD 1.10 / 5.50). The estimate uses the listed price; re-check it before the budget is fixed. MDL-011 (Azure OpenAI) is not priced (B3)."))
    w("")
    w("### 7.2 Scenario assumptions" if LANG == "en" else "### 7.2 シナリオの前提")
    w("")
    hd = ["Driver", "Low", "Expected", "High", "Basis"] if LANG == "en" else ["要素", "低", "想定", "高", "根拠"]
    S = M.SCEN
    table(hd, [
        (T("Active coding-agent users per month"), S["Low"]["users"], S["Expected"]["users"], S["High"]["users"],
         T("30 engineers, set by the requester on 2026-11-17 (A12); scenarios vary active days and workload volume only")),
        (T("Active days per user per month"), S["Low"]["days"], S["Expected"]["days"], S["High"]["days"],
         T("Claude Code cost docs (code.claude.com/docs/en/costs, checked 2026-11-17): enterprise average ≈ USD 13 per developer per active day and USD 150–250 per month → 12–19 active days")),
        (T("Tokens per active user-day (M): input / cache write / cache read / output"), "0.6 / 0.4 / 12 / 0.25", "0.6 / 0.4 / 12 / 0.25", "0.6 / 0.4 / 12 / 0.25",
         T("Calibrated so a full day on Claude Opus 5.5 at `jp.` prices costs ≈ USD 13 (") + f"USD {M.day_cost('Claude Opus 5.5'):.2f})"),
        (T("Model mix for coding agents"), "", T("Opus 5.5 60 %, Haiku 5.5 20 %, Sonnet 4.6 15 %, Opus 4.8 5 %"), "", T("Assumption; 01 §6.5 UC-1 models (Q-4 open)")),
        (T("Workloads (UC-2), share of expected volume"), "25 %", "100 %", "300 %",
         T("Expected per month: Haiku 4.5 1.0 B in / 0.2 B out; Nova 2 Lite 1.0 / 0.2; gpt-oss-120b 0.3 / 0.06; Mistral Large 3 0.2 / 0.04; Titan V2 and Cohere v4 embeddings 0.5 B each (assumption; 01 Q-4, Q-7)")),
    ], "lrrrl")
    w("### 7.3 Monthly usage and cost by model" if LANG == "en" else "### 7.3 モデル別の月間利用量と費用")
    w("")
    hd = ["Catalog ID", "Model", "Tokens/month Low (B)", "Expected (B)", "High (B)", "JPY/month Low", "Expected", "High"] if LANG == "en" else \
         ["カタログID", "モデル", "月間トークン 低（10億）", "想定（10億）", "高（10億）", "月額（円）低", "想定", "高"]
    body = []
    for m in M.BR:
        body.append((M.MDL[m], m, *(f"{U[s][m]['total_b']:,.1f}" for s in S), *(n(U[s][m]["usd"] * M.FX) for s in S)))
    tb = {s: sum(x["total_b"] for x in U[s].values()) for s in S}
    tu = {s: sum(x["usd"] for x in U[s].values()) for s in S}
    body.append(("", f"**{T('Total')}**", *(f"**{tb[s]:,.1f}**" for s in S), *(f"**{n(tu[s] * M.FX)}**" for s in S)))
    body.append(("", T("Total per year (× 12)"), "", "", "", *(n(tu[s] * M.FX * 12) for s in S)))
    body.append(("", T("Total over the 24-month operation period"), "", "", "", *(n(tu[s] * M.FX * 24) for s in S)))
    table(hd, body, "llrrrrrr")
    reqs = S["Expected"]["users"] * S["Expected"]["days"] * 200
    w(T("Tokens include cache reads, which are most of the coding-agent volume. Excl. tax. At the expected scenario, model usage is about ") +
      f"{tu['Expected'] * M.FX / monthly:.0f}" + T("× the gateway's own monthly running cost, which matches CMP §7.1 ('model usage dominates')."))
    w("")

    # 8 Options
    ra, az = M.options()
    w("## 8. Optional items priced separately (not in the totals)" if LANG == "en" else "## 8. 別途試算のオプション（合計に含めない）")
    w("")
    w(T("Route A and the Azure OpenAI backend are optional in the design (01 NG-5, MDL-011; 02 D-6) and are exclusions B2 and B3. Indicative AWS-side costs, using the traffic basis of CMP §8.9 (about 1 TiB a month each way) and [PL] Tokyo rates:"))
    w("")
    hd = ["Option", "Monthly AWS cost (USD)", "Monthly (JPY)", "One-time build", "Not included"] if LANG == "en" else \
         ["オプション", "AWS月額（USD）", "月額（円）", "初期構築", "含まないもの"]
    table(hd, [
        (T("Route A: Direct Connect ingress with internal ALB and split-horizon DNS"), "; ".join(f"{T(a)} {v:,.1f}" for a, v in ra["parts"]) + f" = **{ra['monthly_usd']:,.0f}**",
         n(ra["monthly_usd"] * M.FX), f"{ra['build_pd']} " + T("pd Infra/DevOps ≈ JPY") + f" {n(ra['build_pd'] * 55000)}",
         T("DX ports and circuits (sunk, A-8), carrier and colocation fees, Network team time")),
        (T("Azure OpenAI Japan East over DX + ExpressRoute"), "; ".join(f"{T(a)} {v:,.1f}" for a, v in az["parts"]) + f" = **{az['monthly_usd']:,.0f}**",
         n(az["monthly_usd"] * M.FX), f"{az['build_pd']} " + T("pd Senior engineer ≈ JPY") + f" {n(az['build_pd'] * 55000)}",
         T("All Azure charges (tokens, private endpoint, ExpressRoute), colocation router [CMP §8.9], legal approval (REG-001)")),
    ], "lrrll")
    w(T("CMP §8.9 estimated Route A at about USD 120 a month with the US-East example TGW attachment; the gateway VPC is already attached to the TGW for egress (02 §6), so no extra attachment is counted here, and the Route 53 Resolver inbound endpoint (CMP §4.6) is added."))
    w("")

    # 9 Sizing detail
    w("## 9. Infrastructure sizing detail" if LANG == "en" else "## 9. インフラのサイジング明細")
    w("")
    w(T("Monthly AWS cost per environment in USD, before conversion. Production and DR are one row per component in §2; dev and staging are one row each in §2 with this breakdown."))
    w("")
    hd = ["Environment", "Component", "USD / month"] if LANG == "en" else ["環境", "構成要素", "USD／月"]
    body = []
    for env, cs in ((T("Production (Tokyo)"), PT), (T("DR (Osaka)"), DR), (T("Dev (Tokyo)"), DEV), (T("Staging (Tokyo)"), STG)):
        for c in cs:
            body.append((env, T(c["name"]), f"{c['usd']:,.2f}"))
        body.append((f"**{env}**", f"**{T('Total')}**", f"**{M.tot(cs):,.2f}**"))
    table(hd, body, "llr")
    w(T("Comparison with 02 §12: the comparison's sample baseline of about USD 380 a month [CMP §7.1] covers one small environment before hardening. This design adds 3-AZ production, the guardrail service, 11 interface endpoints per AZ, the Osaka standby, observability and threat detection, and keeps staging at production topology; production alone is about") + f" USD {M.tot(PT):,.0f}" + T(" a month."))
    w("")

    # 10 Open pricing items
    w("## 10. Open items that need a price or a decision, by owner" if LANG == "en" else "## 10. 価格・判断が必要な未決事項（オーナー別）")
    w("")
    hd = ["Owner", "Item", "Where it is in the estimate", "Due (from 01/02)"] if LANG == "en" else ["オーナー", "項目", "見積上の箇所", "期限（01/02より）"]
    OPEN = [
        ("Product owner", "LiteLLM Enterprise licence price, incl. project months (01 Q-17) — the deliberate check failure", "Licences row (J blank)", "2026-12-18"),
        ("Product owner", "Pilot and GA dates (01 Q-3); they set the project-period environment months", "A2, Infrastructure one-time rows", "2026-12-18"),
        ("Product owner", "Model list, usage forecast and growth (01 Q-4, Q-7) for the model-usage budget", "§7", "2026-12-18"),
        ("Product owner", "AWS Support plan and LiteLLM support contract (01 Q-20)", "Exclusion B7", "2027-01-29"),
        ("Product owner", "Support hours, DR drill interval (01 Q-6)", "Operation rows (A17)", "2026-12-18"),
        ("FinOps", "Internal labor rates to replace the template sample rates", "Rates sheet, all labor rows (A4)", "—"),
        ("FinOps", "Budget exchange rate (JPY 160/USD assumed)", "A9, all AWS rows", "—"),
        ("FinOps", "Quick Sight reader and Grafana viewer counts; allocation of fixed platform cost (01 Q-12)", "Chargeback and Grafana rows", "2026-12-18"),
        ("Security / SOC", "Penetration-test vendor quote (template sample JPY 2,000,000 used)", "Security row", "2027-01-29"),
        ("Security / SOC", "Guardrail classifier choice and whether it needs a GPU (R-10, Q-13)", "Guardrail Fargate row, contingency R-10", "2026-12-18"),
        ("Security / SOC", "SIEM ingestion path and its cost (R-48)", "Exclusion B6", "2027-01-29"),
        ("Network", "Osaka egress design (R-7) and whether a fixed-IP front end is needed (R-32, Q-14)", "Contingency R-7, R-32", "2027-01-29"),
        ("Network", "Confirm the shared network-prod egress can serve the gateway (AS-18)", "A12, contingency AS-18", "2026-12-18"),
        ("Platform engineering", "Task sizing (R-42), Aurora and Valkey choices (R-23), staging scale-down policy (R-41)", "Infrastructure rows (A11)", "2027-01-29"),
        ("Platform engineering", "LiteLLM S3 callback batching on the pinned version (A18)", "S3 row", "2027-01-29"),
        ("Legal / privacy", "Whether per-team content logging is needed this phase (01 Q-10)", "Contingency R-6", "2026-12-18"),
    ]
    table(hd, [(T(a), T(b), T(c), d) for a, b, c, d in OPEN], "llll")

    # 11 Findings
    w("## 11. Findings for the design documents (not edited)" if LANG == "en" else "## 11. 設計文書への指摘事項（文書は未修正）")
    w("")
    w(T("docs/en/ was not changed. These are gaps or inconsistencies found while pricing the design; each should be resolved in 01/02 by its owner."))
    w("")
    FIND = [
        ("F-1", "02 §6 lists 10 interface endpoints and allows egress only to Entra and the licence endpoint, but 02 §2.2 sends LiteLLM metrics to Amazon Managed Service for Prometheus. Remote write from private subnets needs an `aps-workspaces` endpoint (or an egress rule). The estimate prices 11 endpoints (matching 02 §12 'about 11').", "Platform engineering"),
        ("F-2", "CMP A-9 / 01 PRF-M02 use 50–200 RPS as the sizing basis. Sustained 50 RPS is about 130 million requests a month; at the per-request token volume of a coding agent (≈ 66k tokens) that would be model spend of several million USD a month, far above the forecast in §7 (≈ 1.1 million requests with 30 engineers). PRF-M02 should be set from a usage forecast (01 Q-7). This estimate uses the design minimum for fixed capacity and the forecast for per-request charges.", "Product owner"),
        ("F-3", "02 §12 says no price was re-checked and R-46 lists the unestimated items. This estimate prices them; R-46 can point to it once reviewed.", "Platform engineering"),
        ("F-4", "02 §2.2 and §9 say ElastiCache is 'rebuilt cold' in Osaka without saying whether the cluster is created at failover or kept running. It affects RTO (AVL-M02) and cost; the estimate assumes it is created at failover.", "Platform engineering"),
        ("F-5", "Osaka egress and the Osaka secrets copy (R-7) have no design, so they are priced only as a contingency row.", "Network"),
        ("F-6", "02 §10 requires staging to match production for valid launch gates. Kept at production topology, staging costs about USD 2,090 a month, close to production. The design should say whether staging may scale down between upgrade windows (R-41).", "Platform engineering"),
        ("F-7", "Dev and staging also need an egress path to Entra for SSO; 02 §6 designs it only for production. The estimate assumes the same network-prod path (TGW attachment per environment).", "Network"),
        ("F-8", "02 §7.1 moves request metadata to Glacier after one year. If the LiteLLM S3 callback writes one object per request, per-object PUT and transition charges dominate the bucket cost; batching should be part of the design (A18).", "Platform engineering"),
        ("F-9", "Grafana and Quick Sight user counts, and who the team-facing dashboards are for (Grafana or the LiteLLM UI), are not in the design; both are per-user licences.", "FinOps"),
    ]
    hd = ["ID", "Finding", "Owner"] if LANG == "en" else ["ID", "指摘事項", "オーナー"]
    table(hd, [(a, T(b), T(c)) for a, b, c in FIND], "lll")

    return doc.text(), T.missing
