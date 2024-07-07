import pytest
from flask import Flask
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_search_organizations(client, mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "organizations": [
            {
                "_type": "organization",
                "name": "Test Organization",
                "vertical": "events",
                "parent_id": None,
                "locale": "en_US",
                "created": "2022-01-01T00:00:00Z",
                "image_id": "12345",
                "id": "1234567890123",
            }
        ],
        "pagination": {
            "object_count": 1,
            "continuation": None,
            "page_count": 1,
            "page_size": 50,
            "has_more_items": False,
            "page_number": 1,
        }
    }
    mocker.patch('requests.get', return_value=mock_response)

    response = client.get("/organizations")
    assert response.status_code == 200
    json_data = response.get_json()
    assert "organizations" in json_data
    assert json_data["organizations"][0]["name"] == "Test Organization"

def test_search_events_by_organization(client, mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "pagination": {
            "object_count": 0,
            "page_number": 1,
            "page_size": 50,
            "page_count": 1,
            "has_more_items": False
        },
        "events": [
            {
                "name": {"text": "Test Event"},
                "start": {"local": "2022-01-01T00:00:00"},
                "end": {"local": "2022-01-01T02:00:00"},
                "id": "1",
            }
        ]
    }
    mocker.patch('requests.get', return_value=mock_response)

    response = client.get("/search_by_organization?organization_id=1&status=live")
    assert response.status_code == 200
    json_data = response.get_json()
    assert "events" in json_data
    assert json_data[0]["name"]["text"] == "Test Event"