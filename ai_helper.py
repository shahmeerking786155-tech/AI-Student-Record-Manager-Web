import os
from dotenv import load_dotenv

load_dotenv()

def _ask_groq(prompt):
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        return "AI is not configured yet. Add GROQ_API_KEY to your .env file. Student records and grade calculations still work."
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        model = os.getenv("GROQ_MODEL", "").strip() or "llama-3.3-70b-versatile"
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a supportive academic assistant. Give constructive, age-appropriate study feedback. Do not make high-stakes decisions about students."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        return f"AI service is currently unavailable. Check your API key, model and internet connection. ({type(exc).__name__})"

def _student_summary(student):
    subjects = student.get("subjects", [])
    marks = student.get("marks", [])
    lines = [f"{s}: {m}/100" for s, m in zip(subjects, marks)]
    return (f"Student: {student.get('name', 'Student')}\n"
            f"Class/Semester: {student.get('class_name', 'Not provided')}\n"
            + "\n".join(lines)
            + f"\nAverage: {student.get('average', 'Not calculated')}%\nGrade: {student.get('grade', 'Not calculated')}")

def analyze_performance(student):
    prompt = ("Review these academic results. Identify stronger areas, subjects to practise, "
              "and 3 practical improvement suggestions. Be encouraging and avoid labeling the student.\n\n"
              + _student_summary(student))
    return _ask_groq(prompt)

def generate_study_tips(student):
    prompt = ("Create a simple, realistic weekly study plan and practical study tips based on these results. "
              "Include short focused sessions and breaks. Be encouraging.\n\n" + _student_summary(student))
    return _ask_groq(prompt)
