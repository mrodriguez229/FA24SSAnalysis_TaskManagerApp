from database import create_connection

def add_task(task):
    """
    Adds a new task to the database.

    Parameters:
    task (Task): An instance of the Task class with task details.
    """
    conn = create_connection()  # Connect to the database
    cursor = conn.cursor()  # Create a cursor to execute SQL commands
    
    # Insert the new task into the tasks table
    cursor.execute('''
        INSERT INTO tasks (title, description, due_date, priority, status, category)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (task.title, task.description, task.due_date, task.priority, task.status, task.category))
    
    conn.commit()  # Save the new task in the database
    conn.close()  # Close the connection

def get_tasks():
    """
    Retrieves all tasks from the database, ordered by due date.

    Returns:
    list: A list of all tasks.
    """
    conn = create_connection()  # Connect to the database
    cursor = conn.cursor()  # Create a cursor to execute SQL commands
    
    # Select all tasks ordered by due date
    cursor.execute('SELECT * FROM tasks ORDER BY due_date')
    tasks = cursor.fetchall()  # Fetch all tasks
    
    conn.close()  # Close the connection
    return tasks  # Return the task list

def delete_task(task_id):
    """
    Deletes a task from the database by task ID.

    Parameters:
    task_id (int): The unique identifier of the task.
    """
    conn = create_connection()  # Connect to the database
    cursor = conn.cursor()  # Create a cursor to execute SQL commands
    
    # Delete the task with the given task ID
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    
    conn.commit()  # Save the deletion
    conn.close()  # Close the connection

def update_task(task, task_id):
    """
    Updates a task in the database.

    Parameters:
    task (Task): An instance of the Task class with updated details.
    task_id (int): The unique identifier of the task to update.
    """
    conn = create_connection()  # Connect to the database
    cursor = conn.cursor()  # Create a cursor to execute SQL commands
    
    # Update the task details in the database
    cursor.execute('''
        UPDATE tasks 
        SET title = ?, description = ?, due_date = ?, priority = ?, status = ?, category = ?
        WHERE id = ?
    ''', (task.title, task.description, task.due_date, task.priority, task.status, task.category, task_id))
    
    conn.commit()  # Save the updated task
    conn.close()  # Close the connection

def get_categories():
    """
    Retrieves all distinct task categories from the database.

    Returns:
    list: A list of unique categories.
    """
    conn = create_connection()  # Connect to the database
    cursor = conn.cursor()  # Create a cursor to execute SQL commands
    
    # Select distinct categories
    cursor.execute('SELECT DISTINCT category FROM tasks')
    categories = cursor.fetchall()  # Fetch all unique categories
    
    conn.close()  # Close the connection
    return categories  # Return the category list

def get_tasks_by_status(status):
    """
    Retrieves tasks by their status.

    Parameters:
    status (str): The task status (e.g., 'Completed', 'Pending').

    Returns:
    list: A list of tasks with the given status.
    """
    conn = create_connection()  # Connect to the database
    cursor = conn.cursor()  # Create a cursor to execute SQL commands
    
    # Select tasks with the given status
    cursor.execute("SELECT * FROM tasks WHERE status = ?", (status,))
    tasks = cursor.fetchall()  # Fetch tasks with the matching status
    
    conn.close()  # Close the connection
    return tasks  # Return the task list
