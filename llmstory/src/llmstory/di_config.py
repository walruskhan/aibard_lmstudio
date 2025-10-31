"""
Dependency injection configuration for the application.
"""
from injector import Module, provider, singleton
from .services import ConfigService


class ServiceModule(Module):
    """Module for configuring service dependencies."""
    
    @provider
    @singleton
    def provide_config_service(self) -> ConfigService:
        """Provide ConfigService instance (loaded first)."""
        return ConfigService()


# You can add more modules here for different layers
class RepositoryModule(Module):
    """Module for configuring repository dependencies."""
    
    # Future: Add database repositories here
    pass


class ConfigModule(Module):
    """Module for configuring application settings."""
    
    # Future: Add configuration providers here
    pass