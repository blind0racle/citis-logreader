import customtkinter as ctk
from interface import setup_interface

if __name__ == "__main__":
    app = ctk.CTk()
    setup_interface(app)
    app.mainloop()
