"""
deploy_fs.py — Build and upload LittleFS image to UniHiker K10

Usage:
    python deploy_fs.py --port COM3
    python deploy_fs.py --port COM3 --dry-run

Partition info (from partitions.csv in the sketch directory):
    offset = 0x510000   ("littlefs" partition, subtype spiffs)
    size   = 0x200000   (2097152 bytes / 2048 KB)
"""

import argparse
import subprocess
import sys
import os
import tempfile

MKLITTLEFS = (
    r"C:\Users\antfr\AppData\Local\Arduino15\packages\UNIHIKER"
    r"\tools\mklittlefs\3.0.0-gnu12-dc7f933\mklittlefs.exe"
)

FS_OFFSET    = "0x510000"
FS_SIZE      = 0x200000   # 2048 KB — "littlefs" partition in partitions.csv
BLOCK_SIZE   = 4096
PAGE_SIZE    = 256
DATA_DIR     = "data"
CHIP         = "esp32s3"


def run(cmd, dry_run=False):
    print(">>", " ".join(str(c) for c in cmd))
    if dry_run:
        return
    result = subprocess.run(cmd, check=True)
    return result


def main():
    parser = argparse.ArgumentParser(description="Upload LittleFS to UniHiker K10")
    parser.add_argument("--port", required=True, help="Serial port, e.g. COM3")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without executing")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir   = os.path.join(script_dir, DATA_DIR)
    image_path = os.path.join(script_dir, "littlefs.bin")

    if not os.path.isdir(data_dir):
        print(f"ERROR: data dir not found: {data_dir}", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(MKLITTLEFS):
        print(f"ERROR: mklittlefs not found: {MKLITTLEFS}", file=sys.stderr)
        sys.exit(1)

    print(f"\n--- Building LittleFS image from {data_dir} ---")
    run([
        MKLITTLEFS,
        "-c", data_dir,
        "-s", str(FS_SIZE),
        "-b", str(BLOCK_SIZE),
        "-p", str(PAGE_SIZE),
        image_path,
    ], args.dry_run)

    print(f"\n--- Uploading to {args.port} at {FS_OFFSET} ---")
    run([
        sys.executable, "-m", "esptool",
        "--chip", CHIP,
        "--port", args.port,
        "write_flash", FS_OFFSET, image_path,
    ], args.dry_run)

    print("\nDone.")


if __name__ == "__main__":
    main()
