from googleapiclient.discovery import build
from order_tracking.parser import parse_order_info
import base64

class EmailManager:
    def __init__(self, creds):
        """
        Initialize the EmailManager with authenticated credentials.
        """
        self.creds = creds
        self.service = build('gmail', 'v1', credentials=self.creds)

    def get_messages_by_label(self, label_id, user_id='me', max_results=100):
        """
        Fetches messages with the specified label ID.
        Returns a list of dicts: [{'id': ..., 'threadId': ...}, ...]
        """
        try:
            response = self.service.users().messages().list(
                userId=user_id,
                labelIds=[label_id],
                maxResults=max_results
            ).execute()
            messages = response.get('messages', [])
            return [
                {
                    'entry_id': f"BestBuy {i+1}",
                    'id': msg['id'], 
                    'threadId': msg['threadId']
                } 
                for i, msg in enumerate(messages)
                ]
        except Exception as e:
            print(f"An error occurred while fetching messages: {e}")
            return []
    
    def get_message_details(self, message_id, user_id='me', format='full'):
        """
        Fetches details of a specific message by its ID.
        Returns a dict with message details.
        """
        try:
            message = self.service.users().messages().get(
                userId=user_id,
                id=message_id,
                format=format
            ).execute()
            return message
        except Exception as e:
            print(f"An error occurred while fetching message details: {e}")
            return None
    
    def extract_html_body(self, message_detail):
        """
        Extracts and decodes the body.data from the 'text/html' part of the message payload.
        Returns the decoded HTML string, or None if not found.
        """
        try:
            payload = message_detail.get('payload', {})
            parts = payload.get('parts', [])
            for part in parts:
                if part.get('mimeType') == 'text/html':
                    data = part.get('body', {}).get('data')
                    if data:
                        # Gmail API encodes body data in URL-safe base64
                        decoded_bytes = base64.urlsafe_b64decode(data.encode('UTF-8'))
                        return decoded_bytes.decode('utf-8'), True
            return None, False
        except Exception as e:
            print(f"An error occurred while extracting HTML body: {e}")
            return None
    
    def process_label_orders(self, label_id):
        """
        Fetches messages for the given label, extracts and parses order info,
        and prints results and stats.
        """
        messages = self.get_messages_by_label(label_id)
        success_count = 0
        fail_count = 0
        failed_messages = []
        for msg in messages:
            detail = self.get_message_details(msg['id'])
            html_body, success = self.extract_html_body(detail)
            if success:
                success_count += 1
                order_info = parse_order_info(html_body)
                print(order_info)
            else:
                fail_count += 1
                failed_messages.append(msg)
        total = success_count + fail_count
        print(f"\nDecoded successfully: {success_count}/{total} ({(success_count/total)*100:.1f}%)")
        print(f"Failed to decode: {fail_count}/{total} ({(fail_count/total)*100:.1f}%)")
        if failed_messages:
            print("\nFailed messages:")
            for msg in failed_messages:
                print(f"  entry_id: {msg['entry_id']}, id: {msg['id']}, threadId: {msg['threadId']}")