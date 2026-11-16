"""
Duplicate File Detection Program
=================================
A practical Python program that scans a specified directory and all its subdirectories
to detect duplicate files by computing and comparing their cryptographic SHA-256 hash values.
"""

import os
import hashlib
import sys


def calculate_hash(file_path, chunk_size=65536):
    """
    Calculate the SHA-256 cryptographic hash of a file.

    Parameters:
        file_path (str): Path to the target file.
        chunk_size (int): Byte size of chunks read during each iteration (default: 64 KB).

    Returns:
        str: 64-character hexadecimal SHA-256 digest string, or None if reading fails.
    """
    sha256_hasher = hashlib.sha256()
    try:
        with open(file_path, "rb") as file_handle:
            while True:
                data_chunk = file_handle.read(chunk_size)
                if not data_chunk:
                    break
                sha256_hasher.update(data_chunk)
        return sha256_hasher.hexdigest()
    except (PermissionError, FileNotFoundError, OSError):
        return None


def find_duplicates(directory):
    """
    Traverse a directory recursively and identify all duplicate files by SHA-256 hash.

    Parameters:
        directory (str): The root directory to scan.

    Returns:
        dict: Summary dictionary containing scan results and duplicate groups.
    """
    hash_map = {}
    inaccessible_files = []
    scanned_count = 0

    for current_root, _, filenames in os.walk(directory):
        for filename in filenames:
            full_path = os.path.join(current_root, filename)
            scanned_count += 1

            file_hash = calculate_hash(full_path)
            if file_hash is None:
                inaccessible_files.append(full_path)
                continue

            if file_hash not in hash_map:
                hash_map[file_hash] = []
            hash_map[file_hash].append(full_path)

    duplicate_groups = {}
    total_duplicates = 0
    wasted_bytes = 0

    for file_hash, file_paths in hash_map.items():
        if len(file_paths) > 1:
            duplicate_groups[file_hash] = file_paths
            redundant_count = len(file_paths) - 1
            total_duplicates += redundant_count

            try:
                single_copy_size = os.path.getsize(file_paths[0])
            except (OSError, FileNotFoundError):
                single_copy_size = 0
            wasted_bytes += redundant_count * single_copy_size

    return {
        "scanned_count": scanned_count,
        "duplicate_groups": duplicate_groups,
        "total_duplicates": total_duplicates,
        "wasted_bytes": wasted_bytes,
        "inaccessible_files": inaccessible_files,
    }
