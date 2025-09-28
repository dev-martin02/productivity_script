import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

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
    credential_key = None
    
    # Token file to store user's access and refresh tokens
    token_file = 'token.json'
    
    # Check if we already have valid credentials
    if os.path.exists(token_file):
        credential_key = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in
    if not credential_key or not credential_key.valid:
        if credential_key and credential_key.expired and credential_key.refresh_token:
            credential_key.refresh(Request())
        else:
            # Create credentials.json from environment variables
            if not create_credentials_json():
                print("Error: Google OAuth credentials not found in environment variables.")
                print("Please create a .env file with GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and GOOGLE_PROJECT_ID")
                return None
            
            if not os.path.exists('credentials.json'):
                print("Error: credentials.json not found and could not be created from environment variables.")
                return None
                
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            credential_key = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(credential_key.to_json())
    
    # Build and return the service
    service = build('tasks', 'v1', credentials=credential_key)
    return service
