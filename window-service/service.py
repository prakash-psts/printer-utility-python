from pathlib import Path
import random
import time
import socket

import win32serviceutil

import servicemanager
import win32event
import win32service
import os
import sys
import traceback


from windows import *
from common import *


class SMWinservice(win32serviceutil.ServiceFramework):
    """Base class to create winservice in Python"""

    _svc_name_ = "00007"
    _svc_display_name_ = "00007"
    _svc_description_ = "Python Service Description"

    @classmethod
    def parse_command_line(cls):
        """
        ClassMethod to parse the command line
        """
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        """
        Constructor of the winservice
        """
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        """
        Called when the service is asked to stop
        """
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.stop()
        self.main()
        win32event.SetEvent(self.hWaitStop)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        """
        Called when the service is asked to start
        """
        self.start()
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, ""),
        )
        self.main()
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def start(self):
        """
        Override to add logic before the start
        eg. running condition
        """

        pass

    def stop(self):
        """
        Override to add logic before the stop
        eg. invalidating running condition
        """

        pass

    def main(self):
        """
        Main class to be ovverridden to add logic
        """

        pass


class PythonCornerExample(SMWinservice):
    _svc_name_ = "0999____"
    _svc_display_name_ = "0999____"
    _svc_description_ = "0999____That's a great winservice! :)"

    def start(self):
        self.processes = []
        self.serverPID = 0
        self.osObj = windowsSystem()
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        self.host = {
            "host": IPAddr,
            "changed": 0
        }
        self.isrunning = True
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        self.dirArr = self.BASE_DIR.split("\\")

        self.dirArr.append("main")

        self.concat = "\\"
        self.server_dir = self.concat.join(self.dirArr)
        self.commonFunc = commons()
        self.commonFunc.log("IP ADDRESS: "+self.host["host"]+"")

    def stop(self):

        self.isrunning = False

    def main(self):
        i = 0

        if self.isrunning:
            self.startUvicornServer()
            self.ipAddressListener()

        else:
            self.stopUvicornServer()
            self.ipaddresslistening = False

        pass

    def startUvicornServer(self):

        try:
            self.commonFunc.log("STARTING SERVER")
            self.commonFunc.log(self.server_dir)
            host = self.host["host"]
            self.commonFunc.log(
                "IP ADDRESS FROM MAIN FUNCTION  : "+self.host["host"]+"")
            self.commonFunc.log("IP ADDRESS ")
            self.commonFunc.log(f'call {self.server_dir} {host}')
            self.ipaddresslistening = True
            serverStarted = self.osObj.startProcess(
                self.server_dir, self.host["host"])
            self.commonFunc.log("SERVER STARTED")
            self.commonFunc.log(str(serverStarted))
        except Exception as e:
            self.commonFunc.log(str(e))
            pass
        pass

    def stopUvicornServer(self):

        try:
            serverStopped = self.osObj.killProcess()
            self.commonFunc.log(str(serverStopped))
        except Exception as e:
            self.commonFunc.log(str(e))
            traceback.print_exc()
            traceback.print_exception()
            pass

        pass

    def ipAddressListener(self):
        while self.ipaddresslistening:
            time.sleep(7)
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)
            if IPAddr != self.host["host"]:
                self.commonFunc.log("IP ADDRESS CHANGED")
                self.host["host"] = IPAddr
                self.ipaddresslistening = False
                self.stopUvicornServer()
                self.startUvicornServer()


if __name__ == '__main__':

    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(PythonCornerExample)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(PythonCornerExample)
