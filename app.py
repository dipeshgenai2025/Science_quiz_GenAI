import os
import random
import json
from flask import Flask, request, jsonify, session, send_from_directory
from AWSImgGen import AWSImgGen
from PIL import Image
import shutil
import uuid
import time # New import for timestamp

app = Flask(__name__)
app.secret_key = os.urandom(24)

img_gen = AWSImgGen()

try:
    with open("QuizData_1.txt", "r", encoding="utf-8") as f:
        ORGANS = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print("QuizData_1.txt not found. Please create the file.")
    ORGANS = ["Heart", "Lungs", "Brain", "Kidneys", "Liver"]

if not os.path.exists('static'):
    os.makedirs('static')

def get_new_question():
    correct_answer = random.choice(ORGANS)
    wrong_options = random.sample([o for o in ORGANS if o != correct_answer], 3)
    options = wrong_options + [correct_answer]
    random.shuffle(options)
    
    session['correct_answer'] = correct_answer
    
    return {
        'organ': correct_answer,
        'options': options
    }

@app.route('/')
def index():
    with open('index.html', 'r') as f:
        return f.read()

@app.route('/get_question', methods=['GET'])
def get_question_endpoint():
    question_data = get_new_question()
    
    try:
        # --- FIX: Clean up the old image file if it exists
        if 'previous_image' in session and session['previous_image']:
            old_image_path = os.path.join('static', session['previous_image'])
            if os.path.exists(old_image_path):
                os.remove(old_image_path)
        
        prompt = f"A clear medical illustration of the human {question_data['organ'].lower()}."
        img_gen.PromptGeneration(prompt)
        response = img_gen.InvokeModel()
        image_path = img_gen.ProcessResponse(response)
        
        # --- FIX: Generate a unique filename using UUID
        filename = f"{uuid.uuid4()}.png"
        static_image_path = os.path.join('static', filename)
        shutil.move(image_path, static_image_path)
        
        # --- FIX: Add a unique timestamp as a query parameter to force a refresh
        cache_buster = int(time.time())
        image_url = f"/static/{filename}?t={cache_buster}"
        
        # --- FIX: Store the new filename in the session for cleanup later
        session['previous_image'] = filename

        return jsonify({
            'options': question_data['options'],
            'image_url': image_url
        })

    except Exception as e:
        print(f"Error during image generation: {e}")
        return jsonify({
            'error': "Failed to generate image. Trying again.",
            'options': question_data['options'],
            'image_url': '/static/placeholder.jpg'
        }), 500

@app.route('/check_answer', methods=['POST'])
def check_answer_endpoint():
    data = request.json
    selected_option = data.get('selected_option')
    
    if 'correct_answer' not in session:
        return jsonify({'error': 'No active question. Please get a new question.'}), 400
    
    correct_answer = session.get('correct_answer')
    is_correct = (selected_option == correct_answer)
    
    response = {
        'is_correct': is_correct,
        'correct_answer': correct_answer
    }
    
    return jsonify(response)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
