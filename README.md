# Duplicate File Check

A Python practical project to find duplicate files in a folder and its subfolders by comparing their SHA-256 hash values.

## Aim
To create a Python script that scans a directory recursively, finds duplicate files by checking their content hash (SHA-256), and prints a summary report without deleting or modifying any files.

## Objectives
- Traverse directories and subdirectories using `os.walk()`.
- Read files in chunks (64 KB) so large files don't use up excessive RAM.
- Generate SHA-256 hashes using Python's built-in `hashlib`.
- Group files with matching hashes to identify original vs. duplicate files.
- Calculate the total number of files scanned, number of duplicates, and wasted disk space.
- Handle file permission errors and unreadable files gracefully.

## Introduction
Comparing files by name or size alone is unreliable because two different files can have the same size, and identical files can have different names. This program reads the actual contents of each file and generates a SHA-256 checksum. If two files have the same hash, their contents are identical.

## Technologies Used
- **Language:** Python 3 (standard library only)
- **Built-in Modules:**
  - `os`: For walking the directory tree and checking file sizes.
  - `hashlib`: For generating SHA-256 checksums.
  - `sys`: For handling command-line arguments.
- **Platform:** Works on Windows, Linux, and macOS.

## Working Principle
1. The user provides a directory path.
2. The script walks through all folders and subfolders.
3. Each file is opened in binary mode and read in 64 KB chunks to compute its SHA-256 hash.
4. Hashes are stored in a dictionary: `{hash: [file_path1, file_path2, ...]}`.
5. Any hash with more than one file path is flagged as a duplicate group.
6. The first file in the list is treated as the original, and the rest are treated as duplicates.
7. Total duplicates and wasted storage are calculated and printed to the terminal.

## SHA-256 Hashing
SHA-256 produces a unique 64-character hexadecimal string for any file content. Even if a single character or byte differs, the resulting hash will be completely different. This makes it ideal for finding duplicate files regardless of their filenames or locations.

## Algorithm
1. Take the folder path from the user.
2. Check if the path exists and is a valid directory. If not, show an error and exit.
3. Initialize an empty dictionary for hashes and a counter for scanned files.
4. Use `os.walk()` to visit every file:
   - Increment the file count.
   - Read the file in binary chunks and calculate its SHA-256 hash.
   - If there is a permission error, record it and skip to the next file.
   - Add the file path to the list for that hash in the dictionary.
5. Loop through the dictionary and filter entries with more than one file path.
6. For each duplicate group, calculate the extra space used (`(copies - 1) * file_size`).
7. Print the results (total files, duplicate count, wasted space, and file paths).

## Program Implementation
The code is written in `duplicate_files.py` and split into clean functions:
- `calculate_hash(file_path, chunk_size)`: Reads a file in 64 KB chunks and returns the SHA-256 string. Catches permission or OS errors so the scan doesn't crash.
- `format_storage_size(size_bytes)`: Converts raw bytes into readable B, KB, MB, or GB.
- `find_duplicates(directory)`: Traverses the directory, collects file hashes, and groups duplicates.
- `display_results(results, target_directory)`: Formats and prints the final report.
- `main()`: Handles user input, checks the directory path, and runs the scanner.

## Project Structure
```text
Duplicate-File-Check/
│
├── duplicate_files.py      # Main Python script
├── requirements.txt        # Notes that only standard library is used
├── README.md               # Project documentation
├── .gitignore              # Git ignore file
└── LICENSE                 # License file
```

## How to Run

### Requirements
- Python 3 installed. No extra packages needed.

### Running on Windows (CMD or PowerShell)
1. Open Command Prompt or PowerShell and go to the project folder:
   ```cmd
   cd /d E:\Duplicate-File-Check
   ```

2. Run the script:
   ```cmd
   python duplicate_files.py
   ```

3. Enter the path when prompted:
   ```text
   Enter the directory path to scan for duplicates: C:\Users\Username\Documents\TestFolder
   ```

You can also pass the folder path directly as an argument:
```cmd
python duplicate_files.py "C:\Users\Username\Documents\TestFolder"
```

## Sample Output
```text
============================================================
   PYTHON PRACTICAL: SHA-256 DUPLICATE FILE DETECTOR
============================================================

[*] Scanning directory tree: C:\Users\Username\Documents\TestFolder ...

===========================================================================
                DUPLICATE FILE DETECTION AUDIT REPORT
===========================================================================
Target Directory     : C:\Users\Username\Documents\TestFolder
Total Files Scanned  : 3
Inaccessible Files   : 0
Duplicate Groups     : 1
Total Duplicate Files: 1
Wasted Storage Space : 120.00 KB (122,880 Bytes)
===========================================================================

[+] DUPLICATE FILE GROUPS FOUND:

Group #1:
  SHA-256 Digest : 3a7b8e4f1c9d2a0b5e8f7c6d4a3b2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d
  Individual Size: 120.00 KB (122,880 Bytes)
  Total Copies   : 2
  --> [Original] : C:\Users\Username\Documents\TestFolder\document.pdf
  --> [Duplicate 1]: C:\Users\Username\Documents\TestFolder\subfolder\copy_of_document.pdf
---------------------------------------------------------------------------

AUDIT SUMMARY:
Found 1 redundant duplicate file(s) across 1 distinct group(s).
Reclaimable storage space: 120.00 KB (122,880 Bytes).
No files were modified or deleted.
===========================================================================
```

## Advantages
- **Accurate:** Checks file content instead of just name or extension.
- **Low Memory Usage:** Files are read in 64 KB chunks, so large files won't cause memory issues.
- **Safe:** Strictly read-only; it won't delete or move your files.
- **No Dependencies:** Uses only Python's standard library.

## Limitations
- Scanning very large hard drives can take time depending on disk read speed.
- If there are multiple empty (0-byte) files, they will match as duplicates, but deleting them frees 0 bytes.
- Does not automatically delete files (manual review is required).

## Result
The duplicate file detection program was successfully built and tested. It accurately scans directory structures, identifies duplicate files using SHA-256 hashes, calculates the wasted storage space, and displays a clean summary without altering any files.
