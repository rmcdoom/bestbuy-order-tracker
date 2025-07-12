class OrderTracker:
    def __init__(self, email_manager, label_manager):
        self.email_manager = email_manager
        self.label_manager = label_manager

    def get_order_status(self, order_number):
        # Get label IDs
        tracking_label_id = self.label_manager.get_label_id_by_name("Best Buy Tracking")
        cancel_label_id = self.label_manager.get_label_id_by_name("Best Buy Cancels")

        # Search for tracking email
        tracking_msgs = self.email_manager.search_messages_by_order_number(tracking_label_id, order_number)
        if tracking_msgs:
            return "Shipped"

        # Search for cancel email
        cancel_msgs = self.email_manager.search_messages_by_order_number(cancel_label_id, order_number)
        if cancel_msgs:
            return "Canceled"

        return "Not ready"