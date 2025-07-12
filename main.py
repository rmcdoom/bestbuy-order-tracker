from gmail.auth import GmailAuthenticator

def main():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    authenticator = GmailAuthenticator(SCOPES)
    creds = authenticator.authenticate()
    print("Access token:", creds.token)

if __name__ == "__main__":
    main()