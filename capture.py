import sys
import json
import subprocess
import time
import os

# Predictable location for your ecosystem
OUTPUT_DIR = "/tmp/hermes_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_active_windows():
    """Retrieve and parse window list."""
    try:
        cmd = [
            "gdbus", "call", "--session", 
            "--dest", "org.gnome.Shell", 
            "--object-path", "/org/gnome/Shell/Extensions/Windows", 
            "--method", "org.gnome.Shell.Extensions.Windows.List"
        ]
        # We capture stdout here because we actually need the JSON list
        result = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode('utf-8').strip()
        
        # Strip the wrapping '( ... )' returned by gdbus
        start = result.find("'") + 1
        end = result.rfind("'")
        json_data = result[start:end]
        
        return json.loads(json_data)
    except Exception as e:
        # We keep this for debugging if the extension fails
        print(f"Error accessing Window Calls extension: {e}")
        return []

def focus_window(window_id):
    """Focus the specific window using the extension."""
    # Suppress output to hide the '()'
    subprocess.run([
        "gdbus", "call", "--session", 
        "--dest", "org.gnome.Shell", 
        "--object-path", "/org/gnome/Shell/Extensions/Windows", 
        "--method", "org.gnome.Shell.Extensions.Windows.Activate",
        str(window_id)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Give the compositor time to switch focus
    time.sleep(0.5)

def capture_with_gnome_screenshot(output_path):
    """Uses gnome-screenshot for a blocking, reliable capture."""
    # -w captures the focused window
    # -f specifies the output file path
    cmd = ["gnome-screenshot", "-w", "-f", output_path]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Screenshot capture failed: {e}")
        return False
    except FileNotFoundError:
        print("Error: gnome-screenshot is not installed. Please run: sudo apt install gnome-screenshot")
        return False

def main():
    search_keywords = sys.argv[1:]
    if not search_keywords:
        print("Usage: python3 capture.py <keyword1> <keyword2> ...")
        return

    windows = get_active_windows()
    
    # Iterate through open windows and match titles
    for win in windows:
        title = win.get('title', '')
        if any(kw.lower() in title.lower() for kw in search_keywords):
            print(f"Hermes found match: '{title}' (ID: {win['id']})")
            
            # Focus the window before capturing
            focus_window(win['id'])
            
            # Set target file path
            dest = os.path.join(OUTPUT_DIR, "hermes_capture.png")
            
            # Perform blocking capture
            if capture_with_gnome_screenshot(dest):
                print(f"Hermes successfully captured window to: {dest}")
            else:
                print("Failed to capture screenshot.")
            
            return

    print("No matching windows found.")

if __name__ == "__main__":
    main()