# Simple Justfile for launching dev servers
# Manages both Bun frontend and Flask backend development servers

# Set shell for Windows PowerShell
set shell := ["pwsh", "-c"]

# Default recipe - show available commands
default:
    @just --list

# Start Flask development server only
flask:
    @echo "🚀 Starting Flask development server..."
    @echo "Server will be available at: http://localhost:5000"
    cd llmstory && uv run python -c "from llmstory import app; app.run(debug=True, host='0.0.0.0', port=5000)"

# Start Bun development server only  
bun:
    @echo "🚀 Starting Bun development server..."
    @echo "Server will be available at: http://localhost:3000"
    cd frontend && bun run dev

# Start both servers (requires manual stopping)
dev:
    @echo "🚀 Starting both development servers..."
    @echo "Frontend (Bun):  http://localhost:3000"
    @echo "Backend (Flask): http://localhost:5000"
    @echo ""
    @echo "💡 Starting servers in separate PowerShell windows..."
    @echo "   Each server will open in its own window"
    @echo "   Close the windows or press Ctrl+C to stop servers"
    @echo ""
    @Start-Process pwsh -ArgumentList "-NoExit", "-Command", "Set-Location '{{justfile_directory()}}\llmstory'; Write-Host '🚀 Flask Server Starting...'; uv run python -c \"from llmstory import app; app.run(debug=True, host='0.0.0.0', port=5000)\""
    @Start-Process pwsh -ArgumentList "-NoExit", "-Command", "Set-Location '{{justfile_directory()}}\frontend'; Write-Host '🚀 Bun Server Starting...'; bun run dev"
    @echo "✅ Both servers launched in separate windows!"

# Show server URLs
urls:
    @echo "🌐 Development Server URLs:"
    @echo "Frontend (Bun):  http://localhost:3000"
    @echo "Backend (Flask): http://localhost:5000"
    @echo "API Health:      http://localhost:5000/api/health"
    @echo "API Docs:        http://localhost:5000/docs"

# Install dependencies
install:
    @echo "📦 Installing backend dependencies..."
    cd llmstory && uv sync
    @echo "📦 Installing frontend dependencies..."
    cd frontend && bun install
    @echo "✅ All dependencies installed!"

# Quick setup
setup: install
    @echo "🎉 Setup complete!"
    @echo "Run 'just dev' to start both servers"