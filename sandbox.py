import tkinter as tk
from tkinter import Canvas, Entry, Frame, END
import customtkinter as ctk  # Ensure customtkinter is installed and imported

ctk.set_appearance_mode("Light")


class CustomTkinterTable:
    def __init__(self, root, data, width=600, height=300, border_color='light slate gray', border_thickness=2):
        # Define dimensions for the inner frame, reducing size based on border thickness
        inner_width = width - border_thickness * 1
        inner_height = height + border_thickness*6

        # Outer frame acting as the border
        self.outer_frame = ctk.CTkFrame(root, width=width, height=height, fg_color=border_color)
        self.outer_frame.pack(pady=20, padx=20)  # Add padx to ensure the border is visible all around

        # Inner 'frame' for the content
        self.frame = ctk.CTkFrame(self.outer_frame, width=inner_width, height=inner_height)
        self.frame.place(x=border_thickness, y=border_thickness)  # Adjust placement to simulate border

        self.canvas = Canvas(self.frame, width=inner_width - 20, height=inner_height - 20,)
        self.scrollbar = ctk.CTkScrollbar(self.frame, orientation="vertical")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.canvas.yview)

        self.scrollable_frame = Frame(self.canvas,)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind mousewheel event to the canvas for scrolling
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)

        self.build_table(data)




if __name__ == "__main__":  # Corrected to __name__
    root = ctk.CTk()
    root.title("CustomTkinter Table with Scrollbar")
    root.geometry("800x600")

    data = [["Row %d, Column %d" % (i, j) for j in range(5)] for i in range(50)]

    table = CustomTkinterTable(root, data, width=700, height=400)

    root.mainloop()
