import os
import threading
import customtkinter as ctk
from tkinter import filedialog
from .converter import process_batch

# Set appearance mode and color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Batch PDF to MD Converter")
        self.geometry("650x450")
        self.resizable(False, False)

        # Title
        self.title_label = ctk.CTkLabel(
            self, 
            text="PDF to Markdown (RAG-ready)", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(25, 20))

        # Input Frame
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10, padx=20, fill="x")
        
        self.input_label = ctk.CTkLabel(self.input_frame, text="Input (File or Folder):")
        self.input_label.pack(anchor="w", padx=10, pady=(10, 0))
        
        # Input row wrapper
        self.input_row = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.input_row.pack(fill="x", padx=10, pady=10)
        
        self.input_entry = ctk.CTkEntry(self.input_row, placeholder_text="Select a PDF file or folder...")
        self.input_entry.pack(side="left", fill="x", expand=True)
        
        self.btn_browse_file = ctk.CTkButton(self.input_row, text="Browse File", width=100, command=self.browse_input_file)
        self.btn_browse_file.pack(side="left", padx=(10, 0))
        
        self.btn_browse_folder = ctk.CTkButton(self.input_row, text="Browse Folder", width=100, command=self.browse_input_folder)
        self.btn_browse_folder.pack(side="left", padx=(10, 0))

        # Output Frame
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.pack(pady=10, padx=20, fill="x")
        
        self.output_label = ctk.CTkLabel(self.output_frame, text="Output Folder (Optional):")
        self.output_label.pack(anchor="w", padx=10, pady=(10, 0))
        
        # Output row wrapper
        self.output_row = ctk.CTkFrame(self.output_frame, fg_color="transparent")
        self.output_row.pack(fill="x", padx=10, pady=10)
        
        self.output_entry = ctk.CTkEntry(self.output_row, placeholder_text="Default: ~/batch-pdf-to-md")
        self.output_entry.pack(side="left", fill="x", expand=True)
        
        self.btn_browse_output = ctk.CTkButton(self.output_row, text="Browse Folder", width=100, command=self.browse_output_folder)
        self.btn_browse_output.pack(side="left", padx=(10, 0))

        # Convert Button
        self.convert_btn = ctk.CTkButton(
            self, 
            text="Convert to Markdown", 
            font=ctk.CTkFont(size=16, weight="bold"), 
            height=40, 
            command=self.start_conversion
        )
        self.convert_btn.pack(pady=20)
        
        # Status Label
        self.status_label = ctk.CTkLabel(self, text="", text_color="gray")
        self.status_label.pack(pady=5)
        
        # Progress bar (Indeterminate)
        self.progressbar = ctk.CTkProgressBar(self, mode="indeterminate")
        self.progressbar.set(0)
        # We pack it but hide it until conversion starts
        self.progressbar.pack(pady=10, padx=20, fill="x")
        self.progressbar.pack_forget()

    def browse_input_file(self):
        filename = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF files", "*.pdf")])
        if filename:
            self.input_entry.delete(0, 'end')
            self.input_entry.insert(0, filename)

    def browse_input_folder(self):
        folder = filedialog.askdirectory(title="Select Folder containing PDFs")
        if folder:
            self.input_entry.delete(0, 'end')
            self.input_entry.insert(0, folder)

    def browse_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_entry.delete(0, 'end')
            self.output_entry.insert(0, folder)

    def start_conversion(self):
        input_path = self.input_entry.get().strip()
        output_path = self.output_entry.get().strip() or None

        if not input_path:
            self.status_label.configure(text="Please select an input file or folder.", text_color="red")
            return
            
        if not os.path.exists(input_path):
            self.status_label.configure(text="Input path does not exist.", text_color="red")
            return

        self.convert_btn.configure(state="disabled")
        self.status_label.configure(text="Converting... Please wait.", text_color="yellow")
        self.progressbar.pack(pady=10, padx=20, fill="x")
        self.progressbar.start()

        # Run conversion in a separate thread to keep GUI responsive
        threading.Thread(target=self.run_conversion, args=(input_path, output_path), daemon=True).start()

    def run_conversion(self, input_path, output_path):
        try:
            process_batch(input_path, output_path)
            self.after(0, self.conversion_success)
        except Exception as e:
            self.after(0, self.conversion_error, str(e))

    def conversion_success(self):
        self.progressbar.stop()
        self.progressbar.pack_forget()
        self.status_label.configure(text="Conversion completed successfully!", text_color="green")
        self.convert_btn.configure(state="normal")

    def conversion_error(self, error_msg):
        self.progressbar.stop()
        self.progressbar.pack_forget()
        self.status_label.configure(text=f"Error: {error_msg}", text_color="red")
        self.convert_btn.configure(state="normal")

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
