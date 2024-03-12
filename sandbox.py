import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
import plotly.graph_objects as go
import webbrowser
import tempfile
import os
from main import reader

ctk.set_appearance_mode("Light")  # Set the overall appearance/theme
ctk.set_default_color_theme("blue")  # Set the default color theme


# Function to browse for files
def browse_files():
    filename = filedialog.askopenfilename()
    searchbar.delete(0, ctk.END)
    searchbar.insert(0, filename)


# Function to open and display the content of the selected file
def open_file():
    filepath = searchbar.get()
    linenum = 0
    try:
        with open(filepath, 'r') as file_content:
            # Preparing headers
            formatted_content = "{:<10}{:<20}{:<20}{:<30}{:<50}\n".format("Status", "First Date", "Second Date", "Name",
                                                                          "Email")

            for line in file_content:
                linenum += 1
                status, first_date, second_date, name, email = reader(linenum, filepath)

                formatted_line = "{:<10}{:<20}{:<20}{:<30}{:<50}".format(
                    status,
                    first_date,
                    second_date,
                    name,
                    email
                )
                formatted_content += formatted_line + "\n"

            # Displaying the formatted content in CTkTextbox
            log_text_widget.delete("0.0", tk.END)
            log_text_widget.insert("0.0", formatted_content)

    except Exception as e:
        log_text_widget.delete("0.0", tk.END)
        log_text_widget.insert("0.0", f"Error opening file: {str(e)}")


# Function to show a Plotly chart in the default web browser
def show_plotly_chart():
    fig = go.Figure(data=[go.Table(
        header=dict(values=['A Scores', 'B Scores'],
                    line_color='darkslategray',
                    fill_color='lightskyblue',
                    align='left'),
        cells=dict(values=[[100, 90, 80, 90],  # 1st column
                           [95, 85, 75, 95]],  # 2nd column
                   line_color='darkslategray',
                   fill_color='lightcyan',
                   align='left'))
    ])

    fig.update_layout(width=500, height=300)

    # Save the figure as a temporary HTML file and open it in the default web browser
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    fig.write_html(temp.name)
    webbrowser.open('file://' + os.path.realpath(temp.name))


# Initialize the main window with customtkinter
window = ctk.CTk()
window.title("LogReader by blindoracle")
window.geometry("900x630")
window.resizable(False, False)

# GUI elements
searchbar = ctk.CTkEntry(window, width=520)
searchbar.grid(row=0, column=0, padx=10, pady=20)

browse_btn = ctk.CTkButton(window, text="Browse Files", command=browse_files)
browse_btn.grid(row=0, column=1, padx=5, pady=10)

open_btn = ctk.CTkButton(window, text="Open", command=open_file)
open_btn.grid(row=0, column=2, padx=5, pady=10)

show_chart_btn = ctk.CTkButton(window, text="Show Chart", command=show_plotly_chart)
show_chart_btn.grid(row=0, column=3, padx=5, pady=10)

# Replace the Text widget with CTkTextbox for log display
log_text_widget = ctk.CTkTextbox(window, width=860, height=510)
log_text_widget.grid(row=1, column=0, columnspan=4, padx=20, pady=0)

window.mainloop()