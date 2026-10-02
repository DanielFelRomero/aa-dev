from pathlib import Path
from html import escape
import duckdb

ROOT=Path(__file__).resolve().parents[1]
GOLD=ROOT/"data/gold/features_delta"
OUT=ROOT/"reports/analytics.html"

def chart(title, labels, values, suffix=""):
    maximum=max(values,default=0) or 1
    items=[]
    for i,(label,value) in enumerate(zip(labels,values)):
        y=40+i*40
        width=340*value/maximum
        items.append(f'<text x="8" y="{y+17}" class="label">{escape(str(label))}</text><rect x="160" y="{y}" width="{width:.1f}" height="23" rx="4" class="bar"/><text x="{170+width:.1f}" y="{y+17}" class="label">{value:.1f}{suffix}</text>')
    return f'<section><h2>{escape(title)}</h2><svg viewBox="0 0 600 {55+40*len(labels)}">{"".join(items)}</svg></section>'

def main():
    if not GOLD.exists():
        raise FileNotFoundError("Run ingestion and transformation first.")
    con=duckdb.connect()
    try:
        con.execute("INSTALL delta")
        con.execute("LOAD delta")
        path=GOLD.as_posix().replace("'","''")
        region=con.execute(f"SELECT region,COUNT(*) AS customers,ROUND(AVG(monthly_spend),1) AS avg_spend,ROUND(AVG(churn)*100,1) AS churn_rate FROM delta_scan('{path}') GROUP BY region ORDER BY region").df()
        tenure=con.execute(f"SELECT CASE WHEN tenure_months<12 THEN '0-11 meses' WHEN tenure_months<36 THEN '12-35 meses' ELSE '36+ meses' END AS tenure_band,COUNT(*) AS customers,ROUND(AVG(churn)*100,1) AS churn_rate FROM delta_scan('{path}') GROUP BY tenure_band ORDER BY MIN(tenure_months)").df()
        total=con.execute(f"SELECT COUNT(*) FROM delta_scan('{path}')").fetchone()[0]
    finally:
        con.close()
    visuals=chart("Clientes por región",region.region.tolist(),region.customers.astype(float).tolist()," clientes")
    visuals+=chart("Tasa de churn por región",region.region.tolist(),region.churn_rate.astype(float).tolist(),"%")
    visuals+=chart("Tasa de churn por antigüedad",tenure.tenure_band.tolist(),tenure.churn_rate.astype(float).tolist(),"%")
    html=f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AA Dev - Consumo analítico</title><style>body{{font-family:system-ui;background:#f4f6f8;color:#20242a;margin:0}}main{{max-width:1000px;margin:auto;padding:30px}}section,.metric{{background:white;border:1px solid #dfe3e8;border-radius:10px;padding:18px;margin:16px 0}}svg{{width:100%;height:auto}}.label{{font-size:14px;fill:#303841}}.bar{{fill:#718096}}table{{border-collapse:collapse;width:100%}}th,td{{padding:9px;text-align:left;border-bottom:1px solid #e8ebef}}.muted{{color:#68727d}}</style></head><body><main><h1>Consumo analítico del Lakehouse</h1><p class="muted">DuckDB consulta directamente Gold en Delta Lake. No se utiliza un Data Warehouse independiente.</p><div class="metric"><strong>Registros analizados: {total:,}</strong></div>{visuals}<section><h2>Resumen por región</h2>{region.to_html(index=False,border=0)}</section><section><h2>Resumen por antigüedad</h2>{tenure.to_html(index=False,border=0)}</section><section><h2>Preguntas de análisis</h2><ul><li>¿Qué diferencias se observan entre regiones?</li><li>¿Qué relación aparece entre antigüedad y churn?</li><li>¿Cuándo bastan consultas directas al Lakehouse y cuándo se justificaría una capa semántica?</li><li>¿Qué límites tiene interpretar datos sintéticos?</li></ul></section></main></body></html>"""
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(html,encoding="utf-8")
    print(f"Analytical report generated: {OUT}")

if __name__=="__main__":
    main()
