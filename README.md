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

4. **Install Dependencies (Also added pip installation, incase not willing to install Python venv)**  
   ```bash
   cd Science_quiz_GenAI
   sudo apt update
   sudo apt-get install pip -y
   pip install -r requirements.txt
   ```

5. **Configure AWS IAM User**  
   Set up an IAM user in your AWS account with permissions for image generation model.

6. **Run the Application**  
   ```bash
   python QuizMain.py QuizData_1.txt
   ```

## ⚙️ Website deployment in AWS (Manual mode)

   All the above steps needs to be executed along with,
   ```bash
   $ sudo apt-get install awscli (Incase awscli in not installed in the AWS EC2 instance)
   $ aws configure
   AWS Access Key ID [None]: XXXXXXXXXXXXXXXXXXXX
   AWS Secret Access Key [None]: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   Default region name [None]: us-east-1
   Default output format [None]: json
   ```

   - **AWS EC2 Deployment**:
     - Launched an EC2 instance (likely Ubuntu).
     - Installed necessary packages: Python, pip, Git
     - Cloned the GitHub repo onto the EC2 instance.
     - Set up a virtual environment and installed dependencies (`requirements.txt`).
     - Ran the app using Flask’s built-in server.
   - **Security & Access**: Configured inbound rules in the EC2 security group to allow HTTP/HTTPS traffic.
   - **Domain & DNS (if applicable)**: Linked a custom domain via Route 53 or updated DNS records.
   
   Start the Flask server with '&'
   ```bash
   Python3 app.py QuizData_1.txt &
   ```
   Ending the command with '&' will keep the server running even with ssh terminal gets closed

## ⚙️ Website deployment in AWS (Added Linux service daemon)
   Added quiz.service to be added to /etc/systemd/system/ directory
   Also, run following commands to add the web service in Linux system daemon list and start the web service
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable quiz.service
   sudo systemctl restart quiz.service
   ```
   Few more help commands
   ```bash
   sudo systemctl start quiz.service
   sudo systemctl status quiz.service
   sudo apt install net-tools
   sudo netstat -tulnp | grep 5000
   sudo journalctl -u quiz.service
   sudo journalctl --vacuum-time=1s
   ```
   Finally run the web site using the public IP address exposed by Amazon EC2
   ```bash
   http://34.239.48.140:5000/
   ```

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
