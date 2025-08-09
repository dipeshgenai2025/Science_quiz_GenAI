###############################################################################
# Human Organ Quiz UI
#
# Desc: This module defines the HumanOrganQuiz class, which encapsulates a
# Flask-based web application for a human organ quiz. It handles quiz logic,
# image generation from prompts, and serves the web interface.
#
# Author: Dipesh Karmakar
# Date: 07/08/2025
# License: MIT License
###############################################################################

# Import necessary libraries
import os
import sys
import random
import json
import shutil
import uuid
import time
from flask import Flask, request, jsonify, session, send_from_directory
# NOTE: The AWSImgGen class is assumed to be defined in a separate file.
from AWSImgGen import AWSImgGen

class HumanOrganQuiz:
    """
    A class to manage the Human Organ Quiz Flask application.
    This class handles the initialization, routing, and core logic of the quiz.
    """

    def __init__(self, quiz_data_file="QuizData_1.txt"):
        """
        Initializes the HumanOrganQuiz application.

        Args:
            quiz_data_file (str): The name of the text file containing the list of organs.
        """
        # Initialize the Flask application
        self.app = Flask(__name__)
        self.app.secret_key = os.urandom(24)

        # Create an instance of the AWS Image Generation class
        self.img_gen = AWSImgGen()

        # Load the list of human organs from a file
        self.organs = self._load_quiz_data(quiz_data_file)
        
        # Ensure the static directory exists for serving images
        if not os.path.exists('static'):
            os.makedirs('static')

        # Register the routes with the Flask application
        self._register_routes()

    def _load_quiz_data(self, file_path):
        """
        Loads the list of organs from the specified text file.
        If the file is not found, it defaults to a pre-defined list.

        Args:
            file_path (str): The path to the file containing the quiz data.

        Returns:
            list: A list of organ names.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                organs = [line.strip() for line in f if line.strip()]
                return organs if organs else ["Heart", "Lungs", "Brain", "Kidneys", "Liver"]
        except FileNotFoundError:
            print(f"{file_path} not found. Using default organ list.")
            return ["Heart", "Lungs", "Brain", "Kidneys", "Liver"]

    def _register_routes(self):
        """
        Binds the class methods to the Flask application routes.
        """
        self.app.route('/')(self.index)
        self.app.route('/get_question', methods=['GET'])(self.get_question_endpoint)
        self.app.route('/check_answer', methods=['POST'])(self.check_answer_endpoint)
        self.app.route('/static/<path:filename>')(self.serve_static)

    def _get_new_question(self):
        """
        Generates a new quiz question with a correct answer and three incorrect options.

        Returns:
            dict: A dictionary containing the correct organ and a shuffled list of options.
        """
        # Select a correct answer randomly from the list of organs
        correct_answer = random.choice(self.organs)
        
        # Select three other random organs as wrong options
        wrong_options = random.sample([o for o in self.organs if o != correct_answer], 3)
        
        # Combine and shuffle the options
        options = wrong_options + [correct_answer]
        random.shuffle(options)
        
        # Store the correct answer in the user's session
        session['correct_answer'] = correct_answer
        
        return {
            'organ': correct_answer,
            'options': options
        }

    def index(self):
        """
        Renders and serves the main HTML page for the quiz.

        Returns:
            str: The content of the 'index.html' file.
        """
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()

    def get_question_endpoint(self):
        """
        Handles the '/get_question' GET request. It generates a new quiz question,
        uses an image generation model to create an illustration of the correct
        organ, and returns the quiz options and image URL as a JSON response.

        Returns:
            flask.Response: A JSON response with the quiz data or an error message.
        """
        question_data = self._get_new_question()
        
        try:
            # Clean up the old image file if it exists from the previous session
            if 'previous_image' in session and session['previous_image']:
                old_image_path = os.path.join('static', session['previous_image'])
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            
            # Generate a prompt for the image generation model
            prompt = f"A clear medical illustration of the human {question_data['organ'].lower()}."
            self.img_gen.PromptGeneration(prompt)
            
            # Invoke the model to generate the image
            response = self.img_gen.InvokeModel()
            image_path = self.img_gen.ProcessResponse(response)
            
            # Generate a unique filename and move the generated image to the static directory
            filename = f"{uuid.uuid4()}.png"
            static_image_path = os.path.join('static', filename)
            shutil.move(image_path, static_image_path)
            
            # Use a cache-busting query parameter to force the browser to refresh the image
            cache_buster = int(time.time())
            image_url = f"/static/{filename}?t={cache_buster}"
            
            # Store the new filename in the session for future cleanup
            session['previous_image'] = filename

            return jsonify({
                'options': question_data['options'],
                'image_url': image_url
            })

        except Exception as e:
            # Log any errors that occur during image generation
            print(f"Error during image generation: {e}")
            return jsonify({
                'error': "Failed to generate image. Trying again.",
                'options': question_data['options'],
                'image_url': '/static/placeholder.jpg'
            }), 500

    def check_answer_endpoint(self):
        """
        Handles the '/check_answer' POST request. It checks if the selected option
        from the user is the correct answer stored in the session.

        Returns:
            flask.Response: A JSON response indicating if the answer was correct.
        """
        data = request.json
        selected_option = data.get('selected_option')
        
        # Check if there is an active question
        if 'correct_answer' not in session:
            return jsonify({'error': 'No active question. Please get a new question.'}), 400
        
        correct_answer = session.get('correct_answer')
        is_correct = (selected_option == correct_answer)
        
        response = {
            'is_correct': is_correct,
            'correct_answer': correct_answer
        }
        
        return jsonify(response)

    def serve_static(self, filename):
        """
        Serves static files from the 'static' directory.

        Args:
            filename (str): The name of the file to be served.

        Returns:
            flask.Response: The static file content.
        """
        return send_from_directory('static', filename)

    def run(self):
        """
        Starts the Flask development server.
        """
        # The 'debug=False' setting is for production, 'host' and 'port'
        # make the server accessible externally.
        self.app.run(debug=False, host='0.0.0.0', port=5000)

# Entry point of the application
if __name__ == '__main__':
    if len(sys.argv) > 1:
        quiz_file = sys.argv[1]
    else:
        # Fallback to the default hard-coded value if no argument is provided
        quiz_file = "QuizData_1.txt"
    quiz_app = HumanOrganQuiz(quiz_file)
    quiz_app.run()
