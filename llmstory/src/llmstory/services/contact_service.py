"""
Contact service for managing contact form submissions.
"""
from typing import Dict, List
from datetime import datetime
from injector import inject, singleton
import json


@singleton
class ContactService:
    """Service for handling contact form operations."""
    
    def __init__(self):
        # In a real application, this would connect to a database
        self._contacts = []
        self._next_id = 1
    
    def submit_contact(self, name: str, email: str, subject: str, message: str) -> Dict:
        """Submit a contact form."""
        # Validate input
        self._validate_contact_data(name, email, subject, message)
        
        contact = {
            'id': self._next_id,
            'name': name.strip(),
            'email': email.strip().lower(),
            'subject': subject.strip(),
            'message': message.strip(),
            'timestamp': datetime.now().isoformat(),
            'status': 'new'
        }
        
        self._contacts.append(contact)
        self._next_id += 1
        
        # Log the contact submission
        self._log_contact_submission(contact)
        
        return {
            'success': True,
            'message': 'Thank you for your message! We will get back to you soon.',
            'submission_id': f"contact_{contact['id']:06d}"
        }
    
    def get_all_contacts(self) -> List[Dict]:
        """Get all contact submissions."""
        return self._contacts.copy()
    
    def get_contact_by_id(self, contact_id: int) -> Dict:
        """Get a specific contact by ID."""
        for contact in self._contacts:
            if contact['id'] == contact_id:
                return contact.copy()
        return None
    
    def mark_contact_as_read(self, contact_id: int) -> bool:
        """Mark a contact as read."""
        for contact in self._contacts:
            if contact['id'] == contact_id:
                contact['status'] = 'read'
                return True
        return False
    
    def get_unread_contacts_count(self) -> int:
        """Get count of unread contacts."""
        return len([c for c in self._contacts if c['status'] == 'new'])
    
    def _validate_contact_data(self, name: str, email: str, subject: str, message: str):
        """Validate contact form data."""
        errors = []
        
        if not name or not name.strip():
            errors.append('Name is required')
        
        if not email or not email.strip():
            errors.append('Email is required')
        elif '@' not in email or '.' not in email.split('@')[-1]:
            errors.append('Invalid email format')
        
        if not subject or not subject.strip():
            errors.append('Subject is required')
        
        if not message or not message.strip():
            errors.append('Message is required')
        
        if errors:
            raise ValueError('; '.join(errors))
    
    def _log_contact_submission(self, contact: Dict):
        """Log contact submission for debugging/monitoring."""
        log_data = {
            'type': 'contact_submission',
            'contact_id': contact['id'],
            'timestamp': contact['timestamp'],
            'email': contact['email'],
            'subject': contact['subject']
        }
        print(f"Contact submission logged: {json.dumps(log_data, indent=2)}")