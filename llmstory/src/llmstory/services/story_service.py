"""
Story service for managing story operations.
"""
from typing import List, Dict, Optional
from datetime import datetime
from injector import inject, singleton


@singleton
class StoryService:
    """Service for handling story-related operations."""
    
    def __init__(self):
        # In a real application, this would connect to a database
        self._stories = [
            {
                'id': 1,
                'title': 'The AI Assistant',
                'summary': 'A story about an AI that learns to be helpful',
                'content': 'Once upon a time, there was an AI assistant that wanted to help everyone...',
                'created_at': '2025-10-30T10:00:00Z',
                'status': 'published'
            },
            {
                'id': 2,
                'title': 'Code Generation Magic',
                'summary': 'How AI helps developers write better code',
                'content': 'In the world of software development, AI became a powerful ally...',
                'created_at': '2025-10-30T11:00:00Z',
                'status': 'draft'
            }
        ]
        self._next_id = 3
    
    def get_all_stories(self) -> List[Dict]:
        """Get all stories."""
        return self._stories.copy()
    
    def get_story_by_id(self, story_id: int) -> Optional[Dict]:
        """Get a specific story by ID."""
        for story in self._stories:
            if story['id'] == story_id:
                return story.copy()
        return None
    
    def create_story(self, title: str, content: str, summary: str = '') -> Dict:
        """Create a new story."""
        story = {
            'id': self._next_id,
            'title': title,
            'content': content,
            'summary': summary or content[:100] + '...' if len(content) > 100 else content,
            'created_at': datetime.now().isoformat(),
            'status': 'draft'
        }
        self._stories.append(story)
        self._next_id += 1
        return story.copy()
    
    def update_story(self, story_id: int, **updates) -> Optional[Dict]:
        """Update an existing story."""
        for i, story in enumerate(self._stories):
            if story['id'] == story_id:
                # Update allowed fields
                allowed_fields = {'title', 'content', 'summary', 'status'}
                for key, value in updates.items():
                    if key in allowed_fields:
                        self._stories[i][key] = value
                return self._stories[i].copy()
        return None
    
    def delete_story(self, story_id: int) -> bool:
        """Delete a story."""
        for i, story in enumerate(self._stories):
            if story['id'] == story_id:
                del self._stories[i]
                return True
        return False
    
    def get_stories_count(self) -> int:
        """Get total count of stories."""
        return len(self._stories)
    
    def search_stories(self, query: str) -> List[Dict]:
        """Search stories by title or content."""
        query_lower = query.lower()
        results = []
        for story in self._stories:
            if (query_lower in story['title'].lower() or 
                query_lower in story['content'].lower() or
                query_lower in story['summary'].lower()):
                results.append(story.copy())
        return results