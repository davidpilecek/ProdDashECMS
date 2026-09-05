
from services.statistics_service import (
    calculate_production_statistics,
)
from services.statistics_service import (
    calculate_production_statistics,
    calculate_production_unit_statistics,
)

import pytest

def make_segment(
    segment_id,
    start_time,
    run_time,
    mass_total,
):
    return {
        "segmentId": segment_id,
        "prodId": "PROD_001",
        "usrId": "N/A",
        "startTime": start_time,
        "stopTime": start_time,
        "runTime": run_time,
        "massTotal": mass_total,
        "totalInclAdditives": mass_total,

        "add1Total": 0.0,
        "add2Total": 0.0,
        "add3Total": 0.0,
        "add4Total": 0.0,
        "add5Total": 0.0,
    }



segments = [
    make_segment(
        "SEG_1",
        "2026-01-10T08:00:00",
        3600,
        10.0,
    ),
    make_segment(
        "SEG_2",
        "2026-01-10T10:00:00",
        1800,
        5.0,
    ),
    make_segment(
        "SEG_3",
        "2026-01-10T14:00:00",
        7200,
        20.0,
    ),
    make_segment(
        "SEG_4",
        "2026-01-11T08:00:00",
        3600,
        8.0,
    ),
]

def test_segment_statistics():

    segments = [
        make_segment(
            "SEG_1",
            "2026-01-10T08:00:00",
            3600,
            10.0,
        ),
        make_segment(
            "SEG_2",
            "2026-01-10T10:00:00",
            1800,
            5.0,
        ),
    ]

    result = calculate_production_statistics(
        segments,
        "SEG_1",
    )

    assert result["segment"]["tonnes"] == 10.0
    assert result["segment"]["hours"] == 1.0
    assert result["segment"]["rate"] == 10.0

def test_day_statistics():

    segments = [
        make_segment(
            "SEG_1",
            "2026-01-10T08:00:00",
            3600,
            10.0,
        ),
        make_segment(
            "SEG_2",
            "2026-01-10T10:00:00",
            1800,
            5.0,
        ),
        make_segment(
            "SEG_3",
            "2026-01-11T08:00:00",
            7200,
            20.0,
        ),
    ]

    result = calculate_production_statistics(
        segments,
        "SEG_1",
    )

    assert result["day"]["tonnes"] == 15.0
    assert result["day"]["hours"] == 1.5
    assert result["day"]["rate"] == 10.0

def test_month_statistics():

    segments = [
        make_segment(
            "SEG_1",
            "2026-01-10T08:00:00",
            3600,
            10.0,
        ),
        make_segment(
            "SEG_2",
            "2026-01-10T10:00:00",
            1800,
            5.0,
        ),
        make_segment(
            "SEG_3",
            "2026-01-11T08:00:00",
            7200,
            20.0,
        ),
    ]

    result = calculate_production_statistics(
        segments,
        "SEG_1",
    )

    assert result["month"]["tonnes"] == 35.0
    assert result["month"]["hours"] == 3.5
    assert result["month"]["rate"] == 10.0

def test_other_month_is_excluded():

    segments = [
        make_segment(
            "SEG_1",
            "2026-01-10T08:00:00",
            3600,
            10.0,
        ),
        make_segment(
            "SEG_2",
            "2026-01-11T08:00:00",
            3600,
            5.0,
        ),
        make_segment(
            "SEG_3",
            "2026-02-01T08:00:00",
            3600,
            100.0,
        ),
    ]

    result = calculate_production_statistics(
        segments,
        "SEG_1",
    )

    assert result["month"]["tonnes"] == 15.0
    assert result["month"]["hours"] == 2.0
    assert result["month"]["rate"] == 7.5

def test_other_day_is_excluded():

    segments = [
        make_segment(
            "SEG_1",
            "2026-01-10T08:00:00",
            3600,
            10.0,
        ),
        make_segment(
            "SEG_2",
            "2026-01-10T10:00:00",
            1800,
            5.0,
        ),
        make_segment(
            "SEG_3",
            "2026-01-11T08:00:00",
            3600,
            100.0,
        ),
    ]

    result = calculate_production_statistics(
        segments,
        "SEG_1",
    )

    assert result["day"]["tonnes"] == 15.0
    assert result["day"]["hours"] == 1.5

def test_invalid_segment_id():

    segments = [
        make_segment(
            "SEG_1",
            "2026-01-10T08:00:00",
            3600,
            10.0,
        ),
    ]

    with pytest.raises(ValueError):
        calculate_production_statistics(
            segments,
            "DOES_NOT_EXIST",
        )

def test_zero_runtime():

    segments = [
        make_segment(
            "SEG_1",
            "2026-01-10T08:00:00",
            0,
            10.0,
        ),
    ]

    result = calculate_production_statistics(
        segments,
        "SEG_1",
    )

    assert result["segment"]["tonnes"] == 10.0
    assert result["segment"]["hours"] == 0.0
    assert result["segment"]["rate"] == 0.0

def test_production_unit_statistics():

    segments = [
        make_segment(
            "SEG_1",
            "2026-01-10T08:00:00",
            3600,
            10.0,
        ),
        make_segment(
            "SEG_2",
            "2026-01-10T10:00:00",
            1800,
            5.0,
        ),
        make_segment(
            "SEG_3",
            "2026-01-10T12:00:00",
            7200,
            100.0,
        ),
    ]

    segments[0]["prodId"] = "PROD_1"
    segments[1]["prodId"] = "PROD_1"
    segments[2]["prodId"] = "PROD_2"

    segments[0]["totalInclAdditives"] = 10.5
    segments[1]["totalInclAdditives"] = 5.5
    segments[2]["totalInclAdditives"] = 100.0

    result = calculate_production_unit_statistics(
        segments,
        "PROD_1",
    )

    assert result["segmentCount"] == 2
    assert result["mass"] == 15.0
    assert result["hours"] == 1.5
    assert result["rate"] == 10.0
    assert result["totalInclAdditives"] == 16.0

def test_production_unit_additives():

    segments = [
        {
            "segmentId": "SEG_1",
            "prodId": "PROD_1",
            "startTime": "2026-01-10T08:00:00",
            "runTime": 3600,
            "massTotal": 100.0,
            "totalInclAdditives": 105.0,
            "add1Total": 5.0,
            "add2Total": 2.0,
            "add3Total": 0.0,
            "add4Total": 0.0,
            "add5Total": 0.0,
        },
        {
            "segmentId": "SEG_2",
            "prodId": "PROD_1",
            "startTime": "2026-01-10T10:00:00",
            "runTime": 1800,
            "massTotal": 50.0,
            "totalInclAdditives": 53.0,
            "add1Total": 3.0,
            "add2Total": 1.0,
            "add3Total": 0.0,
            "add4Total": 0.0,
            "add5Total": 0.0,
        },
    ]

    result = calculate_production_unit_statistics(
        segments,
        "PROD_1",
    )
    assert result["mass"] == 150.0
    assert result["totalInclAdditives"] == 158.0

    assert result["additives"]["add1"]["mass"] == 8.0
    assert result["additives"]["add2"]["mass"] == 3.0

    assert result["additives"]["add1"]["percent"] == pytest.approx(
    8.0 / 158.0 * 100
)

    assert result["additives"]["add2"]["percent"] == pytest.approx(
        3.0 / 158.0 * 100
    )

    