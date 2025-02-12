from flask import Flask, render_template, request, jsonify, send_file
import subprocess
import json
import os
from .utils import extract_test_steps, generate_user_stories
from app import app

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_tests', methods=['POST'])
def generate_tests():
    url = request.form.get('url')
    
    if not url:
        return jsonify({"success": False, "message": "URL is required"}), 400

    try:
        result = subprocess.run(
            ['C:\\Program Files\\nodejs\\npx.cmd', 'playwright', 'codegen', url, '-o', 'recorded_test.js'],
            capture_output=True, text=True, check=True
        )

        test_steps = extract_test_steps('recorded_test.js')

        test_cases = generate_user_stories(test_steps)

        with open('test_cases.json', 'w') as f:
            json.dump(test_cases, f, indent=4)

        return jsonify({"success": True, "message": "Test cases generated", "data": test_cases})

    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "message": f"Playwright error: {e.stderr}"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": f"Unexpected error: {str(e)}"}), 500

@app.route('/confirm_user_stories', methods=['POST'])
def confirm_user_stories():
    user_stories = request.json.get('user_stories')
    
    if not user_stories:
        return jsonify({"success": False, "message": "User stories are required"}), 400

    try:
        with open('test_cases.json', 'w') as f:
            json.dump({"user_stories": user_stories}, f, indent=4)
        return jsonify({"success": True, "message": "User stories saved"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Unexpected error: {str(e)}"}), 500

@app.route('/generate_test_cases', methods=['POST'])
def generate_test_cases():
    try:
        with open('test_cases.json', 'r') as f:
            user_stories = json.load(f).get('user_stories', [])

        # Placeholder for converting user stories to test cases
        test_cases = [{"title": story["title"], "test_case": f"Test case for {story['title']}"} for story in user_stories]

        return jsonify({"success": True, "test_cases": test_cases})
    except Exception as e:
        return jsonify({"success": False, "message": f"Unexpected error: {str(e)}"}), 500