# 🧪 Science Quiz GenAI

A GenAI-powered science quiz app that uses AI-generated images and dynamic content to make learning fun and interactive.

## 📦 Prerequisites

- **Visual Studio Code (VS Code)**: A free and powerful code editor  
- **Anaconda**: A robust platform for Python and R, essential for managing environments and dependencies

## ⚙️ Setup Instructions

1. **Create Conda Environment**  
   Open your terminal in VS Code and run:  
   ```bash
   conda create -p quiz_env python==3.10 -y

2. **Activate Environment**  
   ```bash
   conda activate ./quiz_env
   ```

3. **Install Git & Clone Repository**  
   ```bash
   conda install git
   git clone https://github.com/dipeshgenai2025/Science_quiz_GenAI.git
   ```

4. **Install Dependencies**  
   ```bash
   cd Science_quiz_GenAI
   pip install -r requirements.txt
   ```

5. **Configure AWS IAM User**  
   Set up an IAM user in your AWS account with permissions for image generation model.

6. **Run the Application**  
   ```bash
   python QuizMain.py QuizData_1.txt
   ```

7. **Website deployment**
   All the above steps needs to be executed along with,
   ```bash
   $ aws configure
   AWS Access Key ID [None]: XXXXXXXXXXXXXXXXXXXX
   AWS Secret Access Key [None]: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   Default region name [None]: us-east-1
   Default output format [None]: json
   ```
   Start the Flask server with '&'
   ```bash
   Python3 app.py &
   ```
   Ending the command with '&' will keep the server running even with ssh terminal gets closed

## 📁 Project Structure

```
Science_quiz_GenAI/
├── QuizMain.py
├── QuizData_1.txt
├── requirements.txt
└── ...
```

## 📜 License

This project is open-source and available under the MIT License.
