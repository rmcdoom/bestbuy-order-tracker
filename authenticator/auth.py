import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class GmailAuthenticator:
    def __init__(self, scopes, credentials_path='credentials.json', token_path='token.pickle'):
        self.scopes = scopes
        self.credentials_path = os.path.join(os.path.dirname(__file__), credentials_path)
        self.token_path = os.path.join(os.path.dirname(__file__), token_path)
        self.creds = None

    def load_credentials(self):
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token_file:
                self.creds = pickle.load(token_file)

    def save_credentials(self):
        with open(self.token_path, 'wb') as token_file:
            pickle.dump(self.creds, token_file)

    def authenticate(self):
        try:
            # Load existing credentials if available
            self.load_credentials()

            # If no valid credentials, perform the OAuth flow
            if not self.creds or not self.creds.valid:
                # If the credentials are expired, refresh them
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    try:
                        self.creds.refresh(Request())
                    except Exception as e:
                        print(f"Error refreshing credentials: {e}")
                        self.creds = None
                # If there are no valid credentials, run the OAuth flow
                if not self.creds or not self.creds.valid:
                    try:
                        flow = InstalledAppFlow.from_client_secrets_file(
                            self.credentials_path, self.scopes)
                        self.creds = flow.run_local_server(port=0)
                    except Exception as e:
                        print(f"Error during OAuth flow: {e}")
                        return None
                self.save_credentials()
            return self.creds
        except Exception as e:
            print(f"Authentication failed: {e}")
            return None

if __name__ == "__main__":
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    authenticator = GmailAuthenticator(SCOPES)
    credentials = authenticator.authenticate()
    print(f"Access token: {credentials.token}")