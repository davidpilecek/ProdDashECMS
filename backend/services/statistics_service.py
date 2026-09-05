from datetime import datetime

def _build_stats(segments: list[dict]) -> dict:
    if not segments:
        return {
            "tonnes": 0.0,
            "hours": 0.0,
            "rate": 0.0,
        }

    tonnes = sum(
        float(segment["massTotal"])
        for segment in segments
    )

    hours = sum(
        float(segment["runTime"])
        for segment in segments
    ) / 3600

    return {
        "tonnes": tonnes,
        "hours": hours,
        "rate": tonnes / hours if hours > 0 else 0.0,
    }

def calculate_production_statistics(
    segments: list[dict],
    selected_segment_id: str,
) -> dict:

    parsed_segments = [
        (
            segment,
            datetime.fromisoformat(
                segment["startTime"]
            ),
        )
        for segment in segments
    ]

    selected_segment, selected_start_time = next(
        (
            (segment, start_time)
            for segment, start_time in parsed_segments
            if segment["segmentId"] == selected_segment_id
        ),
        (None, None),
    )

    if selected_segment is None or selected_start_time is None:
        raise ValueError(
            f"Segment not found: {selected_segment_id}"
        )

    selected_day = selected_start_time.date()
    selected_month = selected_start_time.month
    selected_year = selected_start_time.year

    day_segments = [
        segment
        for segment, start_time in parsed_segments
        if start_time.date() == selected_day
    ]

    month_segments = [
        segment
        for segment, start_time in parsed_segments
        if (
            start_time.month == selected_month
            and start_time.year == selected_year
        )
    ]

    return {
        "segment": _build_stats(
            [selected_segment]
        ),
        "day": _build_stats(
            day_segments
        ),
        "month": _build_stats(
            month_segments
        ),
    }


def calculate_production_unit_statistics(
    segments: list[dict],
    prod_id: str,
    setpoints: list[float] | None = None,
) -> dict:

    unit_segments = [
        segment
        for segment in segments
        if segment["prodId"] == prod_id
    ]

    if not unit_segments:
        raise ValueError(
            f"Production unit not found: {prod_id}"
        )

    # An open segment has an empty stopTime.
    closed_segments = [
        segment
        for segment in unit_segments
        if segment.get("stopTime")
    ]

    # Start time can still come from an open segment
    start_time = min(
        segment["startTime"]
        for segment in unit_segments
    )

    # If there is an open segment, there is no final stop time yet.
    if any(not segment.get("stopTime") for segment in unit_segments):
        stop_time = None
    else:
        stop_time = max(
            segment["stopTime"]
            for segment in unit_segments
        )

    # Only use completed/closed segments for statistics.
    mass = sum(
        float(segment["massTotal"] or 0)
        for segment in closed_segments
    )

    runtime = sum(
        float(segment["runTime"] or 0)
        for segment in closed_segments
    )

    total_incl_additives = sum(
        float(segment["totalInclAdditives"] or 0)
        for segment in closed_segments
    )

    hours = runtime / 3600

    rate = (
        mass / hours
        if hours > 0
        else 0.0
    )

    additives = {}

    for index in range(1, 6):

        key = f"add{index}Total"

        total = sum(
            float(segment.get(key) or 0)
            for segment in closed_segments
        )

        additives[f"add{index}"] = {
            "mass": total,
            "percent": (
                total / total_incl_additives * 100
                if total_incl_additives > 0
                else 0.0
            ),
            "deviation":(
                abs((total / total_incl_additives * 100) - setpoints[index - 1])
                if total_incl_additives > 0 and setpoints is not None
                else 0.0
            )
        }

    return {
        "segmentCount": len(unit_segments),

        "startTime": start_time,
        "stopTime": stop_time,

        "runTime": runtime,
        "hours": hours,

        "mass": mass,
        "rate": rate,

        "totalInclAdditives": total_incl_additives,

        "additives": additives,
    }