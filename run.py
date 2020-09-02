# Reference the domain_registry module and import the Flask app
from domain_registry import app

# Expose port 80 over all interfaces with debug mode enabled
app.run(host='0.0.0.0', port=80, debug=True)