"""
NyayaSetu AI - Standalone Production Packaging Script
Packages clean E:\nyayasetu-ai directory into:
1. E:\nyayasetu-ai.zip
2. E:\Final NyayaSetu\nyayasetu-ai.zip
"""

import os
import shutil
import zipfile
from pathlib import Path

SOURCE_DIR = Path(__file__).resolve().parent
DEST_ZIP_1 = SOURCE_DIR.parent / "nyayasetu-ai.zip"
DEST_ZIP_2 = Path("E:/Final NyayaSetu/nyayasetu-ai.zip") if Path("E:/").exists() else None

EXCLUDE_DIRS = {"__pycache__", ".pytest_cache", ".git", ".idea", ".vscode"}
EXCLUDE_EXTS = {".pyc", ".pyo", ".zip"}

def create_zip():
    print(f"Packaging {SOURCE_DIR} into {DEST_ZIP_1}...")
    file_count = 0
    total_bytes = 0

    if DEST_ZIP_1.exists():
        DEST_ZIP_1.unlink()

    with zipfile.ZipFile(DEST_ZIP_1, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(SOURCE_DIR):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in EXCLUDE_EXTS:
                    continue

                full_path = Path(root) / file
                rel_path = full_path.relative_to(SOURCE_DIR)

                zipf.write(full_path, rel_path)
                file_count += 1
                total_bytes += full_path.stat().st_size

    if DEST_ZIP_2:
        DEST_ZIP_2.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(DEST_ZIP_1, DEST_ZIP_2)

    zip_size_mb = DEST_ZIP_1.stat().st_size / (1024 * 1024)
    print(f" Successfully packaged {file_count} files ({total_bytes / (1024*1024):.2f} MB uncompressed).")
    print(f"   --> {DEST_ZIP_1} ({zip_size_mb:.2f} MB)")
    if DEST_ZIP_2:
        print(f"   --> {DEST_ZIP_2} ({zip_size_mb:.2f} MB)")

if __name__ == "__main__":
    create_zip()
