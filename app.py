import subprocess
import sys
import shutil
from packaging import version
import importlib.metadata

def run_command(command, check=True):
    print(f"▶ Running: {command}")
    if isinstance(command, str):
        subprocess.run(command, shell=True, check=check)
    else:
        subprocess.run(command, check=check)

def is_installed(command):
    return shutil.which(command) is not None

def get_version(package_name):
    try:
        return importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        return None

def install_uv():
    if not is_installed("uv"):
        print("⬇ Installing uv...")
        run_command(["pip", "install", "uv"])
    else:
        print("✅ uv is already installed.")

def install_jupyterlab():
    current_version = get_version("jupyterlab")
    if current_version and version.parse(current_version) >= version.parse("4.2"):
        print(f"✅ JupyterLab {current_version} is already installed.")
    else:
        print("⬇ Installing/Upgrading JupyterLab...")
        run_command(["pip", "install", "--upgrade", "jupyterlab>=4.2"])

def install_streamlit():
    current_version = get_version("streamlit")
    if current_version and version.parse(current_version) >= version.parse("1.40"):
        print(f"✅ Streamlit {current_version} is already installed.")
    else:
        print("⬇ Installing/Upgrading Streamlit...")
        run_command(["pip", "install", "--upgrade", "streamlit>=1.40"])

def install_git():
    if is_installed("git"):
        try:
            version_str = subprocess.check_output("git --version", shell=True).decode().split()[2]
            if int(version_str.split(".")[0]) >= 2:
                print(f"✅ Git {version_str} is already installed.")
                return
            else:
                print(f"⚠ Git version {version_str} is outdated.")
        except Exception as e:
            print(f"⚠ Could not determine Git version: {e}")
    print("⬇ Installing Git...")
    if sys.platform == "win32":
        run_command(["winget", "install", "--id", "Git.Git", "-e", "--silent"])
    elif sys.platform == "darwin":
        run_command(["brew", "install", "git"])
    elif sys.platform.startswith("linux"):
        run_command(["sudo", "apt", "update"])
        run_command(["sudo", "apt", "install", "git", "-y"])
    else:
        print("❌ Unsupported OS for automatic Git install.")

def install_vscode():
    try:
        if is_installed("code"):
            version_str = subprocess.check_output("code --version", shell=True).decode().splitlines()[0]
            try:
                if float(version_str[:4]) >= 1.99:
                    print(f"✅ VS Code {version_str} is already installed.")
                    return
            except ValueError:
                print(f"⚠ Unable to parse VS Code version: {version_str}")
        else:
            print("⚠ VS Code not found, installing...")

        print("⬇ Installing VS Code...")
        try:
            run_command(["winget", "install", "--id", "Microsoft.VisualStudioCode", "-e", "--silent"])
        except subprocess.CalledProcessError:
            print("⚠ Silent install failed. Trying non-silent install...")
            run_command(["winget", "install", "--id", "Microsoft.VisualStudioCode", "-e"])

        if is_installed("code"):
            print("📦 Installing Ruff extension in VS Code...")
            run_command(["code", "--install-extension", "charliermarsh.ruff"])
    except Exception as e:
        print(f"❌ VS Code installation failed: {e}")

def install_ruff():
    current_version = get_version("ruff")
    if current_version:
        print(f"✅ Ruff {current_version} is already installed.")
    else:
        print("⬇ Installing Ruff...")
        run_command(["pip", "install", "ruff"])

# ------------------------------
# Entry Point
# ------------------------------

print("🚀 Starting tech stack setup...\n")

# Check Python version
if sys.version_info < (3, 11):
    print("❌ Python 3.11+ is required. Please upgrade your Python version.")
    sys.exit(1)

# Upgrade pip
run_command(["python", "-m", "pip", "install", "--upgrade", "pip"])

# Install each component
install_uv()
install_jupyterlab()
install_streamlit()
install_git()
install_vscode()
install_ruff()

print("\n✅ All tools checked and installed successfully!")