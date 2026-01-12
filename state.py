# In-memory conversation state
conversations = {}

def create_conversation():
    import uuid
    conv_id = str(uuid.uuid4())
    conversations[conv_id] = {"parts": {}}
    return conv_id

def add_part(conv_id, agent, part):
    if conv_id in conversations:
        conversations[conv_id]["parts"][agent] = part

def get_parts(conv_id):
    return conversations.get(conv_id, {}).get("parts", {})
