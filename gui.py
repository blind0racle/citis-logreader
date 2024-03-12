import customtkinter as ctk
from customtkinter import filedialog

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title("LogReader by blindoracle")
window.iconbitmap('eye.ico')
window.geometry("900x600")
window.resizable(False,False)

def browse_files():
    filename = filedialog.askopenfilename()
    searchbar.delete(0, ctk.END)
    searchbar.insert(0, filename)

def open_file():
    filepath = searchbar.get()
    # Add code to open the selected file here

# Create the search bar
searchbar = ctk.CTkEntry(window, width=575)
searchbar.grid(row=0, column=0, padx=(10, 5), pady=10)

# Create the "Browse Files" button
browse_btn = ctk.CTkButton(window, text="Browse Files", command=browse_files)
browse_btn.grid(row=0, column=1, padx=5, pady=10)

# Create the "Open" button
open_btn = ctk.CTkButton(window, text="Open", command=open_file)
open_btn.grid(row=0, column=2, padx=5, pady=10)

# Start the main loop
window.mainloop()