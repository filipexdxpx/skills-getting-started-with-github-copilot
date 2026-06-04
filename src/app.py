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
    "Basketball Team": {
        "description": "Practice and compete in basketball games",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Soccer Club": {
        "description": "Train and play soccer matches",
        "schedule": "Wednesdays and Saturdays, 3:00 PM - 5:00 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "ava@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore painting, drawing, and other visual arts",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act in plays and learn theater skills",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": ["mason@mergington.edu", "charlotte@mergington.edu"]
    },
    "Debate Club": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["ethan@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Tuesdays, 3:00 PM - 4:30 PM",
        "max_participants": 25,
        "participants": ["harper@mergington.edu", "logan@mergington.edu"]
    }
}

students = {
    "michael@mergington.edu": {"name": "Michael Baxter", "grade": "10"},
    "daniel@mergington.edu": {"name": "Daniel Rivera", "grade": "11"},
    "emma@mergington.edu": {"name": "Emma Chen", "grade": "12"},
    "sophia@mergington.edu": {"name": "Sophia Patel", "grade": "11"},
    "john@mergington.edu": {"name": "John Adams", "grade": "10"},
    "olivia@mergington.edu": {"name": "Olivia Lee", "grade": "12"},
    "alex@mergington.edu": {"name": "Alex Carter", "grade": "11"},
    "liam@mergington.edu": {"name": "Liam Brooks", "grade": "10"},
    "ava@mergington.edu": {"name": "Ava Johnson", "grade": "12"},
    "isabella@mergington.edu": {"name": "Isabella Martinez", "grade": "11"},
    "mason@mergington.edu": {"name": "Mason Torres", "grade": "10"},
    "charlotte@mergington.edu": {"name": "Charlotte Kim", "grade": "12"},
    "ethan@mergington.edu": {"name": "Ethan Brown", "grade": "11"},
    "harper@mergington.edu": {"name": "Harper Reed", "grade": "10"},
    "logan@mergington.edu": {"name": "Logan Nguyen", "grade": "12"}
}


def resolve_participant(email: str):
    return {
        "email": email,
        **students.get(email, {"name": "Unknown Student", "grade": "Unknown"})
    }


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return {
        activity_name: {
            "description": details["description"],
            "schedule": details["schedule"],
            "max_participants": details["max_participants"],
            "participants": [resolve_participant(email) for email in details["participants"]]
        }
        for activity_name, details in activities.items()
    }


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, name: str, grade: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    if not name.strip():
        raise HTTPException(status_code=400, detail="Student name is required")

    if not grade.strip():
        raise HTTPException(status_code=400, detail="Student grade is required")

    # Get the specific activity
    activity = activities[activity_name]

    # Check if student is already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
    
    # Check if activity is full
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    activity["participants"].append(email)
    students[email] = {
        "name": name.strip(),
        "grade": grade.strip()
    }
    return {"message": f"Signed up {name.strip()} ({email}, grade {grade.strip()}) for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def remove_participant(activity_name: str, email: str):
    """Remove a participant from an activity."""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found")

    activity["participants"].remove(email)
    return {"message": f"Removed {email} from {activity_name}"}
