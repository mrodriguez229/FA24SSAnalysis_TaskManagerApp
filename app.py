from ui import TaskManagerApp

# Entry point of the Task Management application.
# TaskManagerApp is the main class for the UI logic.
try:
    app = TaskManagerApp()
    app.mainloop()
except Exception as e:
    print(f"An error occurred while running the application: {e}")
