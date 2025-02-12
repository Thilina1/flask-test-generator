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

@app.route('/run_tests', methods=['POST'])
def run_tests():
    try:
        result = subprocess.run(
            ['npx', 'playwright', 'test', 'recorded_test.js'],
            capture_output=True, text=True, check=True
        )
        return jsonify({"output": result.stdout, "error": result.stderr})

    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "message": f"Test execution error: {e.stderr}"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": f"Unexpected error: {str(e)}"}), 500

@app.route('/download_tests', methods=['GET'])
def download_tests():
    if not os.path.exists('test_cases.json'):
        return jsonify({"success": False, "message": "Test cases file not found"}), 404
    return send_file('test_cases.json', as_attachment=True)