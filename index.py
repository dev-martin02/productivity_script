#!/usr/bin/env python3
import time
from datetime import date
import subprocess
import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create file & folder
def create_folder(folder: str):
    home_directory = os.path.expanduser('~')
    desktop_path = os.path.join(home_directory, 'Desktop', 'study', folder)
    os.makedirs(desktop_path, exist_ok=True)
    return desktop_path

def write_to_file(subject: str, content: str):
    folder_path = create_folder(subject)
    file_name = f'reflection-{date.today()}.txt'
    full_path = os.path.join(folder_path, file_name)
    with open(full_path, 'a') as file:
        file.write(content)

def execute_bash_script(mode: str): 
    try:
        result = subprocess.run(['sudo', "./sitesManager.sh", mode], check=True, capture_output=True, text=True)
        print("Script output:")
        print(result.stdout)
        if result.stderr:
            print("Script errors:")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")
        print(f"Stderr: {e.stderr}")   

# Session functionality
def count_down(subject: str ,session_minutes: int = 0) :
    after_session = ['What did you learn today?', 'How would you rate your performance today? (on scale of 1 to 5)','Why do you think it was like that?', 'What would you do next time?']

    to_seconds = session_minutes * 60 
    remaining_seconds = to_seconds
    execute_bash_script('start')
    while remaining_seconds >= 0:
        minutes = remaining_seconds // 60 # divided and round up the number
        seconds = remaining_seconds % 60 

        timer_display = f"{minutes:02d}:{seconds:02d}"

        print(timer_display, end="\r") # end, will prevent to add a new line, instead it would override the other line

        time.sleep(1)

        remaining_seconds -= 1 

    print('time is up !')
    for questions in after_session:
        response = input(f'{questions} ')
        write_to_file(subject, f"{questions} {response} \n")
    execute_bash_script('end')


# Sound Effect
def bell_notification_sound():
    bell_notification_path = '/home/martin-morel/Desktop/ritual_script/sound/bell-notification.mp3'
    sound_command = ['mpv', "--really-quiet", bell_notification_path]
    with open("/dev/null", 'w') as null_file:
        subprocess.run(sound_command, stdout=null_file, stderr=null_file)

# Google Tasks API Functions
def create_credentials_json():
    """Create credentials.json from environment variables."""
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    project_id = os.getenv('GOOGLE_PROJECT_ID')
    
    if not all([client_id, client_secret, project_id]):
        return False
    
    credentials_data = {
        "installed": {
            "client_id": client_id,
            "project_id": project_id,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": client_secret,
            "redirect_uris": ["http://localhost"]
        }
    }
    
    with open('credentials.json', 'w') as f:
        json.dump(credentials_data, f)
    
    return True

def authenticate_google_tasks():
    """Authenticate and return the Google Tasks API service."""
    SCOPES = ['https://www.googleapis.com/auth/tasks']
    creds = None
    
    # Token file to store user's access and refresh tokens
    token_file = 'token.json'
    
    # Check if we already have valid credentials
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Create credentials.json from environment variables
            if not create_credentials_json():
                print("Error: Google OAuth credentials not found in environment variables.")
                print("Please create a .env file with GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and GOOGLE_PROJECT_ID")
                print("See .env.example for the required format.")
                return None
            
            if not os.path.exists('credentials.json'):
                print("Error: credentials.json not found and could not be created from environment variables.")
                return None
                
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    
    # Build and return the service
    service = build('tasks', 'v1', credentials=creds)
    return service

def get_task_lists(service):
    """Get all task lists from Google Tasks."""
    try:
        results = service.tasklists().list(maxResults=10).execute()
        items = results.get('items', [])
        
        if not items:
            print('No task lists found.')
            return []
        
        print('Task Lists:')
        for item in items:
            print(f"- {item['title']} (ID: {item['id']})")
        
        return items
    except Exception as error:
        print(f'An error occurred: {error}')
        return []

def get_tasks(service, tasklist_id):
    """Get tasks from a specific task list."""
    try:
        results = service.tasks().list(tasklist=tasklist_id).execute()
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

def create_task(service, tasklist_id, title, notes=None):
    """Create a new task in the specified task list."""
    try:
        task = {
            'title': title
        }
        if notes:
            task['notes'] = notes
        
        result = service.tasks().insert(tasklist=tasklist_id, body=task).execute()
        print(f"Task created: {result['title']}")
        return result
    except Exception as error:
        print(f'An error occurred: {error}')
        return None

def demo_google_tasks_api():
    """Demonstrate Google Tasks API functionality."""
    print("\n=== Google Tasks API Demo ===")
    
    # Authenticate
    service = authenticate_google_tasks()
    
    if service is None:
        print("Skipping Google Tasks API demo due to authentication failure.")
        print("=== End of Google Tasks API Demo ===\n")
        return
    
    # Get task lists
    task_lists = get_task_lists(service)
    
    if task_lists:
        # Use the first task list for demo
        first_list = task_lists[0]
        tasklist_id = first_list['id']
        
        print(f"\nUsing task list: {first_list['title']}")
        
        # Get existing tasks
        print("\nExisting tasks:")
        get_tasks(service, tasklist_id)
        
        # Create a new task (optional - commented out to avoid spam)
        # create_task(service, tasklist_id, "Test task from Python script", "Created by ritual script")
    
    print("=== End of Google Tasks API Demo ===\n") 

# Test Google Tasks API
demo_google_tasks_api()

# before the study session
questions = ['What subject would you focus on today?', 'on What exactly you would work on ?', 'How long would you like your session to last?']

subject = ""
focus_on = ""
session_time = 0

for index, question in enumerate(questions):
    if(index == 0):
        subject = input(f"{question} ")
    elif(index == 1):
        focus_on = input(f"{question} ") 
    elif(index == 2):
        session_time = int(input(f"{question} "))

prep_time = 2  # convert to seconds
print('Use this time to prepare your setups and gather all your( resources!')
print('You can press CTRL + C to end this time at anytime')

try :
    while prep_time >= 0 :
        minutes = prep_time // 60 
        seconds = prep_time % 60 
        timer_display = f"{minutes:02d}:{seconds:02d}"

        print(timer_display, end="\r") # end, will prevent to add a new line, instead it would override the other line

        time.sleep(1)

        prep_time -= 1
    
except KeyboardInterrupt:
    print("\nTimer stopped by user.")
    print('\n Blocking websites...')
    # Add any cleanup code here, e.g., closing files, releasing resources
    # sys.exit(0)  # Optional: Explicitly exit the program

count_down(subject, session_time)