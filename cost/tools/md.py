"""Generate the markdown snapshot of the estimate in English or Japanese.

Usage: python md.py en|jp <out.md>
Numbers are computed from model.py with the workbook's formulas (Unit cost,
Subtotal, Summary), so the markdown matches the Excel file.
"""
import math
import re
import sys

import model as M

LANG = sys.argv[1] if len(sys.argv) > 1 else "en"
JA, RX = {}, None
if LANG == "jp":
    from ja import JA, RX, calc as CALC_JA  # noqa: F401
MISSING = []


def T(s):
    if LANG == "en" or not s:
        return s
    if s in JA:
        return JA[s]
    r = RX(s, T)
    if r is not None:
        return r
    if not re.search(r"\b[a-z]{3,}\b", s):
        return s
    MISSING.append(s)
    return s


def side(label):
    """Bilingual workbook label 'English / 日本語' -> one language."""
    if " / " not in label:
        return label
    return label.rsplit(" / ", 1)[1] if LANG == "jp" else label


def n(x, dash=True):
    if x is None:
        return ""
    if dash and abs(x) < 0.5:
        return "-"
    return f"{round(x):,}"


def q(x):
    return f"{x:,.2f}".rstrip("0").rstrip(".") if x % 1 else f"{x:,.1f}"


# ------------------------------------------------------------------ compute
rows, (PT, DR, DEV, STG) = None, (M.prod_tokyo(), M.dr_osaka(), M.dev_env(), M.stg_env())
rows = M.labor_rows() + M.infra_rows(PT, DR, DEV, STG) + M.risk_rows()
for r in rows:
    if r["j"]:
        r["F"] = r["j"]
    elif r["unit"] == M.U_PM:
        r["F"] = M.RATES[r["role"]]
    elif r["unit"] == M.U_PD:
        r["F"] = round(M.RATES[r["role"]] / M.DAYS)
    else:
        r["F"] = None
    r["G"] = r["qty"] * r["F"] if r["F"] else 0

cats = M.CAT_ORDER
ot = {k: sum(r["G"] for r in rows if r["key"] == k and r["type"] == M.T_OT) for k in cats}
rc = {k: sum(r["G"] for r in rows if r["key"] == k and r["type"] == M.T_RC) for k in cats}
PMP, CP, TAX, MON = 0.10, 0.15, 0.10, M.OPS_MONTHS
dev = sum(ot[k] for k in M.PHASE)
pm = round(PMP * dev)
c60 = dev + ot["pm"] + pm + sum(ot[k] for k in ("qa", "inf", "lic", "sec"))
c61 = sum(rc[k] for k in cats if k != "con")
cont_ot, cont_rc = round(CP * c60), round(CP * c61)
initial = c60 + ot["con"] + cont_ot
monthly = sum(rc.values()) + cont_rc
annual = monthly * 12
tax = lambda x: math.floor(x * TAX)
effort = sum(r["qty"] for r in rows if r["unit"] == M.U_PM and r["type"] == M.T_OT) + \
    sum(r["qty"] for r in rows if r["unit"] == M.U_PD and r["type"] == M.T_OT) / M.DAYS
noprice = [r for r in rows if r["G"] == 0]
grand = lambda m: initial + monthly * m

# ------------------------------------------------------------------ text
out = []
w = out.append


def table(head, body, align):
    w("| " + " | ".join(head) + " |")
    w("|" + "|".join("---:" if a == "r" else "---" for a in align) + "|")
    for b in body:
        w("| " + " | ".join("" if x is None else str(x) for x in b) + " |")
    w("")


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

# 1 Summary
w("## 1. Summary / サマリー" if LANG == "en" else "## 1. サマリー")
w("")
w("### Project information / 案件情報" if LANG == "en" else "### 案件情報")
w("")
H = ["Item", "Value"] if LANG == "en" else ["項目", "値"]
table(H, [
    (T("Project name / 案件名"), T("Internal LLM gateway on AWS (build and 24-month operation)")),
    (T("Estimate version / 版数"), "v0.1"),
    (T("Estimate date / 作成日"), "2026-11-17"),
    (T("Prepared by / 作成者"), T("Claude (AI assistant), for platform engineering")),
    (T("Status / ステータス"), T("Draft / 作成中")),
], "ll")

w("### Parameters / パラメータ" if LANG == "en" else "### パラメータ")
w("")
table(["Parameter", "Value", "Notes"] if LANG == "en" else ["パラメータ", "値", "備考"], [
    (T("PM cost (% of development cost) / PM費率"), "10.0%", T("Template default kept; the design docs give no reason to change it.")),
    (T("Contingency (% of cost) / 予備費率"), "15.0%", T("Template default kept. Identified risks from 02 §14 are added as line items (§2, Contingency).")),
    (T("Apply contingency to recurring cost? / 継続費用にも予備費を適用"), "Yes", T("Template default.")),
    (T("Consumption tax rate / 消費税率"), "10.0%", T("Calculated once on each total and rounded down to JPY 1.")),
    (T("Recurring months in grand total / 総額に含める継続月数"), str(MON), T("Operation period of 2 years (2027-08 to 2029-07). 12- and 36-month views are in the multi-year table below.")),
], "lrl")

w("### Totals / 合計" if LANG == "en" else "### 合計")
w("")
hd = ["Item", "Excl. tax (JPY) / 税抜", "Consumption tax (JPY) / 消費税", "Incl. tax (JPY) / 税込", "Notes"] if LANG == "en" else \
     ["項目", "税抜（円）", "消費税（円）", "税込（円）", "備考"]
tot_rows = [
    (T("Total initial cost (one-time) / 初期費用合計"), initial, T("All one-time costs incl. PM and contingency")),
    (T("Total recurring cost – monthly / 継続費用（月額）"), monthly, T("Recurring rows per month (+ contingency)")),
    (T("Total recurring cost – annual / 継続費用（年額）"), annual, T("Monthly × 12")),
]
body = [(a, n(v), n(tax(v)), n(v + tax(v)), c) for a, v, c in tot_rows]
gt = grand(MON)
body.append((f"**{T('Grand total (initial + 24 months recurring) / 総額')}**", f"**{n(gt)}**", f"**{n(tax(gt))}**", f"**{n(gt + tax(gt))}**", T("Tax calculated on this total")))
table(hd, body, "lrrrl")

w("### Multi-year views / 複数年試算" if LANG == "en" else "### 複数年試算")
w("")
w(T("The same initial cost with 12, 24 (the grand total above) and 36 months of recurring cost. Model inference is excluded in every view.") )
w("")
hd = ["View", "Recurring months", "Excl. tax (JPY)", "Consumption tax (JPY)", "Incl. tax (JPY)"] if LANG == "en" else \
     ["試算", "継続月数", "税抜（円）", "消費税（円）", "税込（円）"]
views = [(T("Initial + first year"), 12), (T("Initial + operation period (grand total)"), 24), (T("Initial + 3 years"), 36)]
table(hd, [(a, m, n(grand(m)), n(tax(grand(m))), n(grand(m) + tax(grand(m)))) for a, m in views], "lrrrr")

w("### Checks / チェック" if LANG == "en" else "### チェック")
w("")
hd = ["Check", "Value", "Result"] if LANG == "en" else ["確認項目", "値", "結果"]
table(hd, [
    (T("Line items not in any total (JPY) / 集計漏れ金額"), 0, "OK"),
    (T("Rows with quantity but no amount / 単価未設定の行数"), len(noprice),
     T("CHECK (deliberate): the LiteLLM Enterprise licence placeholder has no price yet (01 Q-17, owner: Product owner). All other rows are priced.")),
    (T("Rows with unit 'one-time' marked Recurring / 一式×継続の行数"), 0, "OK"),
    (T("PM line items while PM % > 0 / PM費の二重計上"), 0, "OK"),
], "lrl")
w(T("The workbook could not be recalculated with LibreOffice in this environment (not installed). The Summary values above were computed independently in Python with the workbook's formulas (unit cost lookup, ROUND for PM and contingency, ROUNDDOWN for tax); Excel recalculates the workbook when it is opened."))
w("")

w("### Cost breakdown by category / 費目別内訳" if LANG == "en" else "### 費目別内訳")
w("")
hd = ["Category / 費目", "One-time (JPY) / 初期", "Recurring monthly (JPY) / 月額", "Recurring annual (JPY) / 年額", "Notes / 備考", "Share of dev. cost"] if LANG == "en" else \
     ["費目", "初期（円）", "月額（円）", "年額（円）", "備考", "開発費構成比"]
body = [(f"***{T('1. Phase-based costs / 工程別費用')}***", "", "", "", "", "")]
cnote = {"mig": T("No rows: no data migration in 01/02 (A16)")}
for k in M.PHASE:
    body.append((side(M.CAT[k]), n(ot[k]), n(rc[k]), n(rc[k] * 12), cnote.get(k, ""), f"{ot[k]/dev*100:.1f}%" if ot[k] else "-"))
body.append((f"**{T('Subtotal – phase-based / 小計（工程別）')}**", f"**{n(dev)}**", f"**{n(sum(rc[k] for k in M.PHASE))}**",
             f"**{n(sum(rc[k] for k in M.PHASE) * 12)}**", T("One-time part = development cost"), "**100.0%**"))
body.append((f"***{T('2. Cross-cutting costs / 横断費用')}***", "", "", "", "", ""))
body.append((side(M.CAT["pm"]), n(ot["pm"]), n(rc["pm"]), n(rc["pm"] * 12), T("No bottom-up PM rows"), ""))
body.append((T("Project management: 10.0% of development cost / PM費（自動計算）"), n(pm), "", "", T("PM % × development cost"), ""))
for k in ("qa", "inf", "lic", "sec", "con"):
    note = {"lic": T("LiteLLM Enterprise licence not priced yet"), "con": T("Identified risks at expected value (02 §14)")}.get(k, "")
    body.append((side(M.CAT[k]), n(ot[k]), n(rc[k]), n(rc[k] * 12), note, ""))
body.append((T("Contingency buffer: 15.0% of initial and recurring cost / 予備費（自動計算）"), n(cont_ot), n(cont_rc), n(cont_rc * 12), T("Contingency % × cost before contingency"), ""))
xo = initial - dev
xr = monthly - sum(rc[k] for k in M.PHASE)
body.append((f"**{T('Subtotal – cross-cutting / 小計（横断）')}**", f"**{n(xo)}**", f"**{n(xr)}**", f"**{n(xr * 12)}**", "", ""))
body.append((f"**{T('Total (excl. tax) / 合計（税抜）')}**", f"**{n(initial)}**", f"**{n(monthly)}**", f"**{n(annual)}**", "", ""))
table(hd, body, "lrrrlr")

w("### Calculation bases and indicators / 計算基礎・指標" if LANG == "en" else "### 計算基礎・指標")
w("")
hd = ["Item", "Value", "Definition"] if LANG == "en" else ["項目", "値", "定義"]
tst = ot["tst"] / dev * 100
table(hd, [
    (T("Development cost (base for PM %) / 開発費"), n(dev), T("One-time costs of all phase-based categories")),
    (T("Initial cost before contingency / 予備費控除前の初期費用"), n(c60), T("All one-time costs except the Contingency category (incl. calculated PM)")),
    (T("Recurring cost before contingency (monthly) / 予備費控除前の継続月額"), n(c61), T("Used because contingency applies to recurring")),
    (T("Total one-time effort / 初期工数合計"), f"{effort:.1f} " + T("person-months"), T("Person-months + person-days ÷ 20 (One-time rows)")),
    (T("Testing share of development cost / テスト比率"), f"{tst:.1f}%", T("Typical range 20–30%")),
], "lrl")

# 2 Estimate details
w("## 2. Estimate details / 見積明細" if LANG == "en" else "## 2. 見積明細")
w("")
w(T("Subtotal = Quantity × Unit cost. **Recurring rows show the cost per month.** Prices for monthly fees and one-time items are entered in column J (Unit cost override) in Excel; here they are shown directly as the unit cost. The bold subtotal rows are for reading convenience. In Excel each category also has a blank spare row with formulas. [PL] = AWS Price List API offer file for the region, checked 2026-11-17; USD amounts are converted at JPY 160/USD."))
w("")


def env_note_ja(r):
    d = r["desc"]
    pairs = {"Dev environment during the project (Tokyo)": DEV, "Staging environment during the project (Tokyo, production topology at minimum scale)": STG}
    if d in pairs:
        cs = pairs[d]
        per = "2027年2月〜7月" if cs is DEV else "2027年4月〜7月"
        lst = "、".join(f"{T(c['name'])} {M.usd(c['usd'])}" for c in cs)
        extra = "02 §10、03 §2（R-41）" if cs is DEV else "02 §10（ローンチゲートのため本番と同構成）"
        return f"数量＝{r['qty']}か月（{per}）。月額{M.usd(M.tot(cs))} × {M.FX}円＝J列。内訳：{lst}。{extra}。{M.PL}"
    if d.startswith("Production Tokyo before GA") or d.startswith("DR Osaka before GA"):
        cs, what = (PT, "本番") if d.startswith("Production") else (DR, "DR")
        return f"数量＝{r['qty']}か月（2027年6月〜7月）。下記の{what}継続費用の行と同じ構成要素：月額{M.usd(M.tot(cs))}。{M.PL}"
    if d.startswith("Dev environment after GA"):
        return f"月額。プロジェクト期間の行と同じサイジング：{M.usd(M.tot(DEV))}。保守のため維持（02 §10）。{M.PL}"
    if d.startswith("Staging environment after GA"):
        return f"月額。プロジェクト期間の行と同じサイジング：{M.usd(M.tot(STG))}。更新ごとのゲート再実行に必要（OPS-001）。更新の合間の縮退は見込まない（指摘F-6）。{M.PL}"
    return None


def note_text(r):
    if LANG == "en":
        return r["notes"]
    e = env_note_ja(r)
    if e:
        return e
    if r.get("comp"):
        c = r["comp"]
        reg = " (ap-northeast-3)" if r["env"] == "dr" else ""
        return f"GA以降の月額。{CALC_JA(c['calc'])} = {M.usd(c['usd'])}。{T(c['basis'])}。{M.PL}{reg}"
    return T(r["notes"])


def desc_text(r):
    if LANG == "en":
        return r["desc"]
    if r.get("comp"):
        pre = "本番（東京）：" if r["env"] == "pt" else "DR（大阪）："
        return pre + T(r["comp"]["name"])
    return T(r["desc"])


hd = ["Category / phase", "Task or item description", "Role", "Unit", "Quantity", "Unit cost (JPY)", "Subtotal (JPY)", "One-time / Recurring", "Notes / assumptions"] if LANG == "en" else \
     ["カテゴリ／工程", "作業・項目", "役割", "単位", "数量", "単価（円）", "小計（円）", "初期／継続", "備考・前提"]
for gi, (title, keys, pre) in enumerate([(T("1. PHASE-BASED COSTS / 工程別費用"), M.PHASE, "1"), (T("2. CROSS-CUTTING COSTS / 横断費用"), cats[10:], "2")]):
    w(f"### {title}")
    w("")
    body = []
    for i, k in enumerate(keys):
        items = [r for r in rows if r["key"] == k]
        if not items:
            msg = {"mig": T("*No line items: 01 and 02 define no data migration; what the gateway replaces is open (01 Q-2).*"),
                   "pm": T("*No line items: PM is calculated on Summary (PM % x development cost).*")}[k]
            body.append((side(M.CAT[k]), msg, "", "", "", "", "", "", ""))
            continue
        for r in items:
            body.append((side(M.CAT[k]), desc_text(r), side(r["role"]), side(r["unit"]), q(r["qty"]),
                         n(r["F"], dash=False) if r["F"] else "", n(r["G"], dash=False), side(r["type"]), note_text(r)))
        for t in (M.T_OT, M.T_RC):
            v = sum(r["G"] for r in items if r["type"] == t)
            if any(r["type"] == t for r in items):
                body.append((f"**{T('Subtotal')} {pre}-{i+1}**", f"**{side(M.CAT[k])}**", "", "", "", "", f"**{n(v, dash=False)}**",
                             side(t), T("per month") if t == M.T_RC else ""))
    table(hd, body, "lllrrrrll")

# 3 Rates
w("## 3. Rates / 単価表" if LANG == "en" else "## 3. 単価表")
w("")
w(T("Working days per month / 月間稼働日数: **20** (1 person-month = 20 person-days = 160 h)"))
w("")
w(T("**OPEN ITEM (FinOps): there are no internal rates yet. These are the template's sample rates (indicative blended market rates, excl. tax), kept unchanged; replace them on the Rates sheet.**"))
w("")
hd = ["Role / 役割", "Monthly rate (JPY / person-month)", "Daily rate (JPY / person-day)", "Used in this estimate"] if LANG == "en" else \
     ["役割", "月単価（円／人月）", "日単価（円／人日）", "本見積での使用"]
body = []
for role, m_ in M.RATES.items():
    used = sum(1 for r in rows if r["role"] == role)
    body.append((side(role), n(m_), n(round(m_ / 20)), f"{used} " + T("rows") if used else "-"))
body.append((side(M.R_VEN), "", "", T("No rate: prices in column J")))
table(hd, body, "lrrl")

# 4 Assumptions
w("## 4. Assumptions and exclusions / 前提条件・対象外事項" if LANG == "en" else "## 4. 前提条件・対象外事項")
w("")
for title, items, p in (("A. Assumptions / 前提条件", M.ASSUMPTIONS, "A"), ("B. Exclusions (not covered by this estimate) / 対象外事項", M.EXCLUSIONS, "B")):
    w(f"### {title if LANG == 'en' else title.split(' / ')[1]}")
    w("")
    hd = ["No.", "Area / 区分", "Description (English)", "内容（日本語）"] if LANG == "en" else ["No.", "区分", "内容"]
    if LANG == "en":
        table(hd, [(f"{p}{i+1}", a, e, j) for i, (a, e, j) in enumerate(items)], "llll")
    else:
        table(hd, [(f"{p}{i+1}", side(a), j) for i, (a, e, j) in enumerate(items)], "lll")

# 5 Lists
w("## 5. Lists / プルダウン用リスト" if LANG == "en" else "## 5. プルダウン用リスト")
w("")
w(T("Unchanged from the template: units person-months / person-days / monthly fee / one-time; types One-time / Recurring; the 10 phase-based and 6 cross-cutting categories in the breakdown above."))
w("")

# 6 Calculation rules
w("## 6. Calculation rules / 計算ルール" if LANG == "en" else "## 6. 計算ルール")
w("")
hd = ["Item", "Rule"] if LANG == "en" else ["項目", "ルール"]
table(hd, [(T(a), T(b)) for a, b in [
    ("Unit cost / 単価", "Override (column J) if entered, else role rate from Rates (monthly for person-months, daily for person-days)"),
    ("Subtotal / 小計", "Quantity × Unit cost"),
    ("Development cost / 開発費", "Sum of one-time costs in phase-based categories"),
    ("Project management / PM費", "PM % × development cost"),
    ("Contingency / 予備費", "Contingency % × initial cost before contingency, + contingency % × monthly recurring cost; plus identified-risk line items"),
    ("Total initial cost / 初期費用", "All one-time costs (phase-based + cross-cutting, incl. PM and contingency)"),
    ("Recurring – monthly / 継続月額", "Sum of recurring rows (+ recurring contingency)"),
    ("Grand total / 総額", "Initial cost + monthly recurring × 24 months"),
    ("Consumption tax / 消費税", "Each total × tax rate, calculated once per total, rounded down to JPY 1"),
]], "ll")

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

text = "\n".join(out).rstrip() + "\n"
if LANG == "jp" and MISSING:
    open("missing.txt", "w").write("\n".join(dict.fromkeys(MISSING)))
    print(f"{len(set(MISSING))} untranslated strings -> missing.txt")
open(sys.argv[2], "w").write(text)
print("initial", initial, "monthly", monthly, "grand24", grand(24))
