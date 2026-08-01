import os
import threading
import platform
import subprocess
import customtkinter as ctk
from tkinter import filedialog
from .converter import process_batch

# Setup appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Light Purple color for primary actions as requested
PURPLE_PRIMARY = "#BA68C8"
PURPLE_HOVER = "#AB47BC"

class ModernMessageBox(ctk.CTkToplevel):
    def __init__(self, parent, title, message, btn_color=PURPLE_PRIMARY):
        super().__init__(parent)
        self.title(title)
        self.geometry("450x220")
        self.resizable(False, False)
        
        # Make the window modal (blocks interaction with the main window)
        self.grab_set()
        self.transient(parent)
        
        # Message Label
        self.label = ctk.CTkLabel(self, text=message, font=ctk.CTkFont(family="Roboto", size=16), wraplength=400)
        self.label.pack(pady=(40, 20), padx=20, expand=True, fill="both")
        
        # OK Button
        self.btn = ctk.CTkButton(self, text="OK", width=120, height=40, font=ctk.CTkFont(family="Roboto", size=16, weight="bold"), command=self.destroy, fg_color=btn_color)
        self.btn.pack(pady=(0, 20))
        
        # Center the dialog on screen
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Batch PDF to MD Converter")
        self.geometry("750x550")
        self.resizable(False, False)
        
        self.input_path = ""
        self.output_dir = ""
        
        # Define fonts
        self.title_font = ctk.CTkFont(family="Roboto", size=32, weight="bold")
        self.btn_font = ctk.CTkFont(family="Roboto", size=16, weight="bold")
        self.label_font = ctk.CTkFont(family="Roboto", size=16)
        self.path_font = ctk.CTkFont(family="Roboto", size=14, slant="italic")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        self.title_label = ctk.CTkLabel(self, text="PDF to Markdown Converter", font=self.title_font, text_color=PURPLE_PRIMARY)
        self.title_label.pack(pady=(40, 30))
        
        # Main Card Frame for Inputs
        self.card_frame = ctk.CTkFrame(self, corner_radius=15)
        self.card_frame.pack(pady=10, padx=40, fill="both", expand=True)
        
        # Input Section
        self.input_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.input_frame.pack(pady=(30, 15), padx=30, fill="x")
        
        self.input_btn_file = ctk.CTkButton(self.input_frame, text="Select PDF File", font=self.btn_font, height=40, width=140, command=self.select_input_file)
        self.input_btn_file.pack(side="left", padx=(0, 10))
        
        self.input_btn_folder = ctk.CTkButton(self.input_frame, text="Select Folder", font=self.btn_font, height=40, width=140, command=self.select_input_dir)
        self.input_btn_folder.pack(side="left", padx=(0, 20))
        
        self.input_label = ctk.CTkLabel(self.input_frame, text="No input selected", text_color="gray", font=self.path_font, wraplength=280, justify="left")
        self.input_label.pack(side="left")
        
        # Output Section
        self.output_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.output_frame.pack(pady=(15, 30), padx=30, fill="x")
        
        self.output_btn = ctk.CTkButton(self.output_frame, text="Output Folder (Opt)", font=self.btn_font, height=40, width=290, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.select_output_dir)
        self.output_btn.pack(side="left", padx=(0, 20))
        
        self.output_label = ctk.CTkLabel(self.output_frame, text="Default: ~/batch-pdf-to-md", text_color="gray", font=self.path_font, wraplength=280, justify="left")
        self.output_label.pack(side="left")
        
        # Margin Option
        self.checkbox_margins = ctk.CTkCheckBox(self.card_frame, text="Ignore Headers & Footers", font=self.label_font, fg_color=PURPLE_PRIMARY, hover_color=PURPLE_HOVER)
        self.checkbox_margins.pack(pady=(0, 20), padx=30, anchor="w")
        
        # Progress Section
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.pack(pady=(10, 30), padx=40, fill="x")
        
        self.progress_label = ctk.CTkLabel(self.progress_frame, text="Ready to convert", font=self.label_font)
        self.progress_label.pack(pady=(0, 10))
        
        self.progressbar = ctk.CTkProgressBar(self.progress_frame, height=15, corner_radius=10, progress_color=PURPLE_PRIMARY)
        self.progressbar.pack(fill="x")
        self.progressbar.set(0)
        self.progressbar.pack_forget()
        
        # Convert Button
        self.convert_btn = ctk.CTkButton(self, text="Start Conversion", font=ctk.CTkFont(family="Roboto", size=22, weight="bold"), height=60, width=300, fg_color=PURPLE_PRIMARY, hover_color=PURPLE_HOVER, command=self.start_conversion)
        self.convert_btn.pack(pady=(0, 40))
        
    def ask_directory(self, title):
        if platform.system() == "Linux":
            try:
                # Use native GTK dialog on Linux via zenity for a modern look
                result = subprocess.run(["zenity", "--file-selection", "--directory", f"--title={title}"], capture_output=True, text=True)
                if result.returncode == 0:
                    return result.stdout.strip()
                elif result.returncode == 1:
                    return "" # User cancelled
            except FileNotFoundError:
                pass # Zenity not found, fallback to tkinter
                
        # Fallback to default tkinter dialog
        return filedialog.askdirectory(title=title)
        
    def ask_file(self, title):
        if platform.system() == "Linux":
            try:
                # Use native GTK dialog on Linux via zenity for a modern look
                result = subprocess.run(["zenity", "--file-selection", f"--title={title}", "--file-filter=*.pdf"], capture_output=True, text=True)
                if result.returncode == 0:
                    return result.stdout.strip()
                elif result.returncode == 1:
                    return "" # User cancelled
            except FileNotFoundError:
                pass # Zenity not found, fallback to tkinter
                
        # Fallback to default tkinter dialog
        return filedialog.askopenfilename(title=title, filetypes=[("PDF files", "*.pdf")])

    def select_input_file(self):
        filepath = self.ask_file("Select Input PDF File")
        if filepath:
            self.input_path = filepath
            self.input_label.configure(text=self.input_path, text_color=("black", "white"))

    def select_input_dir(self):
        directory = self.ask_directory("Select Input Folder")
        if directory:
            self.input_path = directory
            self.input_label.configure(text=self.input_path, text_color=("black", "white"))
            
    def select_output_dir(self):
        directory = self.ask_directory("Select Output Folder")
        if directory:
            self.output_dir = directory
            self.output_label.configure(text=self.output_dir, text_color=("black", "white"))
            
    def conversion_thread(self):
        out_dir = self.output_dir if self.output_dir else None
        margins = (0, 72, 0, 72) if self.checkbox_margins.get() else (0, 0, 0, 0)
        
        try:
            process_batch(self.input_path, out_dir, margins=margins)
            
            def finalize_ui():
                self.progressbar.stop()
                self.progressbar.pack_forget()
                self.progress_label.configure(text="Done! Successfully converted files.")
                self.convert_btn.configure(state="normal", fg_color=PURPLE_PRIMARY)
                self.input_btn_file.configure(state="normal")
                self.input_btn_folder.configure(state="normal")
                self.output_btn.configure(state="normal")
                
                # Show success modern dialog
                ModernMessageBox(self, "Conversion Complete", "Successfully converted the PDF file(s).", btn_color="#28a745")
                
            self.after(0, finalize_ui)
            
        except Exception as e:
            def error_ui():
                self.progressbar.stop()
                self.progressbar.pack_forget()
                self.progress_label.configure(text="Error occurred during conversion.")
                self.convert_btn.configure(state="normal", fg_color=PURPLE_PRIMARY)
                self.input_btn_file.configure(state="normal")
                self.input_btn_folder.configure(state="normal")
                self.output_btn.configure(state="normal")
                
                # Show error modern dialog
                ModernMessageBox(self, "Error", f"An unexpected error occurred:\n{str(e)}", btn_color="#dc3545")
                
            self.after(0, error_ui)

    def start_conversion(self):
        if not self.input_path:
            ModernMessageBox(self, "Warning", "Please select an input file or folder first.", btn_color="#ffc107")
            return
            
        # Disable buttons during conversion
        self.convert_btn.configure(state="disabled", fg_color="gray")
        self.input_btn_file.configure(state="disabled")
        self.input_btn_folder.configure(state="disabled")
        self.output_btn.configure(state="disabled")
        
        self.progressbar.pack(fill="x")
        self.progressbar.start()
        self.progress_label.configure(text="Starting conversion...")
        
        threading.Thread(target=self.conversion_thread, daemon=True).start()

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
