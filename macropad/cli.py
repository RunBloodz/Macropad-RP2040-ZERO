import os
import sys
import shutil
from pathlib import Path

def find_circuitpy_drive():
    """Find the CIRCUITPY drive mounted on Windows, macOS, or Linux."""
    # Windows drive letters (E:\, F:\, G:\, etc.)
    if sys.platform == "win32":
        import string
        for letter in string.ascii_uppercase:
            drive = Path(f"{letter}:\\")
            if drive.exists() and (drive / "boot_out.txt").exists():
                return drive
    # macOS
    elif sys.platform == "darwin":
        volumes = Path("/Volumes")
        if volumes.exists():
            for vol in volumes.iterdir():
                if vol.name == "CIRCUITPY" or (vol / "boot_out.txt").exists():
                    return vol
    # Linux
    else:
        try:
            username = os.getlogin()
        except Exception:
            username = "root"
        media_paths = [Path(f"/media/{username}"), Path("/media"), Path("/mnt")]
        for base in media_paths:
            if base.exists():
                for sub in base.glob("**/*"):
                    if sub.is_dir() and (sub.name == "CIRCUITPY" or (sub / "boot_out.txt").exists()):
                        return sub
    return None

def main():
    print("=== 15-Key RP2040 Macropad Deployment Tool ===")

    repo_dir = Path(__file__).parent.parent
    code_py = repo_dir / "code.py"
    boot_py = repo_dir / "boot.py"

    if not code_py.exists() or not boot_py.exists():
        print("Error: code.py and boot.py not found in project directory.")
        sys.exit(1)

    target_drive = find_circuitpy_drive()

    if target_drive and target_drive.exists():
        print(f"Found CircuitPython drive at: {target_drive}")
        try:
            shutil.copy(code_py, target_drive / "code.py")
            print(" -> Copied code.py successfully.")
            shutil.copy(boot_py, target_drive / "boot.py")
            print(" -> Copied boot.py successfully.")
            print("\nDeployment complete! Your 15-Key Macropad is ready.")
        except Exception as e:
            print(f"Error copying files: {e}")
    else:
        print("\nCould not automatically locate connected 'CIRCUITPY' drive.")
        print("Please copy 'code.py' and 'boot.py' manually onto your RP2040-Zero USB drive.")

if __name__ == "__main__":
    main()
