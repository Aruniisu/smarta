import subprocess
import os
import time
import signal

class DevOpsTools:
    def run_git_clone(self, url):
        path = os.path.join(os.getcwd(), f"temp_repo_{int(time.time())}")
        res = subprocess.run(["git", "clone", url.strip(), path], capture_output=True, text=True)
        return path if res.returncode == 0 else None

    def run_docker_deployment(self, path, port):
        # try the Docker
        container_name = "devops-container"
        image_name = "aegis-app"
        subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)
        build = subprocess.run(["docker", "build", "-t", image_name, path], capture_output=True)
        
        if build.returncode == 0:
            subprocess.run(["docker", "run", "-d", "--name", container_name, "-p", f"{port}:{port}", image_name])
            return True, None
        
        # --- Local Deployment (The Ultimate Fix) ---
        print(f"[DEBUG] Docker failed. Launching Local React Server...")
        
        try:
            target_dir = path
            for root, dirs, files in os.walk(path):
                if "package.json" in files:
                    target_dir = root
                    break
            
            original_cwd = os.getcwd()
            os.chdir(target_dir)

            # 1. Port Cleanup 
            # 3000 is release in Windows
            subprocess.run(f"npx kill-port {port}", shell=True, capture_output=True)

            # 2. Dependencies install
            print("[DEBUG] Installing dependencies... Please wait.")
            subprocess.run("npm install", shell=True, capture_output=True)

            # 3. browser running running without open for React App
            
            print(f"[DEBUG] Starting React server on http://localhost:{port}")
            
            # Security command for windows
            full_cmd = f'set BROWSER=none&& set PORT={port}&& npm start'
            
            
            subprocess.Popen(full_cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            
            os.chdir(original_cwd)
            return True, "Success"
            
        except Exception as e:
            if 'original_cwd' in locals(): os.chdir(original_cwd)
            print(f"[ERROR] {e}")
            return False, str(e)