This section will provide a detailed guide on how to install and run the software for the Task Manager Application. These instructions assume that the user has Python installed and is running the application with Visual Studio Code as the IDE for the execution and development.
System Requirements
•	Python Version: Python 3.12 or higher.
•	IDE: Visual Studio Code (recommended for both development and execution).
•	Database: SQLite3 (already included with Python).
•	Dependencies: The application uses libraries such as Tkinter for the graphical user interface and Pillow for image handling.
Installation Steps
Step 1: Clone the repository or download the project files:
•	git clone < https://github.com/mrodriguez229/SDEV265GroupProject_FNM/tree/master >
Step 2: Navigate to the Project Directory
•	 cd path/to/your/project
Step 3: Install Dependencies
•	Install Pillow and tkcalendar.
Install the required libraries:
pip install pillow 
pip install tkcalendar
•	Tkinter
Tkinter is pre-installed with most Python distributions. If you're on Linux and need to install it, use: 
sudo apt-get install python3-tk
Step 4: Database Setup
•	No additional setup is required. The application uses SQLite (tasks.db), and it will create the database automatically if it doesn't exist.
Step 5: Open the Project in Visual Studio Code
•	Set the project folder as your workspace in Visual Studio Code.
Step 6: Run the Application
•	Run the following command in the terminal within Visual Studio Code:
python app.py
This will launch the Task Manager Application, where you can add, view, edit, and delete tasks, adjust settings, and log in/out.
