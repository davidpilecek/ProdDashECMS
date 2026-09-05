from flask import Blueprint, request

from services.production_service import (
    load_production_month,
)


production_bp = Blueprint(
    "production",
    __name__,
    url_prefix="/api/production",
)


@production_bp.get("")
def get_production():

    month = request.args.get(
        "month",
        type=int,
    )

    year = request.args.get(
        "year",
        type=int,
    )

    if month is None or year is None:
        return {
            "error": "month and year are required"
        }, 400

    if month < 1 or month > 12:
        return {
            "error": "month must be between 1 and 12"
        }, 400

    production = load_production_month(
        month,
        year,
    )

    return production