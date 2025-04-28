from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize Firebase Admin SDK
cred = credentials.Certificate("path/to/your-firebase-adminsdk.json")  # Download from Firebase Console
firebase_admin.initialize_app(cred)

# Mock notes data (replace with Firestore or file-based notes)
NOTES = {
    "1": {"subject1": "Notes for Semester 1 Subject 1", "subject2": "Notes for Semester 1 Subject 2"},
    "2": {"subject1": "Notes for Semester 2 Subject 1", "subject2": "Notes for Semester 2 Subject 2"},
    "3": {"subject1": "Notes for Semester 3 Subject 1", "subject2": "Notes for Semester 3 Subject 2"},
    "4": {"subject1": "Notes for Semester 4 Subject 1", "subject2": "Notes for Semester 4 Subject 2"},
}

@app.route("/verify-user", methods=["POST"])
def verify_user():
    id_token = request.json.get("idToken")
    try:
        # Verify Firebase ID token
        decoded_token = auth.verify_id_token(id_token)
        email = decoded_token.get("email")
        # Restrict to @grietcollege.com
        if not email.endswith("@grietcollege.com"):
            return jsonify({"error": "Unauthorized email domain"}), 403
        return jsonify({"email": email, "uid": decoded_token["uid"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@app.route("/set-semester", methods=["POST"])
def set_semester():
    id_token = request.json.get("idToken")
    semester = request.json.get("semester")
    try:
        decoded_token = auth.verify_id_token(id_token)
        email = decoded_token.get("email")
        if not email.endswith("@grietcollege.com"):
            return jsonify({"error": "Unauthorized email domain"}), 403
        # Validate semester (1-8 as example)
        if semester not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            return jsonify({"error": "Invalid semester"}), 400
        # Store semester in Firestore (optional)
        # db = firestore.client()
        # db.collection("users").document(decoded_token["uid"]).set({"semester": semester}, merge=True)
        return jsonify({"message": f"Semester {semester} set successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@app.route("/get-notes", methods=["POST"])
def get_notes():
    id_token = request.json.get("idToken")
    semester = request.json.get("semester")
    try:
        decoded_token = auth.verify_id_token(id_token)
        email = decoded_token.get("email")
        if not email.endswith("@grietcollege.com"):
            return jsonify({"error": "Unauthorized email domain"}), 403
        # Fetch notes for the semester
        notes = NOTES.get(semester, {})
        if not notes:
            return jsonify({"error": "No notes found for this semester"}), 404
        return jsonify({"notes": notes}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == "__main__":
    app.run(debug=True, port=5000)