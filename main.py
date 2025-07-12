from authenticator.auth import GmailAuthenticator
from label_manager.label_manager import LabelManager


def main():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    authenticator = GmailAuthenticator(SCOPES)
    creds = authenticator.authenticate()
    print("Access token:", creds.token)

    label_manager = LabelManager(creds)
    labels = label_manager.list_labels()
    print("Labels:", labels)

if __name__ == "__main__":
    main()