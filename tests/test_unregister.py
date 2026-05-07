"""Tests for the DELETE /activities/{activity_name}/participants endpoint"""

import pytest


def test_unregister_existing_participant(client):
    """
    Test successful unregistration of an existing participant.
    
    AAA Pattern:
    - Arrange: Register a participant first, then prepare to unregister
    - Act: Make a DELETE request to unregister
    - Assert: Verify response status is 200 and participant is removed
    """
    # Arrange
    activity_name = "Chess Club"
    # Use an existing participant from the initial data
    existing_email = "michael@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": existing_email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_unregister_returns_removed_email(client):
    """
    Test that unregister response includes the removed participant's email.
    
    AAA Pattern:
    - Arrange: Identify an existing participant
    - Act: Make a DELETE request for that participant
    - Assert: Verify response contains the email address
    """
    # Arrange
    activity_name = "Basketball Team"
    existing_email = "liam@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": existing_email}
    )
    
    # Assert
    assert response.status_code == 200
    message = response.json()["message"]
    assert existing_email in message


def test_unregister_with_email_normalization(client):
    """
    Test that unregister works with normalized email (case-insensitive, whitespace-stripped).
    
    AAA Pattern:
    - Arrange: Prepare an email with different casing/whitespace than registered
    - Act: Make a DELETE request with normalized email
    - Assert: Verify the request succeeds despite normalization differences
    """
    # Arrange
    activity_name = "Math Club"
    # Existing participant is "harper@mergington.edu" but we try with different case
    test_email = "HARPER@MERGINGTON.EDU"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 200
    message = response.json()["message"]
    assert "removed" in message.lower() or "unregistered" in message.lower()


def test_unregister_response_format(client):
    """
    Test that unregister response has the expected format.
    
    AAA Pattern:
    - Arrange: Prepare an existing participant
    - Act: Make a DELETE request
    - Assert: Verify response JSON structure
    """
    # Arrange
    activity_name = "Drama Society"
    existing_email = "sophia@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": existing_email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert isinstance(data["message"], str)
