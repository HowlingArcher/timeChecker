# #!/usr/bin/env python3

import tkinter as tk
import threading
import time
import platform
import subprocess
import sys
import subprocess
import os
from openpyxl import Workbook
import openpyxl.drawing.image  # Import for adding images to Excel file
import matplotlib.pyplot as plt
from tkinter import messagebox  # Added for message box notifications
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import psutil
import win32gui
import win32process

# Global variables
tracked_apps = {}
tracking_active = False
root = None
already_saved = True

def get_active_window_title():
    if sys.platform.startswith('win'):
        return _get_active_window_title_windows()
    elif sys.platform == 'darwin':
        return _get_active_application_name_macos()
    elif sys.platform.startswith('linux'):
        return _get_active_window_title_linux()
    else:
        raise NotImplementedError("Unsupported platform")

def _get_active_window_title_windows():
    try:
        window = win32gui.GetForegroundWindow()
        _, process_id = win32process.GetWindowThreadProcessId(window)
        process = psutil.Process(process_id)
        process_name = process.name()
        app_name = process_name.split(".exe")[0]
        return app_name
    except ImportError:
        print("pywin32 and psutil modules are required to get active window title on Windows.")
        sys.exit(1)

def _get_active_application_name_macos():
    from AppKit import NSWorkspace
    active_app = NSWorkspace.sharedWorkspace().frontmostApplication()
    app_name = active_app.localizedName()
    return app_name

def _get_active_window_title_linux():
    result = subprocess.run(['xdotool', 'getactivewindow', 'getwindowname'], capture_output=True, text=True)
    return result.stdout.strip()

def export_to_excel(tracked_apps):
    global already_saved
    # Create the 'files' folder if it doesn't exist
    if not os.path.exists("files"):
        os.makedirs("files")

    date_time = time.strftime("%Y-%m-%d-%H-%M")

    # Construct the paths for saving files
    files_folder = "files"
    pie_chart_filename = os.path.join(files_folder, f"pie_chart_{date_time}.png")
    excel_filename = os.path.join(files_folder, f"tracked_apps-{date_time}.xlsx")

    wb = Workbook()
    ws_data = wb.active
    ws_data.append(["Application", "Time Spent (seconds)"])

    for app, time_spent in tracked_apps.items():
        ws_data.append([app, time_spent])
    
    # Create a new worksheet for statistics
    ws_stats = wb.create_sheet(title="Statistics")
    ws_stats.append(["Application", "Time Spent (seconds)"])

    total_time = sum(tracked_apps.values())
    for app, time_spent in tracked_apps.items():
        percentage = (time_spent / total_time) * 100
        ws_stats.append([app, time_spent])
    
    # Create a pie chart
    update_pie_chart(tracked_apps)

    # Save the pie chart as PNG
    plt.savefig(pie_chart_filename)

    # Save the workbook
    wb.save(excel_filename)
    print(f"Tracked data exported to {excel_filename}")

    # Reset the tracked apps
    tracked_apps.clear()
    # Update already_saved to true
    already_saved = True
    # Clear the pie chart
    update_pie_chart(tracked_apps)

    # Show save notification
    folder_name = os.path.abspath(files_folder)
    messagebox.showinfo("Save Notification", f"We have saved your files to {folder_name}")

def update_pie_chart(tracked_apps):
    # Clear the existing plot
    plt.clf()

    # Create the pie chart
    labels = list(tracked_apps.keys())
    sizes = list(tracked_apps.values())

    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title("Time Spent in Applications")
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

def start_tracking(canvas):
    global already_saved
    global tracked_apps, tracking_active
    global root  # Access the global variable root
    
    start_time = time.time()
    already_saved = False

    while tracking_active:
        active_app = get_active_window_title()
        current_time = time.time()
        elapsed_time = current_time - start_time

        if active_app == "":
            active_app = "Unknown or desktop"

        if active_app not in tracked_apps:
            tracked_apps[active_app] = 0

        tracked_apps[active_app] += 1
        start_time = current_time

        print("Tracked Apps:", tracked_apps)
        print("Total Elapsed Time:", elapsed_time)

        # Update the pie chart
        update_pie_chart(tracked_apps)

        # Update the pie chart in the Tkinter application
        canvas.draw_idle()

        time.sleep(1)

def stop_tracking():
    global tracking_active
    tracking_active = False

    # Show stop tracking notification
    messagebox.showinfo("Stop Tracking Notification", "We've stopped tracking your application time")

def save_and_quit():
    global tracking_active
    global already_saved
    tracking_active = False
    if(already_saved == False):
        result = messagebox.askquestion("Quit Confirmation", "Do you want to save your tracked data before quitting?")
        if result == "yes":
            export_to_excel(tracked_apps)
            sys.exit()
        else:
            sys.exit()
    else:
        sys.exit()        

def start_tracking_thread(canvas):
    global tracking_active
    tracking_active = True
    tracking_thread = threading.Thread(target=start_tracking, args=(canvas,))
    tracking_thread.start()

def main():
    global root  # Access the global variable root
    root = tk.Tk()
    root.title("App Usage Tracker")

    icon = tk.PhotoImage(file="favicon.ico")
    root.call('wm', 'iconphoto', root._w, icon)

    # Frame to contain the start and stop buttons
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.TOP, pady=5)

    # Button to start tracking
    start_button = tk.Button(button_frame, text="Start Tracking", command=lambda: start_tracking_thread(canvas))
    start_button.pack(side=tk.LEFT, padx=5)

    # Button to stop tracking
    stop_button = tk.Button(button_frame, text="Stop Tracking", command=stop_tracking)
    stop_button.pack(side=tk.LEFT, padx=5)

    # Create the pie chart with larger size
    fig = plt.figure(figsize=(10, 9))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Button to save tracked data
    save_button = tk.Button(root, text="Save Tracked Data", command=lambda: export_to_excel(tracked_apps))
    save_button.pack(side=tk.BOTTOM, pady=5)

    # Bind the window closing event to save_and_quit
    root.protocol("WM_DELETE_WINDOW", save_and_quit)

    root.mainloop()

if __name__ == "__main__":
    main()
