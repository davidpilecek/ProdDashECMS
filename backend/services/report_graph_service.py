from io import BytesIO
from datetime import datetime

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


AXIS_COLOR = "#8A9199"
SEGMENT_COLOR = "#F2F3F5"
GRID_COLOR = "#CCCCCC"
EDGE_COLOR = "#000000"


def generate_production_graph(
    segments: list[dict],
    month: int,
    year: int,
) -> bytes:

    days_in_month = (
        datetime(year, month + 1, 1)
        - datetime(year, month, 1)
    ).days if month < 12 else (
        datetime(year + 1, 1, 1)
        - datetime(year, 12, 1)
    ).days

    # --------------------------------------------------
    # Prepare daily stacked production
    # --------------------------------------------------

    daily_segments: list[list[dict]] = [
        []
        for _ in range(days_in_month)
    ]

    for segment in segments:

        start_time = datetime.fromisoformat(
            segment["startTime"]
        )

        day = start_time.day

        # Ignore anything outside the selected month.
        if start_time.month != month:
            continue

        if day < 1 or day > days_in_month:
            continue

        daily_segments[day - 1].append(
            segment
        )

    # --------------------------------------------------
    # Create figure
    # --------------------------------------------------

    figure, axis = plt.subplots(
        figsize=(11, 4.4),
        dpi=150,
    )

    # --------------------------------------------------
    # Draw stacked bars
    # --------------------------------------------------

    for day_index, day_segments in enumerate(
        daily_segments
    ):

        bottom = 0.0

        for segment in day_segments:

            mass = segment["massTotal"]

            axis.bar(
                day_index + 1,
                mass,
                bottom=bottom,
                width=0.8,
                color=SEGMENT_COLOR,
                edgecolor=EDGE_COLOR,
                linewidth=1.0,
            )

            bottom += mass

    # --------------------------------------------------
    # X axis
    # --------------------------------------------------

    axis.set_xticks(
        range(1, days_in_month + 1)
    )

    axis.set_xticklabels(
        [
            str(day)
            for day in range(
                1,
                days_in_month + 1,
            )
        ]
    )

    # --------------------------------------------------
    # Labels
    # --------------------------------------------------

    axis.set_xlabel(
        "Day"
    )

    axis.set_ylabel(
        "Mass (t)"
    )

    # --------------------------------------------------
    # Grid
    # --------------------------------------------------

    axis.grid(
        axis="both",
        color=GRID_COLOR,
        alpha=0.2,
        linestyle="--",
        linewidth=0.8,
    )

    axis.set_axisbelow(True)

    # --------------------------------------------------
    # Axis styling
    # --------------------------------------------------

    axis.tick_params(
        colors=AXIS_COLOR
    )

    axis.xaxis.label.set_color(
        AXIS_COLOR
    )

    axis.yaxis.label.set_color(
        AXIS_COLOR
    )

    # --------------------------------------------------
    # Remove unnecessary top/right borders
    # --------------------------------------------------

    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)

    axis.spines["left"].set_color(
        AXIS_COLOR
    )

    axis.spines["bottom"].set_color(
        AXIS_COLOR
    )

    # --------------------------------------------------
    # Export to PNG
    # --------------------------------------------------

    figure.tight_layout()

    buffer = BytesIO()

    figure.savefig(
        buffer,
        format="png",
        bbox_inches="tight",
        facecolor="white",
    )

    plt.close(figure)

    buffer.seek(0)

    return buffer.getvalue()
