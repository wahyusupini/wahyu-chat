import subprocess
import json
import sys

outdated = subprocess.check_output([sys.executable, "-m", "pip", "list", "--outdated", "--format=json"])
packages = json.loads(outdated)
for package in packages:
    subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", package["name"]])