# Coded by Dante

import os
import sys
import shutil
import threading
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def find_python():
    """Dynamically finds the python executable to avoid hardcoded paths."""
    if "python" in os.path.basename(sys.executable).lower():
        return sys.executable
    return shutil.which("python") or shutil.which("python3") or sys.executable

PYTHON_EXE = find_python()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
EX_SCRIPT = os.path.join(SCRIPTS_DIR, "ex.py")


class ModernUnpackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DMC3 PAC Extractor")
        self.geometry("650x550")
        self.resizable(False, False)
        self.eval('tk::PlaceWindow . center')

        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.header_label = ctk.CTkLabel(
            self.main_frame, 
            text="DMC3 PAC Unpacker", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.header_label.pack(pady=(20, 5))

        self.unpack_btn = ctk.CTkButton(
            self.main_frame, 
            text="🔓 Select & Unpack .pac File", 
            font=ctk.CTkFont(size=15, weight="bold"),
            height=45,
            corner_radius=8,
            command=self.start_unpack_process
        )
        self.unpack_btn.pack(pady=15)

        self.console_log = ctk.CTkTextbox(
            self.main_frame, 
            width=580, 
            height=200, 
            corner_radius=8,
            fg_color="#1e1e1e",
            text_color="#a9b7c6",
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.console_log.pack(pady=(5, 15), padx=20)
        self.console_log.insert("0.0", "System idle. Ready to unpack.\n")
        self.console_log.configure(state="disabled")

        self.status_label = ctk.CTkLabel(
            self.main_frame, 
            text="Initializing system checks...", 
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.status_label.pack(pady=(0, 20))

        self.check_system()

    def log_message(self, message):
        """Thread-safe way to append text to the UI console."""
        self.console_log.configure(state="normal")
        self.console_log.insert(tk.END, message + "\n")
        self.console_log.see(tk.END)
        self.console_log.configure(state="disabled")

    def check_system(self):
        """Validates all required dependencies before allowing execution."""
        problems = []
        if not PYTHON_EXE or not os.path.exists(PYTHON_EXE):
            problems.append("Python executable not found in PATH.")
        if not os.path.exists(SCRIPTS_DIR):
            problems.append(f"Missing scripts folder: {SCRIPTS_DIR}")
        if not os.path.exists(EX_SCRIPT):
            problems.append(f"Missing core script: {EX_SCRIPT}")

        if problems:
            self.status_label.configure(text="⚠️ System Error - Check Console", text_color="#ff595e")
            self.unpack_btn.configure(state="disabled", fg_color="gray30")
            for prob in problems:
                self.log_message(f"[ERROR] {prob}")
            return False

        self.status_label.configure(text="✅ System Ready", text_color="#8ac926")
        self.log_message(f"[INFO] Using Python: {PYTHON_EXE}")
        self.log_message(f"[INFO] Script loaded: {EX_SCRIPT}\n")
        return True

    def start_unpack_process(self):
        """Handles file selection and triggers the background thread."""
        if not self.check_system():
            return

        pac_path = filedialog.askopenfilename(
            title="Select a .pac file",
            filetypes=[("PAC files", "*.pac"), ("All files", "*.*")]
        )
        
        if not pac_path:
            return

        self.unpack_btn.configure(state="disabled", text="⏳ Unpacking...")
        self.status_label.configure(text="Processing... Please wait.", text_color="#ffca3a")
        
        self.console_log.configure(state="normal")
        self.console_log.delete("1.0", tk.END)
        self.console_log.configure(state="disabled")

        threading.Thread(target=self.run_extraction, args=(pac_path,), daemon=True).start()

    def run_extraction(self, pac_path):
        """Executes the external python script and captures its output (Runs in background)."""
        pac_dir = os.path.dirname(pac_path)
        pac_name = os.path.basename(pac_path)
        pac_base = os.path.splitext(pac_name)[0]
        out_dir = pac_base + "_extracted"

        self.log_message(f"[START] Unpacking {pac_name}...")
        
        try:
            process = subprocess.Popen(
                [PYTHON_EXE, EX_SCRIPT, pac_name, out_dir],
                cwd=pac_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            for line in process.stdout:
                self.after(0, self.log_message, line.strip())

            process.wait()

            if process.returncode == 0:
                self.after(0, self.extraction_success, out_dir)
            else:
                self.after(0, self.extraction_failed, f"Process exited with code {process.returncode}")

        except Exception as e:
            self.after(0, self.extraction_failed, str(e))

    def extraction_success(self, out_dir):
        """Callback for successful completion."""
        self.log_message(f"\n[SUCCESS] Extracted successfully to: {out_dir}")
        self.status_label.configure(text="✅ Extraction Complete", text_color="#8ac926")
        self.reset_button()

    def extraction_failed(self, error_msg):
        """Callback for extraction failure."""
        self.log_message(f"\n[FATAL ERROR] {error_msg}")
        self.status_label.configure(text="❌ Extraction Failed", text_color="#ff595e")
        self.reset_button()

    def reset_button(self):
        """Re-enables the primary action button."""
        self.unpack_btn.configure(state="normal", text="🔓 Select & Unpack .pac File")


if __name__ == "__main__":
    app = ModernUnpackerApp()
    app.mainloop()