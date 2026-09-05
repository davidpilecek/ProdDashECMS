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
        "add1SP": _safe_float(row["ADD1_RECIPE_SP"]),
        "add2SP": _safe_float(row["ADD2_RECIPE_SP"]),
        "add3SP": _safe_float(row["ADD3_RECIPE_SP"]),
        "add4SP": _safe_float(row["ADD4_RECIPE_SP"]),
        "add5SP": _safe_float(row["ADD5_RECIPE_SP"]),
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
        "massTotal": _safe_float(row["MASS_TOTAL"]),

        "add1Total": _safe_float(row["ADD1_TOTAL"]),
        "add2Total": _safe_float(row["ADD2_TOTAL"]),
        "add3Total": _safe_float(row["ADD3_TOTAL"]),
        "add4Total": _safe_float(row["ADD4_TOTAL"]),
        "add5Total": _safe_float(row["ADD5_TOTAL"]),

        "totalInclAdditives":
            _safe_float(row["TOTAL_INCL_ADDITIVES"]),

        "add1Percent": _safe_float(row["ADD1_PERCENT"]),
        "add2Percent": _safe_float(row["ADD2_PERCENT"]),
        "add3Percent": _safe_float(row["ADD3_PERCENT"]),
        "add4Percent": _safe_float(row["ADD4_PERCENT"]),
        "add5Percent": _safe_float(row["ADD5_PERCENT"]),
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
        setpoints = [production_unit["add1SP"], production_unit["add2SP"], production_unit["add3SP"], production_unit["add4SP"], production_unit["add5SP"]]

        production_unit["statistics"] = (
            calculate_production_unit_statistics(
                segments,
                production_unit["prodId"],
                setpoints=setpoints
            )
        )

    return {
        "month": month,
        "year": year,
        "segments": segments,
        "productionUnits": production_units,
    }