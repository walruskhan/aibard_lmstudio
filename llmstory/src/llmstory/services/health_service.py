"""
Health service for application health monitoring.
"""
from typing import Dict
from datetime import datetime
from injector import inject, singleton
import os
import sys


@singleton
class HealthService:
    """Service for handling application health checks."""
    
    def __init__(self):
        self._start_time = datetime.now()
    
    def get_health_status(self) -> Dict:
        """Get comprehensive health status."""
        uptime = datetime.now() - self._start_time
        
        return {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'LLM Story API',
            'uptime_seconds': int(uptime.total_seconds()),
            'uptime_human': self._format_uptime(uptime),
            'python_version': sys.version,
            'platform': sys.platform,
            'memory_usage': self._get_memory_usage(),
            'environment': os.getenv('ENVIRONMENT', 'development'),
            'features': {
                'dependency_injection': True,
                'story_service': True,
                'contact_service': True,
                'api_routes': True,
                'web_routes': True
            }
        }
    
    def get_simple_health(self) -> Dict:
        """Get simple health check response."""
        return {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'LLM Story API'
        }
    
    def get_readiness_status(self) -> Dict:
        """Check if the application is ready to serve requests."""
        # In a real application, this would check database connectivity,
        # external service availability, etc.
        return {
            'ready': True,
            'timestamp': datetime.now().isoformat(),
            'checks': {
                'database': 'ok',  # Would check actual database
                'services': 'ok',
                'dependencies': 'ok'
            }
        }
    
    def get_liveness_status(self) -> Dict:
        """Check if the application is alive."""
        return {
            'alive': True,
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': int((datetime.now() - self._start_time).total_seconds())
        }
    
    def _format_uptime(self, uptime) -> str:
        """Format uptime duration in human-readable format."""
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        parts = []
        if days:
            parts.append(f"{days}d")
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        if seconds or not parts:
            parts.append(f"{seconds}s")
        
        return " ".join(parts)
    
    def _get_memory_usage(self) -> Dict:
        """Get basic memory usage information."""
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            return {
                'rss_mb': round(memory_info.rss / 1024 / 1024, 2),
                'vms_mb': round(memory_info.vms / 1024 / 1024, 2)
            }
        except ImportError:
            return {
                'rss_mb': 'unavailable (psutil not installed)',
                'vms_mb': 'unavailable (psutil not installed)'
            }