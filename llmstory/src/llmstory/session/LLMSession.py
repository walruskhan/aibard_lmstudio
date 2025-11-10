from contextlib import contextmanager
from datetime import datetime
import os
import threading
from lmstudio import LLM, Chat
from enum import Enum
import lmstudio as lms

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
    prediction_stream = None
    prediction_cancelled = False

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

    def append(self, role: RoleType, text: str):
        self.chat.add_entry(role.value, text)

    async def generate(self):
        with self.try_lock():
            SERVER_API_HOST = os.getenv('LMSTUDIO_API_HOST', 'http://localhost:1234')
            async with lms.AsyncClient(SERVER_API_HOST) as client:
                model = await client.llm.model(self.model_key)
                self.prediction_cancelled = False

                text = ""
                async for fragment in model.respond_stream(self.chat):
                    text += fragment.content

                return text
        return None


    def force_unlock(self):
        if not self.lock.locked and self.lock_time is None:
            return

        try:
            self.lock.release()
            if self.prediction_stream is not None:
                self.prediction_stream.cancel()
                next(self.prediction_stream)

            self.prediction_cancelled = True
        except RuntimeError:
            # Race: lock was released between check and release
            pass
        finally:
            self.lock_time = None


    

    