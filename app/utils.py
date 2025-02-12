import re
import os
import google.generativeai as genai
import json

GEMINI_API_KEY = "AIzaSyBcSZMH1UvTHMhPJqe95ynyMarDZJZcL2M"
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

def generate_user_stories(test_steps):
    if not test_steps:
        return {"error": "No test steps extracted."}

    prompt = f"""
Generate user stories based on the following user actions and inputs.  Treat each distinct 'page.goto', 'page.click', 'page.fill', 'page.locator', 'page.getByRole', etc., as a potential source for a separate user story.  Focus on the user's *specific* goal in performing each action.

Here are a few examples of how to translate actions into user stories:

Actions:
page.goto('https://example.com/products')
page.click('#add-to-cart-button')

User Stories:
{{
  "user_stories": [
    {{
      "title": "Browse Products",
      "description": "As a customer, I want to browse the list of available products so I can find items I'm interested in purchasing."
    }},
    {{
      "title": "Add Product to Cart",
      "description": "As a customer, I want to add a product to my shopping cart so I can purchase it later."
    }}
  ]
}}

Actions:
page.goto('https://flutter.dev/')
page.locator('#get-started__header').click()
page.getByRole('link', {{ name: 'Windows Current device' }}).click()
page.getByRole('link', {{ name: 'Desktop' }}).dblclick()

User Stories:
{{
  "user_stories": [
    {{
      "title": "Visit the Flutter Homepage",
      "description": "As a new user, I want to visit the Flutter homepage so I can learn about the framework and its capabilities."
    }},
    {{
      "title": "Navigate to the Get Started Section",
      "description": "As a user, I want to navigate to the 'Get Started' section from the homepage so I can begin learning how to use Flutter and start the installation process."
    }},
        {{
      "title": "Download Flutter for Windows",
      "description": "As a user, I want to download the Flutter SDK for my Windows device so I can start developing Flutter applications."
    }},
        {{
      "title": "Select Desktop as Target Platform",
      "description": "As a developer, I want to select 'Desktop' as the target platform for my Flutter application so I can build and deploy it on desktop environments."
    }}
  ]
}}

Actions:
{test_steps}

User Stories:
"""

    try:
        model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-01-21")
        response = model.generate_content(prompt)

        if not response.text.strip():
            return {"error": "Empty response from Gemini."}

        try:
            json_match = re.search(r"\{.*\}", response.text, re.DOTALL)  # Improved regex
            if json_match:
                json_text = json_match.group(0)
                user_stories = json.loads(json_text)
                return user_stories
            else:
                return {"error": "Could not extract JSON from the response.", "raw_response": response.text}
        except json.JSONDecodeError:
            return {"error": "Invalid JSON format received.", "raw_response": response.text}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    script_path = "recorded_test.js"  # Replace with your script path
    test_steps = extract_test_steps(script_path)

    if test_steps:
        user_stories = generate_user_stories(test_steps)
        print(json.dumps(user_stories, indent=2))
    else:
        print("No test steps found in the script.")