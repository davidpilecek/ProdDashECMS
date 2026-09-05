from flask import Blueprint, request

from services.production_service import load_segments
from services.statistics_service import (
    calculate_production_statistics,
)


statistics_bp = Blueprint(
    "statistics",
    __name__,
    url_prefix="/api/production/statistics",
)


@statistics_bp.get("")
def get_production_statistics():

    month = request.args.get(
        "month",
        type=int,
    )

    year = request.args.get(
        "year",
        type=int,
    )

    segment_id = request.args.get(
        "segmentId",
    )

    if month is None or year is None:
        return {
            "error": "month and year are required"
        }, 400

    if segment_id is None:
        return {
            "error": "segmentId is required"
        }, 400

    if month < 1 or month > 12:
        return {
            "error": "month must be between 1 and 12"
        }, 400

    segments = load_segments(
        month,
        year,
    )

    

    if not segments:
        return {
            "error": "No production data available"
        }, 404

    try:

        statistics = calculate_production_statistics(
            segments,
            segment_id,
        )

    except ValueError as error:

        return {
            "error": str(error)
        }, 404

    return statistics