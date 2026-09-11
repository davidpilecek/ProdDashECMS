import csv
from pathlib import Path

from services.statistics_service import (
    calculate_production_unit_statistics,
)

from path_config import DATA_DIR

def _get_filename(month: int, year: int, suffix: str) -> Path:
    month_string = f"{month:02d}"
    return DATA_DIR / f"{month_string}{year}_{suffix}.csv"

def _parse_production_unit(row: dict) -> dict:
    return {
        "prodId": row["PROD_ID"],
        "prodNum": row["PROD_NUM"],
        "prodDesc": row["PROD_DESC"],
        "recipeName": row["RECIPE_NAME"],
    }

def _safe_float(value):
    if value is None or str(value).strip() == "":
        return None

    return float(value)

def _parse_segment(row: dict) -> dict:
    return {
        "segmentId": row["SEGMENT_ID"],
        "prodId": row["PROD_ID"],
        "usrId": row["USR_ID"],

        "startTime": row["START_TIME"],
        "stopTime": row["STOP_TIME"],

        "runTime": _safe_float(row["RUN_TIME"]),

        "realTotal": _safe_float(row["REAL_TOTAL_PROD"]),
        "realSteam2Cond": _safe_float(row["REAL_STEAM2COND"]),
        "realSteam2Extr": _safe_float(row["REAL_STEAM2EXTR"]),
        "realWater2Cond": _safe_float(row["REAL_WATER2COND"]),
        "realOil2CondExtr": _safe_float(row["REAL_OIL2CONDEXTR"]),
        "realWater2Extr": _safe_float(row["REAL_WATER2EXTR"]),
        "realAdd2CondExtr": _safe_float(row["REAL_ADD2CONDEXTR"]),
        "realAdd5": _safe_float(row["REAL_ADD5"]),
        "realAdd6": _safe_float(row["REAL_ADD6"]),

        "wasteTotal": _safe_float(row["WASTE_TOTAL_PROD"]),
        "wasteSteam2Cond": _safe_float(row["WASTE_STEAM2COND"]),
        "wasteSteam2Extr": _safe_float(row["WASTE_STEAM2EXTR"]),
        "wasteWater2Cond": _safe_float(row["WASTE_WATER2COND"]),
        "wasteOil2CondExtr": _safe_float(row["WASTE_OIL2CONDEXTR"]),
        "wasteWater2Extr": _safe_float(row["WASTE_WATER2EXTR"]),
        "wasteAdd2CondExtr": _safe_float(row["WASTE_ADD2CONDEXTR"]),
        "wasteAdd5": _safe_float(row["WASTE_ADD5"]),
        "wasteAdd6": _safe_float(row["WASTE_ADD6"]),

    
    }

def load_segments(month: int, year: int) -> list[dict]:

    filename = _get_filename(
        month,
        year,
        "PROD_SEGMENT",
    )

    if not filename.exists():
        return []

    with filename.open(
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)
        rows = [_parse_segment(row) for row in reader if row["RUN_TIME"]]

        return rows


def load_production_units(
    month: int,
    year: int,
) -> list[dict]:

    filename = _get_filename(
        month,
        year,
        "PROD_LIST",
    )

    if not filename.exists():
        return []

    with filename.open(
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        return [
            _parse_production_unit(row)
            for row in reader
        ]

def load_production_month(
    month: int,
    year: int,
) -> dict:

    segments = load_segments(month, year)

    production_units = load_production_units(
        month,
        year,
    )

    for production_unit in production_units:

        production_unit["statistics"] = (
            calculate_production_unit_statistics(
                segments = segments,
                prod_id = production_unit["prodId"]
            )
        )

    return {
        "month": month,
        "year": year,
        "segments": segments,
        "productionUnits": production_units,
    }