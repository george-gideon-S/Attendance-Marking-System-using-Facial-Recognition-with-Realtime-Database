import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Change this as per your own database.
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-attendance-realtime-56b4cd-default-rtdb.firebaseio.com/"
})

ref = db.reference("Students")

data = {
    "5002": 
        {
            "name": "Person 01",
            "major": "CSE",
            "starting_year": 2021,
            "total_attendance": 8,
            "standing": "Excellent",
            "year": 3,
            "last_attendance_time": "2024-01-19 00:54:34"
        },
    "5011": 
        {
            "name": "Person 02",
            "major": "CSE (AI)",
            "starting_year": 2021,
            "total_attendance": 8,
            "standing": "Good",
            "year": 3,
            "last_attendance_time": "2024-01-19 00:54:34"
        },
    "5058": 
        {
            "name": "Person 03",
            "major": "CSE (AI)",
            "starting_year": 2021,
            "total_attendance": 8,
            "standing": "Good",
            "year": 3,
            "last_attendance_time": "2024-01-19 00:54:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)