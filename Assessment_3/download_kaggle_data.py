from __future__ import annotations

import subprocess
import sys
from pathlib import Path

COMPETITION = "llms-you-cant-please-them-all"
DATA_DIR = Path("data")


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    print("This script uses the Kaggle CLI.")
    print("Before running, download kaggle.json from Kaggle Account Settings and put it in:")
    print("Windows: C:\\Users\\<YourName>\\.kaggle\\kaggle.json")
    print("Mac/Linux: ~/.kaggle/kaggle.json")
    print("You must also accept the competition rules on Kaggle first.")
    cmd = [sys.executable, "-m", "kaggle", "competitions", "download", "-c", COMPETITION, "-p", str(DATA_DIR), "--unzip"]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print("Downloaded files:")
    for path in sorted(DATA_DIR.glob("*")):
        print(" -", path)


if __name__ == "__main__":
    main()
