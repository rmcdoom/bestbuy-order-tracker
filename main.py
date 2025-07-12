from authenticator.auth import GmailAuthenticator
from gmail_manager.label_manager import LabelManager
from gmail_manager.email_manager import EmailManager


def main():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    authenticator = GmailAuthenticator(SCOPES)
    creds = authenticator.authenticate()
    print("Access token:", creds.token)

    label_manager = LabelManager(creds)
    labels = label_manager.list_labels()
    print("Labels:", labels)

    # Find the label ID for "Best Buy Order Confirms"
    label_id = label_manager.get_label_id_by_name("Best Buy Order Confirms")
    
    if label_id:
        email_manager = EmailManager(creds)
        messages = email_manager.get_messages_by_label(label_id)
        print("Messages with 'Best Buy Order Confirms' label:", messages)

        # Fetch and print HTML body for each message
        success_count = 0
        fail_count = 0
        failed_messages = []
        for msg in messages:
            detail = email_manager.get_message_details(msg['id'])
            html_body, success = email_manager.extract_html_body(detail)
            if success:
                success_count += 1
            else:
                fail_count += 1
            # print(f"HTML body for {msg['entry_id']} (ID: {msg['id']}):")
            # print(html_body)
        total = success_count + fail_count
        print(f"\nDecoded successfully: {success_count}/{total} ({(success_count/total)*100:.1f}%)")
        print(f"Failed to decode: {fail_count}/{total} ({(fail_count/total)*100:.1f}%)")

        if failed_messages:
            print("\nFailed messages:")
            for msg in failed_messages:
                print(f"  entry_id: {msg['entry_id']}, id: {msg['id']}, threadId: {msg['threadId']}")

if __name__ == "__main__":
    main()