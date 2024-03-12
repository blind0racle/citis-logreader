import tkinter as tk
from cefpython3 import cefpython as cef
import sys
import plotly.express as px
import os


def create_plotly_chart(html_filename='plotly_chart.html'):
    # Create a sample Plotly chart
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")

    # Save the figure as an HTML file
    fig.write_html(html_filename)


def on_configure(event, browser):
    # Resize the browser when the window is resized
    browser.SetBounds(0, 0, event.width, event.height)


def embed_browser(frame):
    # Set CEF browser settings
    window_info = cef.WindowInfo(frame.winfo_id())
    window_info.SetAsChild(frame.winfo_id(), [0, 0, 900, 600])

    # Create a Plotly chart as an HTML file
    html_filename = 'plotly_chart.html'
    create_plotly_chart(html_filename)

    # Create CEF browser instance to display the HTML file
    browser = cef.CreateBrowserSync(window_info, url=os.path.abspath(html_filename))

    # Bind configure event to resize browser with the window
    frame.bind("<Configure>", lambda event: on_configure(event, browser))


def main():
    cef.Initialize()

    # Create the Tkinter window
    root = tk.Tk()
    root.geometry("900x600")

    # Create a frame to embed the browser
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    # Embed the browser in the frame
    embed_browser(frame)

    root.mainloop()
    cef.Shutdown()


if __name__ == '__main__':
    main()
