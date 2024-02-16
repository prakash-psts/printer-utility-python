import os


class windowsSystem():
    def __init__(self):
        super().__init__()
        pass

    def startProcess(self, path, host):
        os.chdir(path)
        response = os.popen(f'call main.exe {host}')
        return response

    def killProcess(self):
        response = -1
        processId = -1
        process = os.popen(
            "netstat -ano | findstr :32568 | findstr LISTENING").read()
        if len(process.split("\n")) > 1:
            arr = process.split("\n")
            for str in arr:
                subArr = str.split(" ")
                processId = subArr[len(subArr)-1]
                response = os.system("taskkill /F /PID "+processId)
            pass
        else:
            arr = process.split(" ")
            processId = arr[len(arr)-1]
            response = os.system("taskkill /F /PID "+processId)
            pass
        res = os.popen("tasklist | findstr main.exe").read()
        resArr = res.split("\n")
        # In case if any rogue exe is still running in the back ground
        if len(resArr) > 1:
            for data in resArr:
                individualArr = data.split("main.exe")
                if len(individualArr) > 1:
                    task_pid = data.split("main.exe")[1].split(
                        "Services")[0].strip()
                    os.popen(f"taskkill /f /PID {task_pid}")
        return response
