"""
Backend logic for Gradio multipage UI with authentication
"""
import os
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any

# Authentication credentials
AUTH_USERNAME = "Riemann"
AUTH_PASSWORD = "Derakhshan"

# File to store uploaded files information
UPLOADS_FILE = "uploads.json"
# Directory to store uploaded files
UPLOADS_DIR = "uploads"
# File to store tasks
TASKS_FILE = "tasks.json"
# File to store settings
SETTINGS_FILE = "settings.json"

# Ensure directories exist
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Initialize data files if they don't exist
def initialize_data_files():
    """Initialize data files if they don't exist"""
    if not os.path.exists(UPLOADS_FILE):
        with open(UPLOADS_FILE, "w") as f:
            json.dump([], f)
    
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w") as f:
            json.dump([], f)
    
    if not os.path.exists(SETTINGS_FILE):
        default_settings = {
            "theme": "light",
            "notifications": True,
            "auto_save": True,
            "max_upload_size_mb": 100
        }
        with open(SETTINGS_FILE, "w") as f:
            json.dump(default_settings, f)

initialize_data_files()

# Authentication functions
def authenticate(username: str, password: str) -> bool:
    """
    Authenticate user with username and password
    
    Args:
        username: Username to authenticate
        password: Password to authenticate
        
    Returns:
        bool: True if authentication successful, False otherwise
    """
    return username == AUTH_USERNAME and password == AUTH_PASSWORD

# Upload functions
def save_uploaded_file(file_obj, filename: str) -> str:
    """
    Save uploaded file to uploads directory
    
    Args:
        file_obj: File object to save
        filename: Name of the file
        
    Returns:
        str: Path to saved file
    """
    file_path = os.path.join(UPLOADS_DIR, filename)
    
    # Save the file
    with open(file_path, "wb") as f:
        f.write(file_obj)
    
    # Update uploads.json
    uploads = get_uploads()
    uploads.append({
        "filename": filename,
        "path": file_path,
        "size": os.path.getsize(file_path),
        "upload_date": datetime.now().isoformat(),
    })
    
    with open(UPLOADS_FILE, "w") as f:
        json.dump(uploads, f, indent=2)
    
    return file_path

def get_uploads() -> List[Dict[str, Any]]:
    """
    Get list of uploaded files
    
    Returns:
        List[Dict]: List of uploaded files with metadata
    """
    try:
        with open(UPLOADS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def delete_upload(filename: str) -> bool:
    """
    Delete uploaded file
    
    Args:
        filename: Name of the file to delete
        
    Returns:
        bool: True if deletion successful, False otherwise
    """
    uploads = get_uploads()
    file_path = os.path.join(UPLOADS_DIR, filename)
    
    # Remove file from filesystem
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        return False
    
    # Update uploads.json
    uploads = [upload for upload in uploads if upload["filename"] != filename]
    with open(UPLOADS_FILE, "w") as f:
        json.dump(uploads, f, indent=2)
    
    return True

# Task functions
def get_tasks() -> List[Dict[str, Any]]:
    """
    Get list of tasks
    
    Returns:
        List[Dict]: List of tasks with metadata
    """
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def add_task(title: str, description: str, due_date: Optional[str] = None) -> Dict[str, Any]:
    """
    Add a new task
    
    Args:
        title: Task title
        description: Task description
        due_date: Due date for the task (optional)
        
    Returns:
        Dict: Added task with metadata
    """
    tasks = get_tasks()
    
    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "due_date": due_date,
        "created_at": datetime.now().isoformat(),
        "completed": False
    }
    
    tasks.append(new_task)
    
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)
    
    return new_task

def update_task(task_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Update an existing task
    
    Args:
        task_id: ID of the task to update
        updates: Dictionary of fields to update
        
    Returns:
        Dict: Updated task or None if task not found
    """
    tasks = get_tasks()
    
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks[i].update(updates)
            
            with open(TASKS_FILE, "w") as f:
                json.dump(tasks, f, indent=2)
            
            return tasks[i]
    
    return None

def delete_task(task_id: int) -> bool:
    """
    Delete a task
    
    Args:
        task_id: ID of the task to delete
        
    Returns:
        bool: True if deletion successful, False otherwise
    """
    tasks = get_tasks()
    
    initial_count = len(tasks)
    tasks = [task for task in tasks if task["id"] != task_id]
    
    if len(tasks) < initial_count:
        with open(TASKS_FILE, "w") as f:
            json.dump(tasks, f, indent=2)
        return True
    
    return False

# Settings functions
def get_settings() -> Dict[str, Any]:
    """
    Get application settings
    
    Returns:
        Dict: Application settings
    """
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return default settings if file not found or invalid
        return {
            "theme": "light",
            "notifications": True,
            "auto_save": True,
            "max_upload_size_mb": 100
        }

def update_settings(updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update application settings
    
    Args:
        updates: Dictionary of settings to update
        
    Returns:
        Dict: Updated settings
    """
    settings = get_settings()
    settings.update(updates)
    
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)
    
    return settings
