"""Tests for the POST /activities/{activity_name}/signup endpoint"""

import pytest


def test_signup_for_activity_success(client):
    """
    Test successful signup for an activity.
    
    AAA Pattern:
    - Arrange: Prepare test data (activity name and email)
    - Act: Make a POST request to signup endpoint
    - Assert: Verify response status is 200 and contains success message
    """
    # Arrange
    activity_name = "Chess Club"
    test_email = "alice@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert test_email in data["message"]
    assert activity_name in data["message"]


def test_signup_with_email_normalization_whitespace(client):
    """
    Test that email signup works with leading/trailing whitespace (normalized).
    
    AAA Pattern:
    - Arrange: Prepare email with extra whitespace
    - Act: Make a POST request with whitespace-padded email
    - Assert: Verify signup is accepted and processed successfully
    """
    # Arrange
    activity_name = "Programming Class"
    test_email_with_spaces = "  bob@mergington.edu  "
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email_with_spaces}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_signup_with_email_normalization_case(client):
    """
    Test that email signup works with mixed case (normalized to lowercase).
    
    AAA Pattern:
    - Arrange: Prepare email with mixed case
    - Act: Make a POST request with mixed-case email
    - Assert: Verify signup is accepted and processed successfully
    """
    # Arrange
    activity_name = "Art Club"
    test_email_uppercase = "CHARLIE@MERGINGTON.EDU"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email_uppercase}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_signup_response_includes_email_and_activity(client):
    """
    Test that signup response includes both the email and activity name.
    
    AAA Pattern:
    - Arrange: Prepare test email and activity
    - Act: Make a POST signup request
    - Assert: Verify response message contains both email and activity name
    """
    # Arrange
    activity_name = "Science Olympiad"
    test_email = "diana@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 200
    message = response.json()["message"]
    assert test_email in message
    assert activity_name in message
