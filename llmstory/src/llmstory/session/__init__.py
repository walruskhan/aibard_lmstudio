from .LLMSession import LLMSession

sessions = dict()

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

def get_session(session_id: str):
    if session_id not in sessions.keys():
        raise f"session='{session_id}' does not exist"
    
    return sessions[session_id]