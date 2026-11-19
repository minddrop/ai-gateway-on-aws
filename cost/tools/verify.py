"""Structural check of the built workbook against the template, plus an
independent recalculation of Summary (no LibreOffice available)."""
import sys, openpyxl
import model as M

tpl, out = sys.argv[1], sys.argv[2]
a, b = openpyxl.load_workbook(tpl), openpyxl.load_workbook(out)
assert a.sheetnames == b.sheetnames, "sheets"
assert {k: v.attr_text for k, v in a.defined_names.items()} == {k: v.attr_text for k, v in b.defined_names.items()}, "names"
for n in a.sheetnames:
    wa, wb_ = a[n], b[n]
    assert wa.protection.sheet == wb_.protection.sheet, ("protection", n)
    print(n, "protected" if wb_.protection.sheet else "-", "DV:", [(d.type, d.formula1, str(d.sqref)) for d in wb_.data_validations.dataValidation])
# unchanged sheets: every cell formula/value identical
for n in ("Instructions", "Rates", "Lists"):
    for row in a[n].iter_rows():
        for c in row:
            assert b[n][c.coordinate].value == c.value, (n, c.coordinate)
s_a, s_b = a["Summary"], b["Summary"]
changed = [c.coordinate for row in s_a.iter_rows() for c in row if s_b[c.coordinate].value != c.value]
print("Summary changed cells:", changed)
for coord in changed:
    assert s_b[coord].protection.locked is False, ("locked input changed", coord)
# no [Example] left anywhere
for ws in b.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith("[Example]"):
                raise SystemExit(f"[Example] left in {ws.title}!{c.coordinate}")
# formulas on every Estimate item row
e = b["Estimate"]
lists = b["Lists"]
cats = [lists[f"A{r}"].value for r in range(5, 21)]
units = [lists[f"C{r}"].value for r in range(5, 9)]
types = [lists[f"E{r}"].value for r in range(5, 7)]
roles = {b["Rates"][f"A{r}"].value: b["Rates"][f"B{r}"].value for r in range(7, 27) if b["Rates"][f"A{r}"].value}
days = b["Rates"]["B4"].value
items, spare = [], 0
for r in range(6, e.max_row + 1):
    A = e.cell(r, 1).value
    if A in cats:
        assert e.cell(r, 6).value == '=IF(N($J{0})>0,$J{0},IFERROR(IF($D{0}=Unit_PM,INDEX(Role_Monthly,MATCH($C{0},Role_List,0)),IF($D{0}=Unit_PD,INDEX(Role_Daily,MATCH($C{0},Role_List,0)),"")),""))'.format(r), r
        assert e.cell(r, 7).value == f"=IFERROR(E{r}*F{r},0)", r
        assert e.cell(r, 5).protection.locked is False and e.cell(r, 6).protection.locked is True
        if e.cell(r, 2).value is None:
            spare += 1
            continue
        C, D, E, H, J = (e.cell(r, k).value for k in (3, 4, 5, 8, 10))
        assert C in roles or C is None, (r, C); assert D in units, (r, D); assert H in types, (r, H)
        if J:
            F = J
        elif D == units[0]:
            F = roles.get(C) or ""
        elif D == units[1]:
            F = round(roles[C] / days) if roles.get(C) else ""
        else:
            F = ""
        G = E * F if F != "" else 0
        items.append(dict(r=r, cat=A, role=C, unit=D, qty=E, type=H, F=F, G=G, desc=e.cell(r, 2).value, notes=e.cell(r, 9).value))
print("item rows", len(items), "spare rows", spare)
assert spare == 16, "one spare row per category"
s = b["Summary"]
pm, cont, cont_rec, tax, months = s["C12"].value, s["C13"].value, s["C14"].value, s["C15"].value, s["C16"].value
ot = {c: sum(i["G"] for i in items if i["cat"] == c and i["type"] == types[0]) for c in cats}
rc = {c: sum(i["G"] for i in items if i["cat"] == c and i["type"] == types[1]) for c in cats}
dev = sum(ot[c] for c in cats[:10])
pm_amt = round(pm * dev)
c60 = dev + ot[cats[10]] + pm_amt + sum(ot[c] for c in cats[11:15])
c61 = sum(rc[c] for c in cats[:10]) + rc[cats[10]] + sum(rc[c] for c in cats[11:15])
cont_ot = round(cont * c60)
cont_rc = round(cont * c61) if cont_rec == "Yes" else 0
initial = dev + ot[cats[10]] + pm_amt + sum(ot[c] for c in cats[11:16]) + cont_ot
monthly = sum(rc.values()) + cont_rc
import math
def t(x): return math.floor(x * tax)
res = dict(ot=ot, rc=rc, dev=dev, pm=pm_amt, c60=c60, c61=c61, cont_ot=cont_ot, cont_rc=cont_rc,
           initial=initial, monthly=monthly, annual=monthly * 12, months=months, items=items, cats=cats, types=types,
           grand=initial + monthly * months, tax=t,
           effort=sum(i["qty"] for i in items if i["unit"] == units[0] and i["type"] == types[0]) +
                  sum(i["qty"] for i in items if i["unit"] == units[1] and i["type"] == types[0]) / days,
           checks=dict(
               missing=sum(i["G"] for i in items) - (sum(ot.values()) + sum(rc.values())),
               noprice=sum(1 for i in items if i["qty"] not in (None, "") and i["G"] == 0),
               ot_rec=sum(1 for i in items if i["unit"] == units[3] and i["type"] == types[1]),
               pm_dup=1 if (ot[cats[10]] > 0 and pm > 0) else 0))
if __name__ == "__main__":
    for k in ("dev", "pm", "c60", "c61", "cont_ot", "cont_rc", "initial", "monthly", "annual", "grand", "effort"):
        print(f"{k:8} {res[k]:>16,.1f}")
    print("checks", res["checks"])
    print("no-price rows:", [i["desc"][:60] for i in items if i["G"] == 0])
