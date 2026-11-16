# Duplicate-File-Check: Python SHA-256 Duplicate File Detection

A practical Python program developed to detect duplicate files within any given directory and its subdirectories by computing and comparing cryptographic SHA-256 hash digests.

---

## 1. Project Title
**SHA-256 Cryptographic Duplicate File Detection System**

---

## 2. Project Description
**Duplicate-File-Check** is a lightweight, command-line practical program implemented in Python. It scans target directories recursively, calculates the cryptographic SHA-256 hash digest for each file using buffered binary streams, detects identical files regardless of file names or extensions, and generates an audit report showing scanned file counts, duplicate groups, original vs. duplicate paths, and wasted storage space.

---

## 3. Aim
To design, implement, and test a standalone Python program capable of identifying redundant duplicate files across nested directory structures using cryptographic hashing, ensuring complete file system safety with read-only execution.

---

## 4. Objectives
- Traverse directory trees recursively using standard library file-system traversal.
- Compute SHA-256 cryptographic hashes by streaming file contents in chunks to prevent memory overhead.
- Group identical files into distinct collision-free hash buckets.
- Differentiate between the first encountered copy (original) and subsequent redundant copies (duplicates).
- Quantify total scanned files, redundant duplicate counts, and storage space occupied by duplicate files.
- Provide error handling for unreadable or permission-restricted files.
- Strictly uphold data integrity: never delete, alter, or relocate any files.

---

## 5. Introduction
In file systems, redundant files waste storage capacity, complicate backups, and lead to version confusion. Simple comparison by file name or size is unreliable because distinct files can share identical sizes, while identical files frequently have different names or modified timestamps.

Using a cryptographic hash function like **SHA-256** solves this problem. A cryptographic hash generates a fixed-size 256-bit (64-character hexadecimal) digital fingerprint representing the exact binary contents of a file. If two files produce identical SHA-256 hashes, their contents are mathematically verified to be identical.

---

## 6. Technologies Used
- **Programming Language:** Python 3 (compatible with Python 3.8+)
- **Standard Libraries:**
  - `os`: Recursive directory walking (`os.walk`), path concatenation (`os.path.join`), and file metadata inspection (`os.path.getsize`).
  - `hashlib`: Generation of Secure Hash Algorithm 256-bit (`hashlib.sha256`) digests.
  - `sys`: Command-line argument parsing and input stream handling.
- **Operating Systems Supported:** Windows 10/11, macOS, and Linux.
- **Dependencies:** None (uses 100% Python Standard Library).

---

## 7. Working Principle
The program operates on the principle of **cryptographic content hashing**:
1. It systematically traverses every directory and subdirectory starting from the user-specified root path.
2. For each file encountered, it reads raw binary data in fixed 64 KB blocks and updates an incremental SHA-256 hashing context.
3. The resulting 64-character hexadecimal hash is stored in a hash map where keys are hashes and values are lists of file paths.
4. Any hash key associated with two or more file paths represents a duplicate group.
5. The first path in the group is identified as the **Original**, and all other paths in that group are identified as **Duplicates**.
6. The program sums the file sizes of the duplicate copies to calculate the total recoverable storage space.

---

## 8. SHA-256 Hashing Explanation
**SHA-256 (Secure Hash Algorithm 256-bit)** is a cryptographic hash algorithm designed by the National Security Agency (NSA) and published as a Federal Information Processing Standard (FIPS PUB 180-2).

Key properties utilized in this project:
- **Deterministic:** The exact same input stream will always produce the identical 256-bit output digest.
- **Fixed Output Length:** Always produces a 64-character hexadecimal string, regardless of whether the file is 0 bytes or 100 gigabytes.
- **Avalanche Effect:** Altering even a single bit in a file changes approximately 50% of the output hash bits.
- **Collision Resistance:** It is computationally infeasible to find two distinct files that yield the same SHA-256 hash ($2^{256}$ possible combinations).

---

## 9. Algorithm

```text
Step 1: Start.
Step 2: Accept the target directory path from the user (via CLI argument or interactive input).
Step 3: Validate the directory path:
        3.1 If path is empty, not found, or not a directory -> display error and terminate.
        3.2 Otherwise, convert path to absolute canonical path.
Step 4: Initialize:
        - hash_map = empty dictionary
        - inaccessible_files = empty list
        - scanned_count = 0
Step 5: Traverse the directory using os.walk(directory):
        For each directory root, and for each filename:
            5.1 Increment scanned_count by 1.
            5.2 Construct full file path.
            5.3 Try to calculate SHA-256 hash using chunked binary reading (64 KB chunks).
            5.4 If a PermissionError or OSError occurs:
                Add full path to inaccessible_files list.
                Continue to next file.
            5.5 If hash is calculated:
                Append full path to hash_map[hash].
Step 6: Identify duplicates:
        Initialize duplicate_groups = empty dictionary
        Initialize total_duplicates = 0
        Initialize wasted_bytes = 0
        For each (hash, file_list) in hash_map:
            If length(file_list) > 1:
                duplicate_groups[hash] = file_list
                redundant_copies = length(file_list) - 1
                total_duplicates += redundant_copies
                wasted_bytes += redundant_copies * size_of(file_list[0])
Step 7: Display results:
        7.1 Print summary metrics (scanned files, duplicate count, wasted storage).
        7.2 If inaccessible files exist, print their paths.
        7.3 If no duplicate groups exist, print success message.
        7.4 For each duplicate group, print SHA-256 digest, file size, original path, and duplicate paths.
Step 8: Stop.
```

---

## 10. Program Implementation Explanation
The program is modularly organized in `duplicate_files.py`:

- **`calculate_hash(file_path, chunk_size=65536)`:**
  Opens files in binary read mode (`"rb"`). Reads data in 64 KB blocks (`65536` bytes) using a `while` loop until EOF. This chunked approach ensures that even multi-gigabyte files can be hashed with minimal RAM consumption. Catches `PermissionError`, `FileNotFoundError`, and `OSError` without terminating the scan.

- **`format_storage_size(size_bytes)`:**
  Converts numeric raw byte totals into human-readable units (`Bytes`, `KB`, `MB`, `GB`) for clear reporting.

- **`find_duplicates(directory)`:**
  Orchestrates directory traversal using `os.walk()`. Populates the hash map, detects groups where `len(files) > 1`, and tallies duplicate counts and wasted bytes.

- **`display_results(results, target_directory)`:**
  Prints a clean academic report to `stdout`. Clearly demarcates original copies from secondary duplicates and highlights potential recoverable disk space.

- **`main()`:**
  Serves as the entry point. Accepts directory paths interactively or via `sys.argv[1]`, strips unnecessary quotation marks, verifies directory existence, and triggers the detection workflow.

---

## 11. Project Structure
```text
Duplicate-File-Check/
│
├── duplicate_files.py      # Main practical program containing hashing & duplicate detection
├── requirements.txt        # Academic dependency declaration (standard libraries only)
├── README.md               # Detailed academic project documentation
├── .gitignore              # Standard Git exclusion file
└── LICENSE                 # Educational project license
```

---

## 12. Installation Instructions

### Prerequisites
- Python 3.8 or higher installed on your computer.
- Git (optional, for cloning).

### Setup
1. Clone the repository or download the source files:
   ```bash
   git clone https://github.com/zuhayr420/Duplicate-File-Check.git
   cd Duplicate-File-Check
   ```

2. Confirm Python is installed and added to your system PATH:
   ```cmd
   python --version
   ```

3. No third-party package installation is required because only Python standard libraries are used.

---

## 13. Execution Instructions

### Windows Command Prompt (CMD)
1. Open Windows Command Prompt (`Win + R`, type `cmd`, press Enter).
2. Navigate to the project directory:
   ```cmd
   cd /d E:\Duplicate-File-Check
   ```
3. Run interactively:
   ```cmd
   python duplicate_files.py
   ```
   When prompted:
   ```cmd
   Enter the directory path to scan for duplicates: C:\Users\Username\Documents\MyFolder
   ```
4. Or pass the folder path directly as a command-line argument:
   ```cmd
   python duplicate_files.py "C:\Users\Username\Documents\MyFolder"
   ```

### Windows PowerShell
```powershell
Set-Location "E:\Duplicate-File-Check"
python duplicate_files.py "C:\Users\Username\Documents\MyFolder"
```

### Linux / macOS Terminal
```bash
python3 duplicate_files.py /path/to/target/directory
```

---

## 14. Sample Input
A directory containing three files:
- `document.pdf` (Original PDF report, 120 KB)
- `copy_of_document.pdf` (Identical copy placed in a subfolder, 120 KB)
- `notes.txt` (Unique text file, 4 KB)

User input:
```text
Enter the directory path to scan for duplicates: C:\Projects\SampleData
```

---

## 15. Expected Output

```text
============================================================
   PYTHON PRACTICAL: SHA-256 DUPLICATE FILE DETECTOR
============================================================

[*] Scanning directory tree: C:\Projects\SampleData ...

===========================================================================
                DUPLICATE FILE DETECTION AUDIT REPORT
===========================================================================
Target Directory     : C:\Projects\SampleData
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
  --> [Original] : C:\Projects\SampleData\document.pdf
  --> [Duplicate 1]: C:\Projects\SampleData\subfolder\copy_of_document.pdf
---------------------------------------------------------------------------

AUDIT SUMMARY:
Found 1 redundant duplicate file(s) across 1 distinct group(s).
Reclaimable storage space: 120.00 KB (122,880 Bytes).
Security Guarantee: No files were modified or deleted.
===========================================================================
```

---

## 16. Advantages
1. **Mathematical Accuracy:** Compares file contents byte-by-byte via SHA-256 rather than superficial metadata (such as file names or modification dates).
2. **Memory Efficiency:** Chunked reading (64 KB buffer) allows processing of files of arbitrary size without memory exhaustion.
3. **Data Safety:** The program operates in strictly read-only mode and never deletes or alters files.
4. **Zero External Dependencies:** Runs natively on any computer with Python 3.
5. **Cross-Platform Compatibility:** Works on Windows, Linux, and macOS without code modifications.

---

## 17. Limitations
1. **I/O Bound:** Scanning very large drives (e.g., hundreds of gigabytes) is bounded by physical disk read speeds.
2. **Identical Empty Files:** Multiple 0-byte files generate the identical SHA-256 digest (`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`) and are correctly grouped, but reclaiming them recovers 0 bytes of storage.
3. **Read-Only Scope:** The program reports duplicates but intentionally does not provide automated deletion or hard-linking to protect users from unintentional data loss.

---

## 18. Result
The Python duplicate file detection program was successfully implemented and verified. The program accurately identifies identical files across nested subdirectories using SHA-256 hashing, groups duplicate copies, calculates reclaimable storage space, handles unreadable files safely, and outputs a formatted academic audit report.
