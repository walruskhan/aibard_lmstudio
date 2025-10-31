"""
Health service for application health monitoring.
"""
from typing import Dict
from datetime import datetime
from injector import inject, singleton
import os
import sys
import lmstudio as lms

@singleton
class LlmService:
    """Service for handling connection with LM Studio"""

    @property
    def model(self):
        """Get the current model."""
        return self._model

    @model.setter
    def model(self, value):
        """Set the current model."""
        self._model = value
    
    def __init__(self):
        self._start_time = datetime.now()
        self.model = None

    async def is_lmstudio_available_async(lmstudio_api_host: str):
        async with lms.AsyncClient() as client:
            return await lms.AsyncClient.is_valid_api_host(lmstudio_api_host)

    async def set_model_async(self, model_name):
        async with lms.AsyncClient() as client:
            available = await client.llm.list_downloaded()
            if model_name not in available:
                return (False, f"Model '{model_name}' not found in available models")

            self.model = await client.llm.model(model_name)
            return True
        
    async def list_models_async(self):
        async with lms.AsyncClient() as client:
            return await client.llm.list_downloaded() 
    