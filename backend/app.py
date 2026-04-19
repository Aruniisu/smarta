from flask import Flask, request, jsonify, session, url_for
from flask_cors import CORS
from flask_pymongo import PyMongo
from authlib.integrations.flask_client import OAuth
from agent_logic import AegisAgents
from tools import DevOpsTools
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("devops")

# CORS සැකසුම්
CORS(app, supports_credentials=True, origins=["http://localhost:3000", "http://localhost:3001"])

# MongoDB Configuration
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

# Google OAuth Configuration
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("67652746046-bbegh5v4678p72d512jqo7km9me4o9n1.apps.googleusercontent.com"),
    client_secret=os.getenv("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"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid profile email'},
    userinfo_endpoint='https://www.googleapis.com/oauth2/v3/userinfo'
)

# Agent සහ Tools Initialize කිරීම
agent = AegisAgents(os.getenv("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"))
tools = DevOpsTools()

@app.route('/api/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/api/authorize')
def authorize():
    token = google.authorize_access_token()
    resp = google.get('https://www.googleapis.com/oauth2/v3/userinfo')
    user_info = resp.json()
    
    session['user'] = user_info
    
    # User තොරතුරු MongoDB හි සේව් කිරීම
    mongo.db.users.update_one(
        {"email": user_info['email']},
        {"$set": {"name": user_info.get('name'), "picture": user_info.get('picture')}},
        upsert=True
    )
    return "<h1>Login Success!</h1><script>setTimeout(() => { window.close(); }, 1500);</script>"

@app.route('/api/logout')
def logout():
    session.pop('user', None)
    return jsonify({"status": "logged out"})

@app.route('/api/deploy', methods=['POST'])
def deploy():
    data = request.json
    url = data.get('url')
    user = session.get('user')
    user_email = user.get('email', "guest") if user else "guest"

    if not url:
        return jsonify({"status": "error", "message": "URL is missing"}), 400

    try:
        # Step 1: Clone the Repo
        repo_path = tools.run_git_clone(url)
        
        # Step 2: AI Analysis
        analysis = agent.analyzer(repo_path)
        
        # Step 3: Get deployment parameters
        p_type = analysis.get('type', 'Web App')
        p_port = analysis.get('port', 3000)

        # Step 4: Docker Deployment
        success, msg = tools.run_docker_deployment(repo_path, p_port)
        live_link = f"http://localhost:{p_port}"
        
        # Step 5: Save History (Only if logged in)
        if user_email != "guest":
            mongo.db.history.insert_one({
                "email": user_email,
                "url": url,
                "live_link": live_link,
                "type": p_type
            })

        return jsonify({"status": "success", "link": live_link})
    except Exception as e:
        print(f"Deployment Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    user = session.get('user')
    if not user: return jsonify([])
    history = list(mongo.db.history.find({"email": user['email']}, {"_id": 0}))
    return jsonify(history)

@app.route('/api/user')
def get_current_user():
    user = session.get('user')
    return jsonify(user) if user else jsonify(None)

if __name__ == '__main__':
    app.run(port=5000, debug=True)