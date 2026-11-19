"""Japanese text for the Estimate rows, used by both the Japanese workbook and
the Japanese markdown. T is a snapshot.Translator holding ja.JA."""
import model as M
from ja import calc


def desc(r, T):
    if r.get("comp"):
        return ("本番（東京）：" if r["env"] == "pt" else "DR（大阪）：") + T(r["comp"]["name"])
    return T(r["desc"])


def notes(r, T, PT, DR, DEV, STG):
    if r.get("comp"):
        c = r["comp"]
        reg = " (ap-northeast-3)" if r["env"] == "dr" else ""
        return f"GA以降の月額。{calc(c['calc'])} = {M.usd(c['usd'])}。{T(c['basis'])}。{M.PL}{reg}"
    d = r["desc"]
    if d.startswith("Dev environment during") or d.startswith("Staging environment during"):
        cs = DEV if d.startswith("Dev") else STG
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
    return T(r["notes"])


def translate(rows, T, envs):
    """Copies of the rows with Japanese description and notes."""
    return [dict(r, desc=desc(r, T), notes=notes(r, T, *envs)) for r in rows]
