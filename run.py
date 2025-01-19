import sys
import subprocess
import importlib.util


#- for the run packages_installed 

def is_package_installed(package_name):
    """Check if a package is installed."""
    package_spec = importlib.util.find_spec(package_name)
    return package_spec is not None

def install_packages():
    """Install required packages."""
    packages = ["streamlit", "plotly"]
    for package in packages:
        if not is_package_installed(package):
            print(f"Installing {package}. Please wait...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"{package} installed successfully.")

def run_streamlit():
    """Run the Streamlit server."""
    print("Starting Streamlit server...")
    subprocess.Popen(["streamlit", "run", "path/to/your/streamlit_app.py"])
    print("Streamlit server started.")

if __name__ == "__main__":
    install_packages()
    run_streamlit()
    







