from waitress import serve
from app import app
import os

# Disable debug mode in production
app.config['DEBUG'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print("=" * 60)
    print("🚀 Employee Productivity Prediction System")
    print("=" * 60)
    print(f"✅ Production server starting...")
    print(f"📊 Server running on: http://localhost:{port}")
    print(f"🌐 Network access: http://0.0.0.0:{port}")
    print(f"⚙️  Worker threads: 4")
    print(f"🔒 Debug mode: OFF (Production)")
    print("=" * 60)
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    
    serve(app, host='0.0.0.0', port=port, threads=4, url_scheme='http')
