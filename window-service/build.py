from PyInstaller import __main__


def build_service():
    try:
        __main__.run(['service.py',
                      '--windowed',
                      '--hidden-import=win32timezone',
                      '--add-data=windows.py;.',

                      '--add-data=venv;.'])
        pass
    except Exception as build_error:
        print(build_error)


if __name__ == "__main__":
    build_service()
    pass
