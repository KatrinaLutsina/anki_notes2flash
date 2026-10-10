import os
import shutil
import subprocess
import zipfile

DEFAULT_CONFIG = {
    "openrouter_api_key": "",
    "notion_api_key": "",
}

def bundle_addon():
    addon_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(addon_dir)
    libs_dir = os.path.join(addon_dir, "libs")
    output_file = os.path.join(project_dir, "notes2flash.ankiaddon")
    requirements_file = os.path.join(project_dir, "requirements.txt")
    installed_packages_file = os.path.join(libs_dir, "installed_packages.txt")
    excluded_files = {
        ".DS_Store",
        "config.json",
        "meta.json",
        "notes2flash.log",
        "service_account.json",
        "tracked_docs.json",
        "user_inputs.json",
    }

    # Step 1: Check whether requirements changed since the last bundle.
    os.makedirs(libs_dir, exist_ok=True)
    with open(requirements_file, 'r') as requirements:
        required_packages = [
            line.strip()
            for line in requirements
            if line.strip() and not line.lstrip().startswith("#")
        ]

    try:
        with open(installed_packages_file, 'r') as installed_packages:
            installed_requirements = installed_packages.read().splitlines()
    except FileNotFoundError:
        installed_requirements = []

    install_dependencies = required_packages != installed_requirements

    # Step 2: Install or update dependencies only if needed
    if install_dependencies:
        print("Installing or updating dependencies...")
        subprocess.run(
            ["pip", "install", "--upgrade", "--target", libs_dir, "-r", requirements_file],
            check=True,
        )
        with open(installed_packages_file, 'w') as installed_packages:
            installed_packages.write('\n'.join(required_packages) + '\n')
    else:
        print("Dependencies are already up to date. Skipping installation.")

    # Step 3: Clean up any existing __pycache__ folders
    print("Removing __pycache__ folders...")
    for root, dirs, _ in os.walk(addon_dir):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                shutil.rmtree(os.path.join(root, dir_name))

    # Step 4: Create the zip archive for the add-on (.ankiaddon file)
    if os.path.exists(output_file):
        os.remove(output_file)

    print("Creating addon package...")
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(addon_dir):
            for file in files:
                if file in excluded_files or ".bak-" in file:
                    continue
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, addon_dir)
                zipf.write(file_path, arcname)

        import json
        zipf.writestr("config.json", json.dumps(DEFAULT_CONFIG, indent=4) + "\n")

    print(f"Addon packaged successfully as {output_file}!")

if __name__ == "__main__":
    bundle_addon()
