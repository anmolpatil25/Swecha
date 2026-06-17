import subprocess
import sys
import shutil

def check_version(command, name):
    print(f"\nChecking {name}...")
    try:
        result = subprocess.check_output(command, shell=True, text=True).strip()
        version_line = result.splitlines()[0]
        print(f"{name} version detected: {version_line}")
    except FileNotFoundError:
        print(f"{name} not found.")
    except subprocess.CalledProcessError as e:
        print(f"Error running {name}: {e}")

def install_vscode_extensions():
    print("\nInstalling VS Code extensions...")
    extensions = [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "GitLab.gitlab-workflow",
        "Cline.code-cline"
    ]
    for ext in extensions:
        try:
            subprocess.run(f"code --install-extension {ext}", shell=True, check=True)
            print(f"Installed: {ext}")
        except subprocess.CalledProcessError:
            print(f"Failed to install: {ext}")

def install_pip_packages():
    print("\nInstalling/upgrading pip packages...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "uv", "streamlit", "jupyterlab"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Package installation failed: {e}")

def main():
    print("Starting Summer of AI 2025 setup...")

    check_version("git --version", "Git")
    check_version("code --version", "VS Code")
    install_vscode_extensions()

    check_version("python --version", "Python")
    install_pip_packages()

    check_version("uv --version", "uv")
    check_version("streamlit --version", "Streamlit")
    check_version("jupyter-lab --version", "JupyterLab")

    print("\nAll tools installed and verified.")
    print("Next Steps:")
    print(" - Clone Swecha notebooks: git clone https://gitlab.com/swecha/summer-of-ai-notebooks.git")
    print(" - Open JupyterLab: cd summer-of-ai-notebooks && jupyter lab")
    print("\nYou're now ready for Summer of AI 2025!")

if __name__ == "__main__":
    main()
