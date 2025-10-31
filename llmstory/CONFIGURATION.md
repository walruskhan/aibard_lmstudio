# Environment Configuration

This document explains how to configure the LLM Story application using environment variables.

## Quick Start

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` to match your environment
3. Start the application - configuration will be loaded automatically

## Configuration Files

- `.env.example` - Template with all available options and documentation
- `.env` - Your local development configuration (not committed to git)
- `.env.local` - Optional local overrides
- `.env.production` - Production configuration template

## Configuration Sections

### Application Environment
```bash
ENVIRONMENT=development          # development, production, testing
DEBUG=true                      # Enable/disable debug mode
```

### Flask Configuration
```bash
FLASK_ENV=development           # Flask environment
SECRET_KEY=your-secret-key      # Change in production!
FLASK_HOST=0.0.0.0             # Server host
FLASK_PORT=5000                # Server port
```

### API Configuration
```bash
API_VERSION=1.0.0              # API version number
API_TITLE=LLM Story API        # API title
API_DESCRIPTION=API description # API description
```

### Feature Flags
```bash
ENABLE_CONTACT_EMAIL=false     # Send actual emails for contact form
ENABLE_STORY_ANALYTICS=true   # Enable story analytics
ENABLE_API_DOCS=true          # Enable API documentation
ENABLE_HEALTH_DETAILED=true   # Detailed health check info
```

### Security Configuration
```bash
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
RATE_LIMIT_PER_MINUTE=60
JWT_SECRET_KEY=jwt-secret-key
```

### Database Configuration (Future)
```bash
DATABASE_URL=sqlite:///llmstory.db
DATABASE_ECHO=false
```

### Email Configuration (Future)
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_USE_TLS=true
FROM_EMAIL=noreply@llmstory.com
```

## Accessing Configuration in Code

The `ConfigService` is available through dependency injection:

```python
from flask_injector import inject
from services import ConfigService

@inject
def my_endpoint(config_service: ConfigService):
    if config_service.features.enable_story_analytics:
        # Analytics is enabled
        pass
    
    # Access configuration sections
    db_url = config_service.database.url
    api_version = config_service.api.version
    is_dev = config_service.is_development()
```

## Environment-Specific Configuration

### Development
- Debug mode enabled
- Relaxed security settings
- Detailed logging
- Auto-reload enabled

### Production
- Debug mode disabled
- Strict security settings
- Optimized logging
- Static file caching

### Testing
- In-memory database
- Disabled external services
- Fast test execution

## Security Best Practices

1. **Never commit .env files** - They contain secrets
2. **Use strong secret keys** - Generate random keys for production
3. **Rotate secrets regularly** - Especially API keys and passwords
4. **Use environment-specific files** - Different configs for different environments
5. **Validate configuration** - Check required settings on startup

## Configuration Validation

The `ConfigService` automatically validates configuration on startup:

- Loads environment variables from `.env`
- Provides type conversion (string, int, bool, list)
- Sets sensible defaults
- Reports configuration errors clearly

## API Endpoints

Access configuration through API:

- `GET /api/config` - Public configuration information
- `GET /api/version` - API version and environment info
- `GET /api/health` - Health check with environment details

## Troubleshooting

### Configuration Not Loading
1. Check `.env` file exists in the correct directory
2. Verify file permissions
3. Check for syntax errors in `.env`
4. Review application logs for error messages

### Invalid Values
1. Check boolean values use: true/false, 1/0, yes/no
2. Verify integer values are numeric
3. Check list values use comma separation
4. Ensure required environment variables are set

### Environment Variables
Environment variables override `.env` file values:
```bash
export FLASK_PORT=8080  # This overrides .env setting
```