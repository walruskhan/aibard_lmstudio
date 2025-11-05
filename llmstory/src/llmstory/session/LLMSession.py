from contextlib import contextmanager
from datetime import datetime
import threading
from lmstudio import LLM, Chat
from enum import Enum

class RoleType(Enum):
    ASSISTANT = "assistant"
    TOOL = "tool"
    USER = "user"
    SYSTEM = "system"

class LLMSession():
    session_key: str

    lock: threading.Lock = threading.Lock()
    lock_time: datetime = None

    chat: Chat = Chat()
    model_key: str = None
    llm: LLM = None

    def __init__(self, session_key: str):
        self.session_key = session_key
        self.chat = Chat()

    @contextmanager
    def try_lock(self):
        acquired = self.lock.acquire(blocking=False)
        if not acquired:
            # Try grab lock again if lock expired
            if self.lock_time and (datetime.now() - self.lock_time).total_seconds() > 120:
                self.lock.release()
                return self.lock()

            if not acquired:
                yield False
            return
        
        try:
            self.lock_time = datetime.now()
            yield True
        finally:
            self.lock.release()
            self.lock_time = None


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
        self.llm.complete_stream()
        

    

    