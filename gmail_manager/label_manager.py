from googleapiclient.discovery import build


class LabelManager:
    def __init__(self, creds):
        """
        Initialize the LabelManager with authenticated credentials.
        """
        self.creds = creds
        self.service = build('gmail', 'v1', credentials=self.creds)

    def list_labels(self, user_id='me'):
        """
        Fetches all labels for the specified user.
        Returns a list of label dictionaries.
        """
        try:
            results = self.service.users().labels().list(userId=user_id).execute()
            labels = results.get('labels', [])
            return [{'name': label['name'], 'id': label['id']} for label in labels]
        except Exception as e:
            print(f"An error occurred while fetching labels: {e}")
            return []

    def get_label_id_by_name(self, label_name, user_id='me'):
        """
        Returns the label ID for a given label name, or None if not found.
        """
        labels = self.list_labels(user_id)
        for label in labels:
            if label['name'] == label_name:
                return label['id']
        return None
    