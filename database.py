import sqlite3
from tkinter import messagebox

def create_connection():
    """
    Establishes a connection to the SQLite database.

    Returns:
    sqlite3.Connection: Connection object to interact with the database.
    """
    conn = None
    try:
        conn = sqlite3.connect('tasks.db')  # Connect to the tasks database
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign keys
    except sqlite3.Error as e:
        print(f"Connection Error: {e}")  # Print connection error if it occurs
    return conn

def create_tables():
    """
    Creates the necessary tables in the database if they don't exist.
    """
    conn = create_connection()  # Connect to the database
    cursor = conn.cursor()  # Create a cursor to execute SQL commands

    # Create the tasks table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT NOT NULL,
            priority TEXT,
            status TEXT,
            category TEXT
        )
    ''')
    
    conn.commit()  # Save changes
    conn.close()  # Close the connection

def add_task(title, description, due_date, priority, status, category):
    """
    Adds a new task to the database.

    Parameters:
    title (str): Task title.
    description (str): Task description.
    due_date (str): Task due date.
    priority (str): Task priority.
    status (str): Task status.
    category (str): Task category.
    """
    conn = create_connection()  # Connect to the database
    cursor = conn.cursor()  # Create a cursor to execute SQL commands

    try:
        # Insert the new task into the tasks table
        cursor.execute('''
            INSERT INTO tasks (title, description, due_date, priority, status, category)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, description, due_date, priority, status, category))
        conn.commit()  # Save the new task
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to add the task. Error: {e}")
    finally:
        conn.close()  # Close the connection

def update_task(task_id, title, description, due_date, priority, status, category):
    """
    Updates an existing task in the database.

    Parameters:
    task_id (int): ID of the task to update.
    title (str): Updated task title.
    description (str): Updated task description.
    due_date (str): Updated due date.
    priority (str): Updated task priority.
    status (str): Updated task status.
    category (str): Updated task category.
    """
    conn = create_connection()  # Connect to the database
    cursor = conn.cursor()  # Create a cursor to execute SQL commands

    try:
        # Update the task in the tasks table
        cursor.execute('''
            UPDATE tasks 
            SET title = ?, description = ?, due_date = ?, priority = ?, status = ?, category = ?
            WHERE id = ?
        ''', (title, description, due_date, priority, status, category, task_id))
        conn.commit()  # Save the updated task
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to update the task. Error: {e}")
    finally:
        conn.close()  # Close the connection

def delete_task(task_id):
    """
    Deletes a task by its ID.

    Parameters:
    task_id (int): ID of the task to delete.
    """
    conn = create_connection()  # Connect to the database
    cursor = conn.cursor()  # Create a cursor to execute SQL commands

    try:
        # Delete the task with the given ID
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()  # Save the deletion
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to delete the task. Error: {e}")
    finally:
        conn.close()  # Close the connection

def get_tasks():
    """
    Retrieves all tasks from the database.

    Returns:
    list: A list of tasks.
    """
    conn = create_connection()  # Connect to the database
    cursor = conn.cursor()  # Create a cursor to execute SQL commands
    tasks = []

    try:
        # Fetch all tasks from the tasks table
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()  # Retrieve all tasks
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to fetch tasks. Error: {e}")
    finally:
        conn.close()  # Close the connection

    return tasks  # Return the list of tasks

# Ensure the tasks table is created when the module is loaded
create_tables()
