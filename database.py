import sqlite3
from tkinter import messagebox

def create_connection():
    """
    Establishes a connection to the SQLite database.
    
    Returns:
    sqlite3.Connection: A connection object to interact with the database.
    """
    conn = None  # Database connection object
    try:
        conn = sqlite3.connect('tasks.db')  # Connect to the tasks.db database
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key support
    except sqlite3.Error as e:
        print(e)  # Print the error if connection fails
    return conn  # Return the connection object

def create_tables():
    """
    Creates the necessary tables in the database if they don't already exist.
    """
    conn = create_connection()  # Get the database connection
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    
    # Create the tasks table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            priority TEXT,
            status TEXT,
            category TEXT
        )
    ''')
    
    conn.commit()  # Commit the changes
    conn.close()  # Close the database connection

def add_task(title, description, due_date, priority, status, category):
    """
    Adds a new task to the database.

    Parameters:
    title (str): Title of the task.
    description (str): Description of the task.
    due_date (str): The due date for the task.
    priority (str): Priority level of the task (e.g., High, Medium, Low).
    status (str): Status of the task (e.g., Pending, Completed).
    category (str): The category to which the task belongs.
    """
    conn = create_connection()  # Get the database connection
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    
    try:
        # Insert the new task into the tasks table
        cursor.execute('''
            INSERT INTO tasks (title, description, due_date, priority, status, category)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, description, due_date, priority, status, category))  # Use individual parameters
        
        conn.commit()  # Commit the new task to the database
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to add the task. Error: {e}")  # Display detailed error message
    finally:
        conn.close()  # Close the database connection

def update_task(task_id, title, description, due_date, priority, status, category):
    """
    Updates an existing task in the database.

    Parameters:
    task_id (int): The unique identifier of the task to update.
    title (str): Updated title of the task.
    description (str): Updated description of the task.
    due_date (str): Updated due date for the task.
    priority (str): Updated priority level of the task.
    status (str): Updated status of the task.
    category (str): Updated category of the task.
    """
    conn = create_connection()  # Get the database connection
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    
    try:
        # Update the task in the tasks table
        cursor.execute('''
            UPDATE tasks 
            SET title = ?, description = ?, due_date = ?, priority = ?, status = ?, category = ?
            WHERE id = ?
        ''', (title, description, due_date, priority, status, category, task_id))
        
        conn.commit()  # Commit the updates to the database
    finally:
        conn.close()  # Close the database connection

def delete_task(task_id):
    """
    Deletes a task from the database by task ID.

    Parameters:
    task_id (int): The unique identifier of the task to delete.
    """
    conn = create_connection()  # Get the database connection
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    
    try:
        # Delete the task with the specified task ID
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        
        conn.commit()  # Commit the deletion
    finally:
        conn.close()  # Close the database connection

def get_tasks():
    """
    Retrieves all tasks from the database.

    Returns:
    list: A list of all tasks stored in the database.
    """
    conn = create_connection()  # Get the database connection
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    tasks = []  # List to store fetched tasks
    
    try:
        cursor.execute('SELECT * FROM tasks')  # Select all tasks from the database
        tasks = cursor.fetchall()  # Fetch all task records
    finally:
        conn.close()  # Close the database connection
    
    return tasks  # Return the list of tasks

# Create tables in the database if they don't exist
create_tables()
