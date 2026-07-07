import subprocess
import json
import sys

print("Checking for outdated packages...")

# Fetch the outdated packages as JSON
result = subprocess.run(
    [sys.executable, "-m", "pip", "list", "--outdated", "--format=json"],
    capture_output=True,
    text=True
)

# Parse the JSON data
packages = json.loads(result.stdout)

if not packages:
    print("Everything is already up to date! 🎉")
else:
    print(f"Found {len(packages)} packages to upgrade.\n")

    # Loop and upgrade
    for package in packages:
        name = package["name"]
        print(f"Upgrading {name}...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", name])

    print("\nAll packages updated successfully!")