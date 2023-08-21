import threading
import pystray
from PIL import Image
import tkinter as tk
import requests
from io import BytesIO
import os

# import find
from flask import Flask,render_template, request,jsonify
import urllib.parse 
import sys
import win32print
import win32api
import requests
from urllib.parse import quote
import tempfile
import shutil
import uuid
import time

app = Flask(__name__)

@app.route('/')
def hello():
    return "Welcome!"

@app.route('/process_form', methods=['POST'])
def process_form():
    print(request,'red')
    username = request.form.get('username')
    email = request.form.get('email')
    file =request.form.get('file')
    print(file,'file')
    url = file
    url_encoded = quote(url)
    headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br", 
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"  
    }
    response1 = requests.get(url,headers=headers)
    UPLOAD_FOLDER = "upload/" 
    if(response1.status_code==200):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(response1.content)
            temp_file_path = temp_file.name # Replace with the actual temporary file path
        destination_folder = "upload/" 
        file_extension = ".pdf"
        unique_identifier = str(uuid.uuid4().hex)
        new_file_name = f"new_file_{unique_identifier}{file_extension}"
        try:
          destination_path = os.path.join(destination_folder, new_file_name)
          shutil.move(temp_file_path, destination_path) 
          response = {'message': 'File printing successful', 'response': temp_file_path}# Replace with the actual destination folder path
        except Exception as e:
          response = {'message': 'An error occurred:', 'response': str(e)}
        
        try:
            abs_file_path = os.path.abspath(f"upload/{new_file_name}")            
            print_result = print_list_names(abs_file_path)   
            response = {'message': 'File printing', 'response': print_result}
            time.sleep(6)
            os.remove(destination_path)
        except Exception as e:
                # print("An error occurred:", )
            response = {'message': 'An error occurred:', 'response': str(e)}
            # print_result = print_list_names("file:///C:/Users/91638/Downloads/dummy.pdf")

    else:
        response = {'message': 'Some thing went wrong', 'response': response1.status_code}
    
    return jsonify(response), response1.status_code

def print_list_names(file_path):     
    print_name=win32print.GetDefaultPrinter() 
    printer_handle=win32print.OpenPrinter(print_name)
    
    result = win32api.ShellExecute(
        0,
        "print",
         file_path,
        f'"{print_name}"',
        ".",
        0
    )
    
    return result


def run_server():
    app.run(host="127.1.0.1",port=32568,debug=True)

def on_exit(icon, item):
    app.do_teardown_appcontext()  # Close Flask gracefully
    icon.stop()
    # server_thread.join()

if __name__ == '__main__':
    # server_thread = threading.Thread(target=run_server)
    # server_thread.start()
    run_server()
    icon_url = "https://www.smartb.demopsts.com/static/media/Logo.1199d99c952e78c8d43db47af2d9ace1.svg" 
    
    
    def get_icon():
        # response = requests.get(icon_url)
        # icon_image = Image.open(BytesIO(response.content))
        # return icon_image
        #  icon_path = "D:/PrinterApplication/b_smart.png"  # Replace with the actual path to your image
         icon_path = os.path.abspath(f"b_smart.png")
         icon_image = Image.open(icon_path)
         return icon_image

    menu = (
        pystray.MenuItem("Stop Server", on_exit),
    )

    icon = pystray.Icon("Bsmart", get_icon(), "Bsmart", menu)
    icon.run()
