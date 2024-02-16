# import win32serviceutil
# import win32service
# import win32event
# import servicemanager
# import socket
# import sys
# from flask import Flask

# app = Flask(__name__)


# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

# # Define more endpoints as needed


# class MyService(win32serviceutil.ServiceFramework):
#     _svc_name_ = 'MyService'  # The name of your service
#     _svc_display_name_ = 'My Service'  # The display name of your service

#     def __init__(self, args):
#         win32serviceutil.ServiceFramework.__init__(self, args)
#         self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
#         self.is_running = True

#     def SvcStop(self):
#         self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
#         win32event.SetEvent(self.hWaitStop)
#         self.is_running = False

#     def SvcDoRun(self):
#         servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
#                               servicemanager.PYS_SERVICE_STARTED,
#                               (self._svc_name_, ''))
#         self.main()

#     def main(self):
#         # Start your Flask API here
#         app.run()


# if __name__ == '__main__':
#     if len(sys.argv) == 1:
#         servicemanager.Initialize()
#         servicemanager.PrepareToHostSingle(MyService)
#         servicemanager.StartServiceCtrlDispatcher()
#     else:
#         win32serviceutil.HandleCommandLine(MyService)
