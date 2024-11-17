import os
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import sys


def create_directory_structure(target_dir, extension):
    target_path = Path(target_dir) / extension
    target_path.mkdir(parents=True, exist_ok=True)
    return target_path


def process_file(file_path, target_dir):
    extension = file_path.suffix.lstrip('.').lower()
    if extension:  
        target_path = create_directory_structure(target_dir, extension)
        shutil.copy(file_path, target_path / file_path.name)


def process_directory(source_dir, target_dir):
    with ThreadPoolExecutor() as executor:
        for root, _, files in os.walk(source_dir):
            root_path = Path(root)
            for file_name in files:
                file_path = root_path / file_name
                executor.submit(process_file, file_path, target_dir)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Sort files from source directory to target directory by extensions.")
    parser.add_argument("source", help="Path to source directory with files.")
    parser.add_argument("target", nargs="?", default="dist", help="Path to target directory for sorted files.")
    args = parser.parse_args()

    source_dir = Path(args.source).resolve()
    target_dir = Path(args.target).resolve()

    if not source_dir.is_dir():
        print(f"Error: {source_dir} is not a valid directory.")
        sys.exit(1)

    process_directory(source_dir, target_dir)
    print(f"Files from {source_dir} sorted into {target_dir}.")
