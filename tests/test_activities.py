"""Tests for the GET /activities endpoint"""

import pytest


def test_get_all_activities(client):
    """
    Test that GET /activities returns all available activities with correct structure.
    
    AAA Pattern:
    - Arrange: Use the client fixture (no additional setup needed)
    - Act: Make a GET request to /activities
    - Assert: Verify status code is 200 and response contains activities
    """
    # Arrange
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Club",
        "Basketball Team",
        "Art Club",
        "Drama Society",
        "Math Club",
        "Science Olympiad"
    ]
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert len(activities) == len(expected_activities)
    for activity_name in expected_activities:
        assert activity_name in activities


def test_activity_has_required_fields(client):
    """
    Test that each activity in the response contains required fields.
    
    AAA Pattern:
    - Arrange: Define the required fields for an activity
    - Act: Make a GET request to /activities
    - Assert: Verify each activity has all required fields
    """
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_name, activity_data in activities.items():
        for field in required_fields:
            assert field in activity_data, f"Field '{field}' missing from {activity_name}"


def test_activities_have_participants_list(client):
    """
    Test that each activity has a participants list (even if initially empty).
    
    AAA Pattern:
    - Arrange: No additional setup needed
    - Act: Make a GET request to /activities
    - Assert: Verify all activities have a participants list
    """
    # Arrange
    # No setup needed
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_name, activity_data in activities.items():
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)
