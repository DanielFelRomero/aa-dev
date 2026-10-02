from __future__ import annotations

from html import escape
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"
REPORT_PATH = REPORT_DIR / "run_report.html"
SOURCE = ROOT / "data/source/customers.csv"
BRONZE = ROOT / "data/bronze/customers_delta"
SILVER = ROOT / "data/silver/customers_delta"
GOLD = ROOT / "data/gold/features.parquet"
MODEL = ROOT / "data/gold/model.joblib"


def exists(path: Path) -> bool:
    return path.exists()


def count_rows(path: Path, delta: bool = False) -> str:
    try:
        if delta:
            from deltalake import DeltaTable
            return f"{len(DeltaTable(str(path)).to_pandas()):,}"
        return f"{len(pd.read_parquet(path)):,}"
    except Exception:
        return "No disponible"


def html_table(df: pd.DataFrame, columns: list[str]) -> str:
    view = df[columns].head(8).copy()
    return view.to_html(index=False, classes="data", border=0)


def status_badge(ok: bool) -> str:
    label = "Disponible" if ok else "Pendiente"
    cls = "ok" if ok else "pending"
    return f'<span class="badge {cls}">{label}</span>'


def bar(label: str, value: float, max_value: float) -> str:
    width = 0 if max_value <= 0 else min(100, value / max_value * 100)
    return (
        f'<div class="bar-row"><span>{escape(label)}</span>'
        f'<div class="bar-track"><div class="bar-fill" style="width:{width:.1f}%"></div></div>'
        f'<strong>{value:.0f}</strong></div>'
    )


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    source_df = pd.read_csv(SOURCE) if SOURCE.exists() else pd.DataFrame()
    gold_df = pd.read_parquet(GOLD) if GOLD.exists() else pd.DataFrame()

    null_rate = float(gold_df.isna().mean().mean()) if not gold_df.empty else 0.0

    drift_shift = None
    drift_flag = None
    if not gold_df.empty and "monthly_spend" in gold_df.columns:
        midpoint = len(gold_df) // 2
        if midpoint:
            reference = gold_df["monthly_spend"].iloc[:midpoint]
            current = gold_df["monthly_spend"].iloc[midpoint:]
            ref_mean = float(reference.mean())
            cur_mean = float(current.mean())
            scale = abs(ref_mean) if abs(ref_mean) > 1e-12 else 1.0
            drift_shift = abs(cur_mean - ref_mean) / scale
            drift_flag = drift_shift >= 0.20

    churn_counts = (
        gold_df["churn"].value_counts().sort_index().to_dict()
        if "churn" in gold_df.columns
        else {}
    )
    max_churn = max(churn_counts.values()) if churn_counts else 0

    layers = [
        ("Fuente", SOURCE.exists(), "CSV"),
        ("Bronze", BRONZE.exists(), "Delta Lake"),
        ("Silver", SILVER.exists(), "Delta Lake"),
        ("Gold", GOLD.exists(), "Parquet"),
        ("Modelo", MODEL.exists(), "Joblib"),
    ]

    layer_cards = "".join(
        f'<div class="layer"><div class="layer-title">{escape(name)}</div>'
        f'<div>{status_badge(ok)}</div><small>{escape(kind)}</small></div>'
        for name, ok, kind in layers
    )

    drift_text = "No disponible"
    if drift_shift is not None:
        drift_text = f"{drift_shift:.3f} " + ("(umbral superado)" if drift_flag else "(bajo umbral)")

    bars = "".join(
        bar(f"Clase {int(k)}", float(v), float(max_churn))
        for k, v in churn_counts.items()
    )

    source_preview = (
        html_table(
            source_df,
            ["customer_id", "age", "monthly_spend", "tenure_months", "support_calls", "churn"],
        )
        if not source_df.empty
        else "<p>No disponible.</p>"
    )

    gold_preview = (
        html_table(
            gold_df,
            ["age", "monthly_spend", "tenure_months", "support_calls", "churn"],
        )
        if not gold_df.empty
        else "<p>No disponible.</p>"
    )

    html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AA Dev — Reporte de ejecución</title>
<style>
body {{ font-family: Inter, system-ui, -apple-system, sans-serif; margin: 0; background:#f5f6f8; color:#20242a; }}
main {{ max-width: 1180px; margin: 0 auto; padding: 36px; }}
h1 {{ margin-bottom: 6px; }}
.muted {{ color:#66707a; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:14px; margin:20px 0; }}
.card, .panel {{ background:white; border:1px solid #dfe3e8; border-radius:10px; padding:18px; box-shadow:0 1px 2px rgba(0,0,0,.03); }}
.metric {{ font-size:28px; font-weight:700; margin-top:8px; }}
.layers {{ display:grid; grid-template-columns:repeat(5,1fr); gap:10px; margin:18px 0; }}
.layer {{ background:white; border:1px solid #dfe3e8; border-radius:8px; padding:14px; text-align:center; }}
.layer-title {{ font-weight:700; margin-bottom:8px; }}
.badge {{ display:inline-block; padding:4px 8px; border-radius:999px; font-size:12px; }}
.ok {{ background:#e7f6ec; color:#176b37; }}
.pending {{ background:#fff4db; color:#8a5a00; }}
.layer small {{ display:block; color:#707985; margin-top:8px; }}
.flow {{ display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin:12px 0 4px; }}
.box {{ background:#eef1f5; border:1px solid #cfd5dc; padding:10px 13px; border-radius:7px; }}
.arrow {{ color:#7b838c; }}
.data {{ width:100%; border-collapse:collapse; font-size:13px; }}
.data th,.data td {{ text-align:left; padding:8px; border-bottom:1px solid #eceff2; }}
.bar-row {{ display:grid; grid-template-columns:80px 1fr 40px; gap:10px; align-items:center; margin:9px 0; }}
.bar-track {{ background:#edf0f3; height:12px; border-radius:6px; overflow:hidden; }}
.bar-fill {{ height:100%; background:#6b7280; }}
@media (max-width:760px) {{ .layers {{ grid-template-columns:1fr 1fr; }} main {{ padding:20px; }} }}
</style>
</head>
<body>
<main>
<h1>AA Dev — Reporte de ejecución</h1>
<p class="muted">Estado generado localmente a partir de los artefactos producidos por la práctica.</p>

<div class="flow">
  <span class="box">Fuente</span><span class="arrow">→</span>
  <span class="box">Bronze</span><span class="arrow">→</span>
  <span class="box">Silver</span><span class="arrow">→</span>
  <span class="box">Gold</span><span class="arrow">→</span>
  <span class="box">ML</span><span class="arrow">→</span>
  <span class="box">Serving</span><span class="arrow">→</span>
  <span class="box">Observabilidad</span>
</div>

<h2>Estado de la arquitectura</h2>
<div class="layers">{layer_cards}</div>

<div class="grid">
  <div class="card"><div class="muted">Registros fuente</div><div class="metric">{len(source_df):,}</div></div>
  <div class="card"><div class="muted">Registros Gold</div><div class="metric">{len(gold_df):,}</div></div>
  <div class="card"><div class="muted">Missingness</div><div class="metric">{null_rate:.2%}</div></div>
  <div class="card"><div class="muted">Mean shift</div><div class="metric">{drift_shift:.3f}</div></div>
</div>

<div class="panel">
<h2>Distribución de la variable objetivo</h2>
{bars or "<p>No disponible.</p>"}
</div>

<div class="panel">
<h2>Observabilidad</h2>
<p><strong>Data drift (monthly_spend):</strong> {escape(drift_text)}</p>
<p class="muted">El indicador no demuestra por sí mismo degradación del rendimiento predictivo.</p>
</div>

<div class="panel">
<h2>Vista de datos fuente</h2>
{source_preview}
</div>

<div class="panel">
<h2>Vista de dataset Gold</h2>
{gold_preview}
</div>

<div class="panel">
<h2>Interpretación</h2>
<p>El reporte constituye una ayuda visual para seguir la práctica. La evidencia debe relacionarse con responsabilidades de componentes, atributos de calidad, restricciones y trade-offs.</p>
</div>
</main>
</body>
</html>
"""
    REPORT_PATH.write_text(html, encoding="utf-8")
    print(f"Reporte generado: {REPORT_PATH}")


if __name__ == "__main__":
    main()
