class VkEvent:
    def __init__(self, type: str, message=None, attachment=None, user_id=None, payload=None):
        self.type = type
        self.message = message
        self.attachment = attachment
        self.user_id = user_id
        self.payload = payload
        self.ext = None
