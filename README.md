# AI Student Record Manager

A beginner-friendly Flask web application to add, search, update and delete student records, calculate results, and optionally generate AI feedback with Groq.

## Requirements
- Windows, Python 3.10+, and VS Code
- Internet and a Groq API key for AI features (record management works without it)

## Run in VS Code (Windows PowerShell)
Open this folder in VS Code, then run:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt and run `venv\Scripts\activate.bat`.

## Configure optional AI
1. Copy `.env.example` and rename the copy to `.env`.
2. Open `.env` and add your key: `GROQ_API_KEY=your_actual_key`.
3. Keep `.env` private; never upload it or share screenshots containing the key.
4. `GROQ_MODEL` can be left blank to use the default model, or set to a model available in your Groq account.

Get a key from https://console.groq.com/keys.

## Start
```powershell
python app.py
```
Open http://127.0.0.1:5000 in Chrome. Keep the terminal open while using the app. Press `Ctrl+C` to stop.

## Grade scale
- A: 85% or above
- B: 70% to below 85%
- C: 60% to below 70%
- D: 50% to below 60%
- F: below 50%

Student data is saved locally in `students.json`. Back it up regularly.
