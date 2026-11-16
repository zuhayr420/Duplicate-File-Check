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
