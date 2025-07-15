import os
import subprocess

# List of tuples containing the absolute directory and the corresponding script
scripts = [
    (r"/Users/srinithi/desktop/Project_Final/Blockchain_Webpage", "peer.py"),
    (r"/Users/srinithi/desktop/Project_Final/Blockchain_Webpage", "run_app.py"),
    (r"/Users/srinithi/desktop/Project_Final/Encryption", "app.py"),
    (r"/Users/srinithi/desktop/Project_Final/Option_display", "app.py")
]

# Loop through each script and run it in its respective directory
for directory, script in scripts:
    if os.path.exists(directory):
        script_path = os.path.join(directory, script)
        print(f"Opening {script} in a new terminal from {directory}")
        
        # AppleScript command to open terminal and run the Python script
        subprocess.Popen(['osascript', '-e', f'tell application "Terminal" to do script "cd {directory} && python3 {script}"'])
    else:
        print(f"Directory {directory} does not exist!")
