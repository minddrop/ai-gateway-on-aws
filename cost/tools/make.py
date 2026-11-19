"""Build the Internal LLM gateway estimate: the English and Japanese workbooks
and markdown snapshots in cost/.

Usage: python make.py [cost_estimate_template.xlsx]

Needs openpyxl (requirements.txt) and a checkout of cost-estimate-template,
whose tools/ do the generic work (see template_tools.py). The template
defaults to the one in that checkout.

For each language: fill a copy of the template (fill.py), check its structure
against the template (check.py), recalculate its Summary from the filled cells
and compare it with the model, and write the markdown (md.py). Exits with
status 1 if a check fails or a Japanese string is missing from ja.py.
"""
import pathlib
import sys

import md
import model as M
import template_tools
from check import recalc, structure
from estimate import compute
from fill import fill
from snapshot import Translator
from ja import JA, RX

OUT = pathlib.Path(__file__).resolve().parents[1]
FILES = {
    "en": ("CostEstimate_InternalLLMGateway_v0.1.xlsx", "cost_estimate_InternalLLMGateway_v0.1.md"),
    "jp": ("CostEstimate_InternalLLMGateway_v0.1_jp.xlsx", "cost_estimate_InternalLLMGateway_v0.1_jp.md"),
}


def main(template):
    failed = []
    for lang, (xlsx, mdfile) in FILES.items():
        T = Translator(lang, JA, RX)
        est, _ = md.estimate(lang, T)
        project = dict(M.PROJECT, name=T(M.PROJECT["name"]), prepared_by=T(M.PROJECT["prepared_by"]))
        fill(template, OUT / xlsx, project, est["items"], est["assumptions"], est["exclusions"],
             params=M.PARAMS, rates=M.RATES, days=M.DAYS)
        failed += [f"{xlsx}: {p}" for p in structure(template, OUT / xlsx)]
        want = compute(est["items"], M.RATES, M.DAYS, M.PARAMS)
        _, got = recalc(OUT / xlsx)
        for k in ("initial", "monthly", "c60", "c61", "effort"):
            if abs(getattr(want, k) - getattr(got, k)) > 0.001:
                failed.append(f"{xlsx}: {k} is {getattr(got, k)} in the workbook, {getattr(want, k)} in the model")
        if got.checks != want.checks:
            failed.append(f"{xlsx}: checks {got.checks} in the workbook, {want.checks} in the model")
        text, missing = md.render(lang)
        (OUT / mdfile).write_text(text)
        failed += [f"{mdfile}: no Japanese for {s!r}" for s in dict.fromkeys(T.missing + missing)]
        print(f"{lang}: {len(est['items'])} line items; initial {got.initial:,.0f}, monthly {got.monthly:,.2f}, "
              f"grand total ({M.PARAMS.months} months) {got.grand():,.0f} excl. tax; checks {got.checks}")
    for f in failed:
        print("FAILED:", f)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else template_tools.TEMPLATE))
