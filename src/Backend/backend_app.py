from flask import Flask
from flask_session import Session
from dotenv import load_dotenv
from routes import routes

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = '2DE89DF852C7CF338CAA437A1896E'
Session(app)

# Load environment variables for API keys
load_dotenv()

# Register the blueprint to route CRUD calls 
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)