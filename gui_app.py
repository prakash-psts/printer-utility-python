# import tkinter as tk
# import pystray
# from PIL import Image
# import requests
# from io import BytesIO
# import threading
# import subprocess
# import os

# class TrayApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.withdraw()  # Hide the main window
        
#         self.icon_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Flat_tick_icon.svg/512px-Flat_tick_icon.svg.png?20170316053531"  # Replace with your actual icon URL
        
#         self.tray = pystray.Icon("name", self.get_icon(), "Bsmart util", self.get_menu())
#         self.tray.run()
        
#         self.server_process = None

#     def get_icon(self):
#         response = requests.get(self.icon_url)
#         icon_image = Image.open(BytesIO(response.content))
#         return icon_image

#     def start_server(self):
#         if self.server_process is None:
#             self.server_process = subprocess.Popen(['python', 'main.py'])

#     def stop_server(self):
#         if self.server_process:
#             # Implement a way to stop the server gracefully (e.g., sending a shutdown request)
#             os.kill(self.server_process.pid, signal.SIGTERM)
#             self.server_process = None
        
#     def get_menu(self):
#         menu = (
#             pystray.MenuItem('Start Server', self.start_server),
#             pystray.MenuItem('Stop Server', self.stop_server),
#             pystray.MenuItem('Exit', self.exit_app)
#         )
#         return menu
        
#     def exit_app(self, icon, item):
#         if self.server_process:
#             self.stop_server()
#         icon.stop()
#         self.root.destroy()
        
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = TrayApp(root)
#     root.mainloop()


import tkinter as tk
import pystray
from PIL import Image
import requests
from io import BytesIO
import threading
import subprocess
import os
import signal

class TrayApp:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()  # Hide the main window
        
        self.icon_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Flat_tick_icon.svg/512px-Flat_tick_icon.svg.png?20170316053531"  # Replace with your actual icon URL
        
        self.tray = pystray.Icon("name", self.get_icon(), "Title", self.get_menu())
        self.tray.run()
        
        # self.server_process = None

    def get_icon(self):
        response = requests.get(self.icon_url)
        icon_image = Image.open(BytesIO(response.content))
        return icon_image

    def start_server(self):
        # if self.server_process is None:
            self.server_process = subprocess.Popen(['python', 'main.py'])

    def stop_server(self):
        if self.server_process:
            # Implement a way to stop the server gracefully (e.g., sending a shutdown request)
            os.kill(self.server_process.pid, signal.SIGTERM)
            self.server_process = None
        
    def get_menu(self):
        menu = (
            pystray.MenuItem('Start Server', self.start_server),
            pystray.MenuItem('Stop Server', self.stop_server),
            pystray.MenuItem('Exit', self.exit_app)
        )
        return menu
        
    def exit_app(self, icon, item):
        if self.server_process:
            self.stop_server()
        icon.stop()
        self.root.destroy()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = TrayApp(root)
    root.mainloop()
