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
        self.load_credentials()
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.scopes)
                self.creds = flow.run_local_server(port=0)
            self.save_credentials()
        return self.creds

if __name__ == "__main__":
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    authenticator = GmailAuthenticator(SCOPES)
    credentials = authenticator.authenticate()
    print(f"Access token: {credentials.token}")