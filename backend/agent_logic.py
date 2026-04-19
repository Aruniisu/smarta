import json, os, re
from langchain_groq import ChatGroq

class AegisAgents:
    def __init__(self, api_key):
        self.llm = ChatGroq(groq_api_key=api_key, model_name="llama-3.3-70b-versatile", temperature=0)

    def analyzer(self, repo_path, error_log=None):
        files = os.listdir(repo_path)
        
        # promt of identify frontend
        prompt = f"""
        Analyze these files: {files}. 
        Identify the Frontend framework (React, Vue, Angular, or Static HTML).
        Generate a professional Dockerfile using 'node:18-alpine' and 'serve' package.
        
        Return ONLY a JSON object:
        {{
            "framework": "Framework Name",
            "port": 3000,
            "dockerfile_content": "FROM node:18-alpine\\nWORKDIR /app\\nCOPY . .\\nRUN npm install\\nRUN npm install -g serve\\nEXPOSE 3000\\nCMD [\\"serve\\", \\"-s\\", \\".\\", \\"-l\\", \\"3000\\"]"
        }}
        """
        try:
            response = self.llm.invoke(prompt)
            json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
            data = json.loads(json_match.group(0))
            return data
        except:
            # Frontend Dockerfile (if frontend down)
            content = "FROM node:18-alpine\nWORKDIR /app\nCOPY . .\nRUN npm install\nRUN npm install -g serve\nEXPOSE 3000\nCMD [\"serve\", \"-s\", \".\", \"-l\", \"3000\"]"
            return {"framework": "Frontend App", "port": 3000, "dockerfile_content": content}