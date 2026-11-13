from flask import Flask, render_template, request, jsonify
from pathlib import Path
import json
from ai_helper import analyze_performance, generate_study_tips

app = Flask(__name__)
DATA_FILE = Path(__file__).with_name("students.json")

def load_students():
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []

def save_students(students):
    DATA_FILE.write_text(json.dumps(students, indent=2), encoding="utf-8")

def calculate_result(marks):
    total = sum(marks)
    average = total / len(marks) if marks else 0
    if average >= 85: grade = "A"
    elif average >= 70: grade = "B"
    elif average >= 60: grade = "C"
    elif average >= 50: grade = "D"
    else: grade = "F"
    return {"total": total, "average": round(average, 2), "grade": grade}

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/students")
def get_students():
    return jsonify(load_students())

@app.post("/api/students")
def add_student():
    data = request.get_json(silent=True) or {}
    sid = str(data.get("id", "")).strip()
    name = str(data.get("name", "")).strip()
    class_name = str(data.get("class_name", "")).strip()
    subjects = data.get("subjects", [])
    marks = data.get("marks", [])
    if not sid or not name or not class_name:
        return jsonify(error="Student ID, name and class/semester are required."), 400
    if not isinstance(subjects, list) or not isinstance(marks, list) or not subjects or len(subjects) != len(marks):
        return jsonify(error="Enter matching subject names and marks."), 400
    try:
        marks = [float(m) for m in marks]
    except (TypeError, ValueError):
        return jsonify(error="Marks must be numbers."), 400
    if any(m < 0 or m > 100 for m in marks):
        return jsonify(error="Each mark must be between 0 and 100."), 400
    students = load_students()
    if any(s["id"] == sid for s in students):
        return jsonify(error="That Student ID already exists."), 409
    student = {"id": sid, "name": name, "class_name": class_name,
               "subjects": [str(s).strip() for s in subjects], "marks": marks}
    student.update(calculate_result(marks))
    students.append(student)
    save_students(students)
    return jsonify(student), 201

@app.put("/api/students/<sid>")
def update_student(sid):
    data = request.get_json(silent=True) or {}
    students = load_students()
    student = next((s for s in students if s["id"] == sid), None)
    if not student:
        return jsonify(error="Student not found."), 404
    subjects, marks = data.get("subjects", []), data.get("marks", [])
    if not isinstance(subjects, list) or not isinstance(marks, list) or not subjects or len(subjects) != len(marks):
        return jsonify(error="Enter matching subject names and marks."), 400
    try:
        marks = [float(m) for m in marks]
    except (TypeError, ValueError):
        return jsonify(error="Marks must be numbers."), 400
    if any(m < 0 or m > 100 for m in marks):
        return jsonify(error="Each mark must be between 0 and 100."), 400
    student.update({"name": str(data.get("name", "")).strip(),
                    "class_name": str(data.get("class_name", "")).strip(),
                    "subjects": [str(s).strip() for s in subjects], "marks": marks})
    student.update(calculate_result(marks))
    save_students(students)
    return jsonify(student)

@app.delete("/api/students/<sid>")
def delete_student(sid):
    students = load_students()
    updated = [s for s in students if s["id"] != sid]
    if len(updated) == len(students):
        return jsonify(error="Student not found."), 404
    save_students(updated)
    return jsonify(message="Student deleted.")

@app.post("/api/ai/<action>")
def ai_action(action):
    data = request.get_json(silent=True) or {}
    if action not in ("analyze", "tips"):
        return jsonify(error="Unknown AI action."), 404
    result = analyze_performance(data) if action == "analyze" else generate_study_tips(data)
    return jsonify(result=result)

if __name__ == "__main__":
    print("AI Student Record Manager is running!")
    print("Open this link in Chrome: http://127.0.0.1:5000")
    app.run(debug=True)
