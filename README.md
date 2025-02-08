Flask Test Generator Documentation

📌 Overview
The Flask Test Generator is a web application that automates test case generation using Playwright for test recording and Google Gemini API for structured test case generation. It allows users to input a URL, record browser interactions, and generate detailed test cases automatically.

📂 Project Structure
flask-test-generator/
├── app/
│   ├── templates/
│   │   └── index.html
│   ├── static/
│   │   └── style.css
│   ├── __init__.py
│   ├── routes.py
│   └── utils.py
├── test_cases.json
├── recorded_test.js
├── requirements.txt
└── run.py

⚙️ Setup Instructions
1️⃣ Install Dependencies
Ensure you have Python and Node.js installed. Then, run the following commands:
# Create a virtual environment
python -m venv .venv
# Activate the virtual environment
# Windows
.venv\Scripts\activate
# Install Python dependencies
pip install -r requirements.txt
# Install Playwright globally
npm install -g playwright
# Install required browsers
npx playwright install

2️⃣ Set Up Gemini API Key
Obtain an API key from Google AI Studio and set it as an environment variable:
export GEMINI_API_KEY="your-secret-key"
(For Windows PowerShell, use $env:GEMINI_API_KEY="your-secret-key")

3️⃣ Run the Flask App
python run.py
The application will start at: http://127.0.0.1:5000
