"""Build cost/CostEstimate_InternalLLMGateway_v0.1.xlsx from the template.

Usage: python build.py <template.xlsx> <out.xlsx> [en|jp]
Never writes to the template. Keeps formulas, validations, named ranges,
styles and sheet protection; rewrites only input blocks on Estimate and
Assumptions and the project/parameter inputs on Summary.
"""
import datetime
import math
import shutil
import sys
from copy import copy

import openpyxl
from openpyxl.worksheet.cell_range import MultiCellRange
from openpyxl.styles.cell_style import StyleArray

import model as M

F_FORMULA = ('=IF(N($J{r})>0,$J{r},IFERROR(IF($D{r}=Unit_PM,INDEX(Role_Monthly,MATCH($C{r},Role_List,0)),'
             'IF($D{r}=Unit_PD,INDEX(Role_Daily,MATCH($C{r},Role_List,0)),"")),""))')
G_FORMULA = '=IFERROR(E{r}*F{r},0)'


def all_rows(lang="en"):
    pt, dr, dev, stg = M.prod_tokyo(), M.dr_osaka(), M.dev_env(), M.stg_env()
    rows = M.labor_rows() + M.infra_rows(pt, dr, dev, stg) + M.risk_rows()
    if lang == "jp":
        import tr
        for r in rows:
            r["desc"], r["notes"] = tr.desc(r), tr.notes(r, pt, dr, dev, stg)
        if tr.MISSING:
            raise SystemExit("untranslated: " + repr(sorted(set(tr.MISSING))))
    return rows, (pt, dr, dev, stg)


def snap(ws, r, cols):
    return {c: (copy(ws.cell(r, c)._style)) for c in cols}


def apply(ws, r, style, cols):
    for c in cols:
        ws.cell(r, c)._style = copy(style[c])


def lines(text, width):
    if not text:
        return 1
    w = sum(2 if ord(ch) > 0x2E80 else 1 for ch in str(text))   # CJK counts double
    return max(1, math.ceil(w / width))


def build_estimate(wb, rows):
    ws = wb["Estimate"]
    cols = range(1, 11)
    st_sec, st_cat, st_item = snap(ws, 6, cols), snap(ws, 7, cols), snap(ws, 8, cols)
    h_sec, h_cat = ws.row_dimensions[6].height, ws.row_dimensions[7].height
    sec1, sec2 = ws["A6"].value, ws["A54"].value
    pm_note, con_note = ws["I56"].value, ws["I80"].value
    last_old = ws.max_row
    for r in range(6, last_old + 1):
        for c in cols:
            cell = ws.cell(r, c)
            cell.value = None
            cell._style = StyleArray()
        ws.row_dimensions[r].height = None

    r = 6
    def put_item(rr, cat, d):
        apply(ws, rr, st_item, cols)
        ws.cell(rr, 1).value = cat
        if d:
            ws.cell(rr, 2).value = d["desc"]
            ws.cell(rr, 3).value = d["role"]
            ws.cell(rr, 4).value = d["unit"]
            ws.cell(rr, 5).value = d["qty"]
            ws.cell(rr, 8).value = d["type"]
            ws.cell(rr, 9).value = d["notes"]
            if d.get("j") is not None:
                ws.cell(rr, 10).value = d["j"]
            n = max(lines(d["desc"], 52), lines(d["notes"], 46))
            ws.row_dimensions[rr].height = max(32, 15 * n + 4)
        else:
            ws.row_dimensions[rr].height = 17.5
        ws.cell(rr, 6).value = F_FORMULA.format(r=rr)
        ws.cell(rr, 7).value = G_FORMULA.format(r=rr)

    for gi, (title, keys, prefix, list_off) in enumerate([
            (sec1, M.PHASE, "1", 5), (sec2, M.CAT_ORDER[10:], "2", 15)]):
        apply(ws, r, st_sec, cols)
        ws.cell(r, 1).value = title
        ws.row_dimensions[r].height = h_sec
        r += 1
        for i, k in enumerate(keys):
            apply(ws, r, st_cat, cols)
            ws.cell(r, 1).value = f'="{prefix}-{i+1}  "&Lists!$A${list_off+i}'
            ws.row_dimensions[r].height = h_cat
            r += 1
            for d in [x for x in rows if x["key"] == k]:
                put_item(r, M.CAT[k], d)
                r += 1
            put_item(r, M.CAT[k], None)          # blank spare row with formulas
            if k == "pm":
                ws.cell(r, 9).value = pm_note
                ws.row_dimensions[r].height = 61
            if k == "con":
                ws.cell(r, 9).value = con_note
                ws.row_dimensions[r].height = 46.5
            r += 1
    last = r - 1
    ws.auto_filter.ref = f"A5:J{last}"
    end = max(280, last + 20)
    for dv in ws.data_validations.dataValidation:
        new = []
        for rng in str(dv.sqref).split():
            a, b = rng.split(":")
            col = "".join(ch for ch in b if ch.isalpha())
            new.append(f"{a}:{col}{end}")
        dv.sqref = MultiCellRange(" ".join(new))
    cf = ws.conditional_formatting
    rules = [(str(rng.sqref), rng.rules) for rng in cf]
    cf._cf_rules.clear()
    for sq, rl in rules:
        parts = []
        for rng in sq.split():
            a, b = rng.split(":")
            col = "".join(ch for ch in b if ch.isalpha())
            parts.append(f"{a}:{col}{end}")
        for rule in rl:
            cf.add(" ".join(parts), rule)
    return last


def build_assumptions(wb):
    ws = wb["Assumptions"]
    cols = range(1, 5)
    st_sec, st_hdr, st_item, st_blank = snap(ws, 4, cols), snap(ws, 5, cols), snap(ws, 6, cols), snap(ws, 19, cols)
    hdr = [ws.cell(5, c).value for c in cols]
    sec_a, sec_b = ws["A4"].value, ws["A20"].value
    h_sec = ws.row_dimensions[4].height
    for r in range(4, ws.max_row + 1):
        for c in cols:
            ws.cell(r, c).value = None
            ws.cell(r, c)._style = StyleArray()
        ws.row_dimensions[r].height = None
    r = 4
    for title, items, pre in ((sec_a, M.ASSUMPTIONS, "A"), (sec_b, M.EXCLUSIONS, "B")):
        apply(ws, r, st_sec, cols); ws.cell(r, 1).value = title; ws.row_dimensions[r].height = h_sec; r += 1
        apply(ws, r, st_hdr, cols)
        for c in cols:
            ws.cell(r, c).value = hdr[c - 1]
        r += 1
        for i, (area, en, ja) in enumerate(items + [("", "", "")]):
            apply(ws, r, st_item, cols)
            ws.cell(r, 1).value = f"{pre}{i+1}"
            if en:
                ws.cell(r, 2).value, ws.cell(r, 3).value, ws.cell(r, 4).value = area, en, ja
                n = max(lines(en, 62), lines(ja, 27), lines(area, 24))
                ws.row_dimensions[r].height = max(32, 15 * n + 4)
            r += 1
        apply(ws, r, st_blank, cols); r += 1
    last = r - 1
    cf = ws.conditional_formatting
    rules = [(str(x.sqref), x.rules) for x in cf]
    cf._cf_rules.clear()
    for sq, rl in rules:
        for rule in rl:
            cf.add(f"B6:D{last + 2}", rule)
    return last


def main(tpl, out, lang="en"):
    shutil.copyfile(tpl, out)
    wb = openpyxl.load_workbook(out)
    s = wb["Summary"]
    s["C5"] = ("社内LLMゲートウェイ（AWS）構築・24か月運用" if lang == "jp"
               else "Internal LLM gateway on AWS (build and 24-month operation)")
    s["C6"] = "v0.1"
    s["C7"] = datetime.datetime(2026, 11, 17)
    s["C8"] = ("Claude（AIアシスタント）、プラットフォームエンジニアリング向け" if lang == "jp"
               else "Claude (AI assistant), for platform engineering")
    s["C9"] = "Draft / 作成中"
    s["C16"] = M.OPS_MONTHS
    rows, _ = all_rows(lang)
    last = build_estimate(wb, rows)
    alast = build_assumptions(wb)
    wb.save(out)
    print("estimate last row", last, "assumptions last row", alast, "line items", len(rows))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "en")
