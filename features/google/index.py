from features.google.auth import authenticate_google_tasks

service_key = authenticate_google_tasks()

def get_task_lists():
    """Get all task lists from Google Tasks."""
    try:
        results = service_key.tasklists().list(maxResults=10).execute()
        items = results.get('items', [])
        
        if not items:
            print('No task lists found.')
            return []
        
        return items
    except Exception as error:
        print(f'An error occurred: {error}')
        return []

def get_tasks():
    """Get tasks from a specific task list."""

 # Get task lists
    task_lists = get_task_lists()
    
    list_id = None
    if task_lists:
        # Use the first task list for demo
        school_index = None

        for task_list in task_lists:
            if task_list['title'] == "School":
                school_index = task_lists.index(task_list)
                break

        if school_index is None:
            print("School list not found")
            return
        
        school_list = task_lists[school_index]
        list_id = school_list['id'] 

    try:
        results = service_key.tasks().list(tasklist=list_id).execute()
        items = results.get('items', [])
        
        if not items:
            print('No tasks found.')
            return []
        
        print('Tasks:')
        for item in items:
            title = item['title']
            status = item.get('status', 'needsAction')
            print(f"- {title} (Status: {status})")
        
        return items
    except Exception as error:
        print(f'An error occurred: {error}')
        return []
