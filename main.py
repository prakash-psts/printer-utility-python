# # from flask import Flask, jsonify

# # app = Flask(__name__)

# # @app.route('/hello', methods=['GET'])
# # def hello():
# #     return jsonify(message="Hello, API!")



# import subprocess
# import servicemanager
# import socket
# import sys
# import win32event
# import win32service
# import win32serviceutil

# # from app import app

# service_name = 'APIService'  # Replace with the actual service name
# try:
#     result = subprocess.run(['sc', 'query', service_name], capture_output=True, text=True, check=True)
#     print("Service is already installed.")
# except subprocess.CalledProcessError:
#     # The service doesn't exist, so install it
#     install_command = ['python', 'main.py', 'install']
#     try:
#         install_result = subprocess.run(install_command, capture_output=True, text=True, check=True)
#         print("Service installed successfully.")
#     except subprocess.CalledProcessError as e:
#         print("Error installing the service:", e.stderr)

# class APIService(win32serviceutil.ServiceFramework):
#     _svc_name_ = 'APIService'
#     _svc_display_name_ = 'API Service'

#     def __init__(self, args):
#         win32serviceutil.ServiceFramework.__init__(self, args)
#         self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
#         socket.setdefaulttimeout(60)
#         self.is_alive = True

#     def SvcStop(self):
#         self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
#         win32event.SetEvent(self.hWaitStop)
#         self.is_alive = False

#     def SvcDoRun(self):
#         servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
#                               servicemanager.PYS_SERVICE_STARTED,
#                               (self._svc_name_, ''))
#         self.main()

#     def main(self):
#         app.run(host='0.0.0.0', port=5000)

# if __name__ == '__main__':
#     if len(sys.argv) == 1:
#         servicemanager.Initialize()
#         servicemanager.PrepareToHostSingle(APIService)
#         servicemanager.StartServiceCtrlDispatcher()
#     else:
#         win32serviceutil.HandleCommandLine(APIService)

# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return "Welcome to the homepage!"

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
