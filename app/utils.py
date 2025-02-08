import re
import os
import google.generativeai as genai
import json

# Load Gemini API key from environment variables

if not GEMINI_API_KEY:
    raise ValueError("Missing Gemini API Key. Set GEMINI_API_KEY environment variable.")

genai.configure(api_key=GEMINI_API_KEY)

def extract_test_steps(script_path):
    """Extracts Playwright test steps from a script file."""
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            script_content = f.read()
        
        actions = re.findall(r'page\.(goto|click|fill|expect)\(.*?\)', script_content)
        return actions if actions else []
    
    except FileNotFoundError:
        print(f"Error: File '{script_path}' not found.")
        return []

def generate_test_cases(test_steps):
    """Generates structured test cases using Gemini AI."""
    if not test_steps:
        return {"error": "No test steps extracted."}

    prompt = f"""
Generate structured test cases in JSON format based on the following user actions and inputs:

User Actions and Inputs:
{test_steps}

Ensure the output strictly follows this JSON structure:
{{
    "test_cases": [
        {{
            "test_name": "A concise test case name",
            "url": "The URL to visit",
            "steps": [
                "Step 1 description",
                "Step 2 description",
                "Step 3 description"
            ],
            "inputs": [
                {{
                    "element": "Element description (e.g., search field, button, etc.)",
                    "action": "Action performed (e.g., clicked, filled, selected, etc.)",
                    "value": "Value entered or selected (if applicable)"
                }}
            ],
            "expected_result": "A clear expected outcome of the test"
        }}
    ]
}}

Return only valid JSON without any additional text, explanations, or formatting outside of JSON.
"""




    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        if not response.text.strip():
            return {"error": "Empty response from Gemini."}

        print("Raw API Response:", response.text)

        try:
            test_cases = json.loads(response.text)
            return test_cases
        except json.JSONDecodeError:
            return {"error": "Invalid JSON format received.", "raw_response": response.text}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    script_path = "recorded_test.js"  
    test_steps = extract_test_steps(script_path)

    if test_steps:
        test_cases = generate_test_cases(test_steps)
        print(json.dumps(test_cases, indent=2))
    else:
        print("No test steps found in the script.")
