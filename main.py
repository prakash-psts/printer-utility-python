
import win32serviceutil
import win32service
import servicemanager
import sys
import os
import os.path
import multiprocessing
import subprocess
from tkinter import messagebox

from flask import Flask, jsonify

# from app import app

app = Flask(__name__)


service_name = 'BsmartPrinterService'  # Replace with the actual service name
# try:
#     result = subprocess.run(['sc', 'query', service_name],
#                             capture_output=True, text=True, check=True)
#     print("Service is already installed.")
# except subprocess.CalledProcessError:
#     # The service doesn't exist, so install it
#     install_command = ['python', 'main.py', 'install']
#     try:
#         install_result = subprocess.run(
#             install_command, capture_output=True, text=True, check=True)
#         print("Service installed successfully.")
#     except subprocess.CalledProcessError as e:
#         print("Error installing the service:", e.stderr)
#


def main():
    messagebox.showinfo("Service installed",
                        "Please check system tray and click start server")
    subprocess.check_call(["python", 'gui_app.py'], shell=True)


class ProcessService(win32serviceutil.ServiceFramework):
    _svc_name_ = "BsmartPrinterService"
    _svc_display_name_ = "Bsmart Printer Service"
    _svc_description_ = "Printer utility"
    _exe_name_ = sys.executable  # python.exe from venv
    _exe_args_ = '-u -E "' + os.path.abspath(__file__) + '"'

    proc = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        if self.proc:
            self.proc.terminate()

    def SvcRun(self):
        self.proc = multiprocessing.Process(target=main)
        self.proc.start()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.SvcDoRun()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)

    def SvcDoRun(self):
        self.proc.join()


def start():
    if len(sys.argv) == 1:
        import win32traceutil
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ProcessService)
        servicemanager.StartServiceCtrlDispatcher()
    elif 'start' in sys.argv:
        main()
    else:
        win32serviceutil.HandleCommandLine(ProcessService)


if __name__ == '__main__':
    try:
        start()
    except (SystemExit, KeyboardInterrupt):
        raise
    except:
        import traceback
        traceback.print_exc()
