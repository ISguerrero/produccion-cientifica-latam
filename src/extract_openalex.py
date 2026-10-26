"""Extracción inicial desde OpenAlex: conteos de obras por año y país.

Uso:
    export OPENALEX_API_KEY="tu_clave"      # gratis en openalex.org/settings/api
    python extract_openalex.py

Guarda un CSV en data/raw/. Es un punto de partida: revisa la documentación
(developers.openalex.org) por si cambian nombres de filtros o costos.
"""
import os
import time
from pathlib import Path

import pandas as pd
import requests

BASE_URL = "https://api.openalex.org/works"
API_KEY = os.environ.get("OPENALEX_API_KEY")

# Colombia y países de comparación (códigos ISO de 2 letras)
COUNTRIES = {"CO": "Colombia", "BR": "Brasil", "MX": "México",
             "AR": "Argentina", "CL": "Chile", "PE": "Perú"}
YEARS = "2000-2025"

OUT_DIR = Path("data/raw")


def get(params: dict, retries: int = 4) -> dict:
    """GET con reintentos y espera exponencial ante 429/5xx."""
    if API_KEY:
        params = {**params, "api_key": API_KEY}
    for attempt in range(retries):
        r = requests.get(BASE_URL, params=params, timeout=60)
        if r.status_code == 200:
            return r.json()
        if r.status_code in (429, 500, 502, 503):
            time.sleep(2 ** attempt)
            continue
        r.raise_for_status()
    raise RuntimeError(f"Falló la consulta tras {retries} intentos: {params}")


def works_by_year(country_code: str) -> pd.DataFrame:
    """Número de obras por año con al menos un autor afiliado al país."""
    data = get({
        "filter": f"authorships.institutions.country_code:{country_code},"
                  f"publication_year:{YEARS},type:article",
        "group_by": "publication_year",
    })
    rows = [{"country_code": country_code,
             "country": COUNTRIES[country_code],
             "year": int(g["key"]),
             "works": g["count"]}
            for g in data["group_by"]]
    return pd.DataFrame(rows)


def main() -> None:
    if not API_KEY:
        print("Aviso: sin OPENALEX_API_KEY el presupuesto diario es mínimo.")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    frames = []
    for code in COUNTRIES:
        frames.append(works_by_year(code))
        time.sleep(0.2)  # cortesía con la API

    df = (pd.concat(frames, ignore_index=True)
            .sort_values(["country_code", "year"]))
    out = OUT_DIR / "works_by_year_country.csv"
    df.to_csv(out, index=False)
    print(f"Guardado {out} ({len(df)} filas)")
    print(df.groupby("country")["works"].sum().sort_values(ascending=False))


if __name__ == "__main__":
    main()
