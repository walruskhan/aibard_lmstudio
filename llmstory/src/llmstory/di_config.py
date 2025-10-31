"""
Dependency injection configuration for the application.
"""
from injector import Module, provider, singleton
from .services import StoryService, ContactService, HealthService


class ServiceModule(Module):
    """Module for configuring service dependencies."""
    
    @provider
    @singleton
    def provide_story_service(self) -> StoryService:
        """Provide StoryService instance."""
        return StoryService()
    
    @provider
    @singleton
    def provide_contact_service(self) -> ContactService:
        """Provide ContactService instance."""
        return ContactService()
    
    @provider
    @singleton
    def provide_health_service(self) -> HealthService:
        """Provide HealthService instance."""
        return HealthService()


# You can add more modules here for different layers
class RepositoryModule(Module):
    """Module for configuring repository dependencies."""
    
    # Future: Add database repositories here
    pass


class ConfigModule(Module):
    """Module for configuring application settings."""
    
    # Future: Add configuration providers here
    pass