import tkinter as tk
import pystray
from PIL import Image
import requests
from io import BytesIO
import threading
import subprocess
import os
import signal
from tkinter import messagebox
import psutil
from plyer import notification

# Global variable to track the service status
service_running = False
server_file = "PrinterUtility.py"
stop_event = threading.Event()
server_thread = None


class TrayApp:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()  # Hide the main window
        self.tray = pystray.Icon(
            "name", self.get_icon(), "B smart printer utility", self.get_menu())
        self.tray.run(setup=self.start_server())
        self.server_process = None
    
    stop_event = threading.Event()
    
    def get_icon(self):
        # response = requests.get(self.icon_url)
        # icon_image = Image.open(BytesIO(response.content))
        icon_image = Image.open('b_smart.png')
        return icon_image

    def start_server(self):
        global service_running, server_thread
        if not service_running:
            notify()

            # Create a new thread for starting the server
            server_thread = threading.Thread(target=self.start_server_thread)
            server_thread.daemon = True  # Daemonize the thread
            server_thread.start()
        else:
            messagebox.showerror("Error", "Server already running.")

    def start_server_thread(self):
        global service_running
        try:
            service_running = True
            print("Service started")
            subprocess.check_call(["python", server_file], shell=True)
            messagebox.showinfo("Service Installation",
                                "Service has been started.")
        except subprocess.CalledProcessError as e:
            print(f"Error starting service: {e}")
            messagebox.showerror("Error", "Failed to start the service.")

    def stop_server(self):
        global service_running, server_thread
        if service_running:
            try:
                # self.stop_flask_server()  # Call the method to stop the Flask server
                # self.killProcess()
                # stop_event.set()
                # server_thread.join()
                print("Server stopped")
                service_running = False
                messagebox.showinfo(
                    "Server Stop", "Server has been stopped.")
            except subprocess.CalledProcessError as e:
                print(f"Error stopping service: {e}")
                messagebox.showerror("Error", "Failed to stop the service.")
        else:
            messagebox.showinfo(
                "Error", "Server does not running.")

    def killProcess(self):
        response = -1
        processId = -1
        process = os.popen(
            "netstat -ano | findstr :32568|| findstr LISTENING").read()
        if len(process.split("\n")) > 1:
            arr = process.split("\n")
            print(arr, 'process')
            for str in arr:
                subArr = str.split(" ")
                processId = subArr[len(subArr)-1]
                print(processId, 'processId')
                response = os.system("taskkill /F /PID "+processId)
            pass
        else:
            print(str, 'subArr')
            arr = process.split(" ")
            processId = arr[len(arr)-1]
            response = os.system("taskkill /F /PID "+processId)
            pass
        # return response

    def find_flask_server_process():
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if 'python' in process.info['name']:
                cmdline = ' '.join(process.cmdline())
                if 'PrinterUtility.py' in cmdline:  # Replace with your Flask script filename
                    return process

    def stop_flask_server(self):
        flask_process = self.find_flask_server_process()
        if flask_process:
            print(f"Found Flask server process (PID {
                  flask_process.info['pid']}). Stopping...")
            flask_process.terminate()
        else:
            print("Flask server process not found.")

    def get_menu(self):
        menu = (
            pystray.MenuItem('Start Server', self.start_server),
            # pystray.MenuItem('Stop Server', self.stop_server),
            pystray.MenuItem('Exit', self.exit_app)
        )
        return menu

    def exit_app(self, icon, item):
        try:
            # self.stop_server()
            icon.stop()
            self.root.destroy()
        except:
            icon.stop()
            self.root.destroy()


def notify():
    notification.notify(
        title="Bsmart Printer Utility Server Started",
        message="Please check system tray.",
        timeout=5  # Notification will auto-dismiss after 5 seconds
    )


if __name__ == "__main__":
    root = tk.Tk()
    app = TrayApp(root)
    root.mainloop()
