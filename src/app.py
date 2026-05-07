"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Club": {
        "description": "Practice teamwork, strategy, and fitness through soccer drills and matches",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 24,
        "participants": ["ava@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Develop skills, coordination, and team play through basketball training",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["liam@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore drawing, painting, and creative expression with different materials",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu", "ethan@mergington.edu"]
    },
    "Drama Society": {
        "description": "Build confidence and creativity through acting, improv, and stage production",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["sophia@mergington.edu", "lucas@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve puzzles, explore problem-solving strategies, and prepare for competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 16,
        "participants": ["harper@mergington.edu", "elijah@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Collaborate on experiments, engineering challenges, and science competitions",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["amelia@mergington.edu", "benjamin@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Normalize email for duplicate checks
    normalized_email = email.strip().lower()
    existing = {p.strip().lower() for p in activity.get("participants", [])}

    # Prevent duplicate registration
    if normalized_email in existing:
        raise HTTPException(status_code=400, detail="Student already registered for this activity")

    # Enforce capacity if provided
    max_participants = activity.get("max_participants")
    if isinstance(max_participants, int) and len(activity.get("participants", [])) >= max_participants:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def unregister_participant(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    # Normalize and search for participant
    normalized_email = email.strip().lower()
    participants = activity.get("participants", [])
    match_index = None
    for i, p in enumerate(participants):
        if p.strip().lower() == normalized_email:
            match_index = i
            break

    if match_index is None:
        raise HTTPException(status_code=404, detail="Participant not found for this activity")

    removed = participants.pop(match_index)
    return {"message": f"Removed {removed} from {activity_name}"}
