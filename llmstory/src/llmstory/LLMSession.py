from lmstudio import LLM, Chat
from enum import Enum

class RoleType(Enum):
    ASSISTANT = "assistant"
    TOOL = "tool"
    USER = "user"
    SYSTEM = "system"

class LLMSession():
    session_key: str

    chat: Chat = Chat()
    model_key: str = None
    llm: LLM = None

    def __init__(self, session_key: str):
        self.session_key = session_key
        self.chat = Chat()

    def set_model(self, model_key: str):
        self.model_key = model_key 
        
    def new_chat(self):
        """Save chat and create a new one"""
        self.chat = Chat()

    def load_chat(self, chat_key: str):
        """Loads an existing chat"""
        self.chat = Chat()

    def compress_chat(self):
        """Summarize chat and create a smaller context"""
        pass

    def append_response(self, role: RoleType, text: str):
        self.chat.add_entry(role.value, text)

    def generate_message(self):
        pass
        

    

    