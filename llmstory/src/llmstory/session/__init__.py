import uuid
from .LLMSession import LLMSession
from typing import Dict

sessions: Dict[str, LLMSession] = {}

def unload_session(session_id: str):
    pass

def cleanup_unused_sessions():
    pass

def get_or_create_session(session_id: str):
    if session_id not in sessions.keys():
        session = LLMSession(session_id)
        sessions[session_id] = session
        return session

    return sessions[session_id]

def create_session() -> LLMSession:
    session_id = str(uuid.uuid4())
    session = LLMSession(session_id)
    sessions[session_id] = session
    return session
    

def get_session(session_id: str):
    if session_id not in sessions.keys():
        raise ValueError(f"session='{session_id}' does not exist")
    
    return sessions[session_id]