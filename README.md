Project Setup Guide
This guide will walk you through the necessary steps to set up and run the Science Quiz GenAI application.

Prerequisites
You will need to have the following software installed:

VS Code: A powerful source code editor.

Anaconda: A distribution of Python and R for scientific computing.

Step-by-Step Installation
Install VS Code and Anaconda
If you haven't already, download and install both VS Code and Anaconda from their official websites.

Open a Terminal in VS Code
Open VS Code, then navigate to the terminal by going to Terminal > New Terminal in the menu. This will open a terminal directly within your project workspace.

Create a Conda Environment
Create a dedicated virtual environment for the project to manage its dependencies. This ensures that the project's libraries do not interfere with other Python projects.

conda create -p quiz_env python==3.10 -y

Activate the Environment
Activate the newly created environment. All subsequent commands will be executed within this isolated environment.

conda activate ./quiz_env

Install Git and Clone the Repository
First, install Git within your environment, then clone the project repository from GitHub.

conda install git
git clone https://github.com/dipeshgenai2025/Science_quiz_GenAI.git

Install Project Dependencies
Navigate into the cloned repository's directory and install all the required Python libraries using the requirements.txt file.

cd Science_quiz_GenAI
pip install -r requirements.txt

Create an IAM User in AWS
You will need to set up an IAM user in your Amazon Web Services (AWS) account to grant the application permissions to use the image generation service.

Run the Application
Once all dependencies are installed and your AWS user is configured, you can run the quiz application with the following command, passing QuizData_1.txt as the quiz file.

python QuizMain.py QuizData_1.txt
