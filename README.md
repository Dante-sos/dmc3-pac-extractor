# DMC3 PAC Extractor

## Overview

The **DMC3 PAC Extractor is a modern, reliable application designed to extract Devil May Cry 3 ```.pac``` archive files. Built strictly for stability and efficiency by utilizing native Python subprocess execution and asynchronous multithreading. This ensures that the user interface remains fully responsive while heavy extraction processes occur in the background.

## Features

- **Modern Interface:** Utilizes `customtkinter` for a clean, dark-themed user experience.    
- **Integrated Console Logging:** Streams standard output and standard errors directly into the application's built-in text console. No external command-line windows will intrude on your workspace.
- **Asynchronous Processing:** File extraction runs on a dedicated background thread, preventing UI freezing or application lockups.
- **Dynamic Dependency Validation:** Automatically scans system variables to locate the optimal Python executable and verifies the integrity of required local directories before allowing execution.

## Prerequisites

To operate this software, the host system must have the following installed:
1. **Python 3.x** (Ensure Python is added to your system PATH during installation).
2. **CustomTkinter** (The UI library framework).

To install the required library, open your system terminal or command prompt and execute:

Bash

```
pip install customtkinter
```

## Directory Structure Requirement

For the application to pass its initial system check, your folder structure must be strictly organized as follows:

```
/Your_Project_Folder
|-- main_tool.py       (This main application script)
|-- /scripts
    |-- ex.py             (The core extraction script required for processing)
```

_Note: The script specifically looks for `scripts/ex.py` relative to the main application file. If this file or directory is missing, the application will disable the unpack button to prevent execution failures._

## Usage Instructions

1. **Launch the Application:**    
    Execute the main Python script from your terminal or by double-clicking the file (if configured to run via Python on your operating system).

    Bash
    
    ```
    python main_tool.py
    ```
    
2. **Verify System Status:**
    Upon launch, observe the status text above the primary action button. It must read "System Ready". If it indicates an error, consult the built-in console log to identify the missing dependency.
    
3. **Initiate Extraction:**
    Click the "Select & Unpack .pac File" button. A standard file dialog will appear.
    
4. **Select the Archive:**
    Navigate to your Devil May Cry 3 directory (or backup location) and select the target `.pac` file.
    
5. **Monitor Progress:**
    The application will transition to a "Processing" state. Do not close the window. You can monitor the live output of the extraction process directly within the application's console log.
    
6. **Locate Extracted Files:**
    Upon a successful extraction message in the console, navigate to the directory where your original `.pac` file is located. A new folder named `[filename]_extracted` will have been generated containing your assets.
## Frequently Asked Questions (Q&A)

**Q: The application says "System Error - Check Console" upon startup. What should I do?**

**A:** Review the text inside the dark console box. This error typically occurs for two reasons:
1. Python is not correctly registered in your system's PATH variables.
2. The `scripts` folder or the `ex.py` file is missing from the directory where the main application is located. Ensure the folder structure matches the requirements detailed above.

---

**Q: Why does the application console say "Process exited with code 1" during extraction?**

**A:** Exit code 1 indicates that the underlying core script (`ex.py`) encountered a fatal error. This usually means the selected `.pac` file is corrupted, encrypted differently than expected, or the user lacks read/write permissions for the directory where the file is stored.

---

**Q: Will the application freeze if I unpack an exceptionally large archive?**

**A:** No. The extraction engine operates on a background daemon thread. The UI will remain fully interactive, and you can scroll through the console log in real-time as the large file processes.

---

**Q: Can I queue multiple `.pac` files at once?**

**A:** In the current iteration, files must be unpacked sequentially. Wait for the success or failure confirmation of the current file before clicking the button to select the next archive.

---  

**Q: Are my original `.pac` files modified or deleted during this process?**

**A:** No. The extraction process is strictly a "read" operation on the original `.pac` file. All extracted data is written to a completely new folder, leaving your original archive perfectly intact.

---

**Q: Is a command prompt window supposed to pop up when I click unpack?**

**A:** No. By design, this application sets `subprocess.CREATE_NO_WINDOW` on Windows operating systems and pipes all standard output to the internal UI. If an external window appears, it is likely due to an abnormal operating system configuration bypassing standard subprocess flags.
