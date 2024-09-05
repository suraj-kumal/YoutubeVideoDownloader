import tkinter as tk
from tkinter import ttk, filedialog, font
import threading
from downloader import video_info, download_video, display_progress

app = tk.Tk()

# Title
app.title("YouTube Video Downloader")

# Get screen size
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# App width and height
app_width = 640
app_height = 480

center_x = int(screen_width / 2 - app_width / 2)
center_y = int(screen_height / 2 - app_height / 2)

app_font = font.Font(family="Arial", size=12)

ttk.Label(app, text="Enter URL:", font=app_font).pack(padx=5, pady=3)

url_box = ttk.Entry(app, font=app_font, width=30)
url_box.pack(padx=5, pady=2)


fetch = None


def display_info():
    destroy_widget(destroyable_widget)

    
    url = url_box.get()
    if url:
        fetch = ttk.Label(app, text="fetching information.......", font=("Arial", 9))
        fetch.pack(padx=10, pady=2)
        app.update()
        title, resolution_list = video_info(url)
        fetch.destroy()
        after_info(title, resolution_list)


download_path = ""
resolution = ""
fill = None
destroyable_widget = []
wait = None


def after_info(title, resolution_list):
    global destroyable_widget
    app_title = ttk.Label(app, text=f"{title}", font=app_font)
    app_title.pack(padx=10, pady=5)
    destroyable_widget.append(app_title)

    def on_select(event):
        global resolution
        resolution = Combobox.get()

    if resolution_list:
        Combobox = ttk.Combobox(app, values=resolution_list)
        def_text = "Select a resolution"
        Combobox.set(def_text)
        Combobox.bind("<<ComboboxSelected>>", on_select)
        Combobox.pack(padx=10, pady=5)
        destroyable_widget.append(Combobox)

        def select_folder():
            global download_path
            folder_selected = filedialog.askdirectory()
            if folder_selected:
                download_path = folder_selected
                folder_label.config(text=folder_selected)

        select_folder_button = ttk.Button(
            app, text="Select Folder", command=select_folder
        )
        select_folder_button.pack(padx=10, pady=5)
        destroyable_widget.append(select_folder_button)

        folder_label = ttk.Label(app, text="No folder selected", font=("Arial", 10))
        folder_label.pack(padx=10, pady=5)
        destroyable_widget.append(folder_label)

        url = url_box.get()

        def download():
            global fill
            if fill:
                fill.destroy()
            if url and resolution and download_path and title:
                download_video(url, resolution, download_path, title, progress_var)

            else:
                fill = ttk.Label(app, text="fill all the information", font=app_font)
                fill.pack(padx=5, pady=2)

        download_button = ttk.Button(
            app,
            text="Download",
            command=lambda: threading.Thread(target=download).start(),
        )
        download_button.pack(padx=10, pady=2)
        destroyable_widget.append(download_button)

        progress_var = tk.StringVar()
        progress_label = ttk.Label(app, textvariable=progress_var, font=("Arial", 10))
        progress_label.pack(padx=10, pady=5)
        destroyable_widget.append(progress_label)


def destroy_widget(destroyable_widget):
    for widget in destroyable_widget:
        widget.destroy()
    destroyable_widget.clear()


submit = ttk.Button(app, text="Enter", command=display_info)
submit.pack(pady=20)


app.geometry(f"{app_width}x{app_height}+{center_x}+{center_y}")

display_frame = ttk.Frame(app)
display_frame.pack(padx=5, pady=5)

app.resizable(width=False, height=False)
app.mainloop()
