from database import create_connection

def add_task(task):
    """
    Adds a new task to the database.

    Parameters:
    task (Task): An instance of the Task class containing task details.
    """
    conn = create_connection()  # Establish a database connection
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    
    # Insert the new task into the tasks table
    cursor.execute('''
        INSERT INTO tasks (title, description, due_date, priority, status, category)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (task.title, task.description, task.due_date, task.priority, task.status, task.category))
    
    conn.commit()  # Commit the new task to the database
    conn.close()  # Close the database connection

def get_tasks():
    """
    Retrieves all tasks from the database, ordered by their due date.

    Returns:
    list: A list of all tasks from the database.
    """
    conn = create_connection()  # Establish a database connection
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    
    # Select all tasks ordered by their due date
    cursor.execute('SELECT * FROM tasks ORDER BY due_date')
    tasks = cursor.fetchall()  # Fetch all the results
    
    conn.close()  # Close the database connection
    return tasks  # Return the list of tasks

def delete_task(task_id):
    """
    Deletes a task from the database by task ID.

    Parameters:
    task_id (int): The unique identifier of the task to delete.
    """
    conn = create_connection()  # Establish a database connection
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    
    # Delete the task with the specified task ID
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    
    conn.commit()  # Commit the deletion
    conn.close()  # Close the database connection

def update_task(task, task_id):
    """
    Updates an existing task in the database.

    Parameters:
    task (Task): An instance of the Task class containing the updated task details.
    task_id (int): The unique identifier of the task to update.
    """
    conn = create_connection()  # Establish a database connection
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    
    # Update the task details in the tasks table
    cursor.execute('''
        UPDATE tasks 
        SET title = ?, description = ?, due_date = ?, priority = ?, status = ?, category = ?
        WHERE id = ?
    ''', (task.title, task.description, task.due_date, task.priority, task.status, task.category, task_id))
    
    conn.commit()  # Commit the updated task
    conn.close()  # Close the database connection

def get_categories():
    """
    Retrieves all distinct categories from the tasks table.

    Returns:
    list: A list of unique task categories.
    """
    conn = create_connection()  # Establish a database connection
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    
    # Select all distinct categories from the tasks table
    cursor.execute('SELECT DISTINCT category FROM tasks')
    categories = cursor.fetchall()  # Fetch all unique categories
    
    conn.close()  # Close the database connection
    return categories  # Return the list of categories

def get_tasks_by_status(status):
    """
    Retrieves all tasks that match the given status.

    Parameters:
    status (str): The status to filter tasks by (e.g., 'Completed', 'Pending').

    Returns:
    list: A list of tasks that match the given status.
    """
    conn = create_connection()  # Establish a database connection
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    
    # Select all tasks where the status matches the provided status
    cursor.execute("SELECT * FROM tasks WHERE status = ?", (status,))
    tasks = cursor.fetchall()  # Fetch the tasks with the matching status
    
    conn.close()  # Close the database connection
    return tasks  # Return the list of tasks with the given status
