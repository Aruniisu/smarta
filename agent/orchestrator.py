from agent_logic import AegisAgents
from tools import DevOpsTools
import os

class AegisOrchestrator:
    def __init__(self, api_key):
        self.agents = AegisAgents(api_key)
        self.tools = DevOpsTools()

    def start_workflow(self, github_url):
        repo_path = self.tools.run_git_clone(github_url)
        if not repo_path:
            return {"status": "Error", "msg": "GitHub Clone Failed"}

        analysis = self.agents.analyzer(repo_path)
        
        with open(os.path.join(repo_path, "Dockerfile"), "w") as f:
            f.write(analysis['dockerfile_content'])
        
        success, err = self.tools.run_docker_deployment(repo_path, analysis['port'])
        
        if success:
            return {
                "status": "Success", 
                "link": f"http://localhost:{analysis['port']}", 
                "tech": analysis['framework']
            }
        else:
            return {"status": "Error", "msg": err}