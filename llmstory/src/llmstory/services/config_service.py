"""
Configuration service for managing environment variables and app settings.
"""
import os
from typing import Any, Dict, Optional
from dataclasses import dataclass
from injector import singleton
from dotenv import load_dotenv


@dataclass
class DatabaseConfig:
    """Database configuration."""
    url: str
    echo: bool = False


@dataclass
class EmailConfig:
    """Email configuration."""
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    smtp_use_tls: bool
    from_email: str

@dataclass
class LmStudioConfig:
    """LMStudio Configuration"""
    lmstudio_api_host: str


@dataclass
class SecurityConfig:
    """Security configuration."""
    secret_key: str
    jwt_secret_key: str
    cors_origins: list[str]
    rate_limit_per_minute: int


@dataclass
class APIConfig:
    """API configuration."""
    version: str
    title: str
    description: str


@dataclass
class FeatureFlags:
    """Feature flags configuration."""
    enable_contact_email: bool
    enable_story_analytics: bool
    enable_api_docs: bool
    enable_health_detailed: bool


@singleton
class ConfigService:
    """Service for managing application configuration."""
    
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Basic app configuration
        self.environment = os.getenv('ENVIRONMENT', 'development')
        self.debug = self._get_bool('DEBUG', True)
        self.flask_host = os.getenv('FLASK_HOST', '0.0.0.0')
        self.flask_port = int(os.getenv('FLASK_PORT', '5000'))
        
        # Load configuration sections
        self._database = self._load_database_config()
        self._email = self._load_email_config()
        self._lmstudio = self._load_lmstudio_config()
        self._security = self._load_security_config()
        self._api = self._load_api_config()
        self._features = self._load_feature_flags()
        
        # Logging configuration
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.log_file = os.getenv('LOG_FILE', 'logs/app.log')
        
        print(f"🔧 Configuration loaded for environment: {self.environment}")
    
    @property
    def database(self) -> DatabaseConfig:
        """Get database configuration."""
        return self._database
    
    @property
    def email(self) -> EmailConfig:
        """Get email configuration."""
        return self._email
    
    @property
    def lmstudio(self) -> LmStudioConfig:
        """Get email configuration."""
        return self._lmstudio
    
    @property
    def security(self) -> SecurityConfig:
        """Get security configuration."""
        return self._security
    
    @property
    def api(self) -> APIConfig:
        """Get API configuration."""
        return self._api
    
    @property
    def features(self) -> FeatureFlags:
        """Get feature flags."""
        return self._features
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get environment variable with optional default."""
        return os.getenv(key, default)
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get environment variable as integer."""
        try:
            return int(os.getenv(key, str(default)))
        except (ValueError, TypeError):
            return default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get environment variable as boolean."""
        return self._get_bool(key, default)
    
    def get_list(self, key: str, default: Optional[list] = None, separator: str = ',') -> list:
        """Get environment variable as list."""
        if default is None:
            default = []
        
        value = os.getenv(key)
        if not value:
            return default
        
        return [item.strip() for item in value.split(separator) if item.strip()]
    
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == 'development'
    
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == 'production'
    
    def is_testing(self) -> bool:
        """Check if running in testing environment."""
        return self.environment.lower() == 'testing'
    
    def get_flask_config(self) -> Dict[str, Any]:
        """Get Flask configuration dictionary."""
        return {
            'SECRET_KEY': self.security.secret_key,
            'DEBUG': self.debug,
            'ENVIRONMENT': self.environment,
            'TEMPLATES_AUTO_RELOAD': self._get_bool('TEMPLATES_AUTO_RELOAD', self.debug),
            'SEND_FILE_MAX_AGE_DEFAULT': self.get_int('SEND_FILE_MAX_AGE_DEFAULT', 0 if self.debug else 43200),
            'MAX_CONTENT_LENGTH': self.get_int('MAX_CONTENT_LENGTH', 16 * 1024 * 1024),  # 16MB
        }
    
    def _load_database_config(self) -> DatabaseConfig:
        """Load database configuration."""
        return DatabaseConfig(
            url=os.getenv('DATABASE_URL', 'sqlite:///llmstory.db'),
            echo=self._get_bool('DATABASE_ECHO', False)
        )
    
    def _load_email_config(self) -> EmailConfig:
        """Load email configuration."""
        return EmailConfig(
            smtp_host=os.getenv('SMTP_HOST', 'localhost'),
            smtp_port=self.get_int('SMTP_PORT', 587),
            smtp_username=os.getenv('SMTP_USERNAME', ''),
            smtp_password=os.getenv('SMTP_PASSWORD', ''),
            smtp_use_tls=self._get_bool('SMTP_USE_TLS', True),
            from_email=os.getenv('FROM_EMAIL', 'noreply@llmstory.com')
        )
    
    def _load_lmstudio_config(self) -> LmStudioConfig:
        """Load LMStudio Configuration"""
        return LmStudioConfig(
            lmstudio_api_host=os.getenv('LMSTUDIO_API_HOST', 'localhost:1234')
        )
    
    def _load_security_config(self) -> SecurityConfig:
        """Load security configuration."""
        return SecurityConfig(
            secret_key=os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production'),
            jwt_secret_key=os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production'),
            cors_origins=self.get_list('CORS_ORIGINS', ['http://localhost:3000']),
            rate_limit_per_minute=self.get_int('RATE_LIMIT_PER_MINUTE', 60)
        )
    
    def _load_api_config(self) -> APIConfig:
        """Load API configuration."""
        return APIConfig(
            version=os.getenv('API_VERSION', '1.0.0'),
            title=os.getenv('API_TITLE', 'LLM Story API'),
            description=os.getenv('API_DESCRIPTION', 'API for LLM Story application')
        )
    
    def _load_feature_flags(self) -> FeatureFlags:
        """Load feature flags."""
        return FeatureFlags(
            enable_contact_email=self._get_bool('ENABLE_CONTACT_EMAIL', False),
            enable_story_analytics=self._get_bool('ENABLE_STORY_ANALYTICS', True),
            enable_api_docs=self._get_bool('ENABLE_API_DOCS', True),
            enable_health_detailed=self._get_bool('ENABLE_HEALTH_DETAILED', True)
        )
    
    def _get_bool(self, key: str, default: bool = False) -> bool:
        """Convert environment variable to boolean."""
        value = os.getenv(key)
        if value is None:
            return default
        return value.lower() in ('true', '1', 'yes', 'on', 'enabled')