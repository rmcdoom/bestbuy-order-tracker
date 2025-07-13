from authenticator.auth import GmailAuthenticator
from gmail_manager.label_manager import LabelManager
from gmail_manager.email_manager import EmailManager
from order_tracking.tracker import OrderTracker



def main():

    # Define the scopes required for Gmail API access
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    # Authenticate and get credentials
    print("Authenticating with Gmail...")
    authenticator = GmailAuthenticator(SCOPES)
    creds = authenticator.authenticate()

    if creds is None:
        print("Authentication failed. Exiting program.")
        return

    # Initialize the LabelManager to fetch labels
    print("Fetching labels...")
    label_manager = LabelManager(creds)
    labels = label_manager.list_labels()

    if labels is None:
        print("Fetching labels failed. Exiting program.")
        return

    # Find the label ID for "Best Buy Order Confirms"
    label_id = label_manager.get_label_id_by_name("Best Buy Order Confirms")
    
    if label_id:
        email_manager = EmailManager(creds)
        orders = email_manager.process_label_orders(label_id)
    else:
        print("Label 'Best Buy Order Confirms' not found.")
    
    tracker = OrderTracker(email_manager, label_manager)

    for order in orders:  # orders is a list of parsed order_info dicts
        status = tracker.get_order_status(order['order_number'])
        order['status'] = status
        print(order)

    

if __name__ == "__main__":
    main()