
import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_statistics_endpoint(client, monkeypatch):

    segments = [
        {
            "segmentId": "SEG_1",
            "startTime": "2026-01-10T08:00:00",
            "stopTime": "2026-01-10T09:00:00",
            "runTime": 3600,
            "massTotal": 10.0,
        },
        {
            "segmentId": "SEG_2",
            "startTime": "2026-01-10T10:00:00",
            "stopTime": "2026-01-10T10:30:00",
            "runTime": 1800,
            "massTotal": 5.0,
        },
    ]

    monkeypatch.setattr(
        "routes.statistics.load_segments",
        lambda month, year: segments,
    )

    response = client.get(
        "/api/production/statistics"
        "?month=1"
        "&year=2026"
        "&segmentId=SEG_1"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["segment"]["tonnes"] == 10.0
    assert data["segment"]["hours"] == 1.0
    assert data["segment"]["rate"] == 10.0

    assert data["day"]["tonnes"] == 15.0
    assert data["day"]["hours"] == 1.5
    assert data["day"]["rate"] == 10.0

    assert data["month"]["tonnes"] == 15.0
    assert data["month"]["hours"] == 1.5
    assert data["month"]["rate"] == 10.0

def test_statistics_endpoint_missing_segment_id(client):

    response = client.get(
        "/api/production/statistics"
        "?month=1"
        "&year=2026"
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "segmentId is required"

def test_statistics_endpoint_invalid_month(client):

    response = client.get(
        "/api/production/statistics"
        "?month=13"
        "&year=2026"
        "&segmentId=SEG_1"
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "month must be between 1 and 12"

def test_statistics_endpoint_unknown_segment(
    client,
    monkeypatch,
):

    monkeypatch.setattr(
        "routes.statistics.load_segments",
        lambda month, year: [
            {
                "segmentId": "SEG_1",
                "startTime": "2026-01-10T08:00:00",
                "stopTime": "2026-01-10T09:00:00",
                "runTime": 3600,
                "massTotal": 10.0,
            }
        ],
    )

    response = client.get(
        "/api/production/statistics"
        "?month=1"
        "&year=2026"
        "&segmentId=DOES_NOT_EXIST"
    )

    assert response.status_code == 404