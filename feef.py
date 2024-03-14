import tkinter as tk
from tkinterweb import HtmlFrame  # Import the HTML browser
import plotly.graph_objects as go
import tempfile
import os

# Step 1: Create a Plotly table and convert it to HTML string
fig = go.Figure(data=[go.Table(
    header=dict(values=['A Scores', 'B Scores'],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[[100, 90, 80, 90], [95, 85, 75, 95]],
               fill_color='lavender',
               align='left'))
])

# Convert the figure to HTML
fig_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

# Step 2: Write the HTML to a temporary file
temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w')
temp_file.write(fig_html)
temp_file.close()

# Step 3: Use tkinterweb to display the HTML
root = tk.Tk()  # Create the tkinter window
frame = HtmlFrame(root)  # Create HTML browser

# Load the temporary HTML file into the HtmlFrame
frame.load_file(temp_file.name)
frame.pack(fill="both", expand=True)  # Attach the HtmlFrame widget to the parent window

root.mainloop()

# Cleanup the temporary file after the GUI is closed
os.unlink(temp_file.name)
