from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
# import find
import urllib.parse
import sys
import os
import win32print
import win32api
from urllib.parse import quote
import tempfile
import shutil
import uuid
import time

app = Flask(__name__)
CORS(app, origins='*') 

@app.route('/')
def home():
    return 'Welcome to the Home Page!'


@app.route('/process_form', methods=['POST'])
def process_form():
    file = request.form.get('file')
    print(request.files["file"])
    pdf_file = request.files["file"]
    destination_folder = "upload/"
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    unique_identifier = str(uuid.uuid4().hex)
    file_extension = ".pdf"
    new_file_name = f"{destination_folder}/new_file_{unique_identifier}{file_extension}"
    pdf_file.save(new_file_name)
  
    # url = file
    # url_encoded = quote(url)
    # headers = {
    #     "Accept": "*/*",
    #     "Accept-Encoding": "gzip, deflate, br",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    # }
    # response1 = requests.get(url, headers=headers)

    # if (response1.status_code == 200):
        # with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        #     temp_file.write(response1.content)
        #     temp_file_path = temp_file.name  # Replace with the actual temporary file path
       
        # file_extension = ".pdf"
        # unique_identifier = str(uuid.uuid4().hex)
        # 
        # try:
        #     destination_path = os.path.join(destination_folder, new_file_name)
        #     shutil.move(temp_file_path, destination_path)
        #     # Replace with the actual destination folder path
        #     response = {'message': 'File printing successful',
        #                 'response': temp_file_path}
        # except Exception as e:
        #     response = {'message': 'An error occurred:', 'response': str(e)}

    try:
            abs_file_path = os.path.abspath(f"{new_file_name}")           
            print_result = print_list_names(abs_file_path)

            response = {'message': 'File printed', 'response': print_result }

            time.sleep(20)           
            if os.path.exists(new_file_name):
                os.remove(new_file_name)
            return jsonify(response), 200
    except Exception as e:
            # print("An error occurred:", )
            response = {'message': 'An error occurred:', 'response': str(e)}
            return jsonify(response), 400

    # else:
    #     response = {'message': 'Some thing went wrong',
    #                 'response': response1.status_code}


@app.route('/printer_list', methods=['GET'])
def printers_list():
    
    printer_list = []
    printers = win32print.EnumPrinters(2)  # 2 means enumerate locally installed printers
    print(printers)
    for printer in printers:
        printer_name = printer[2]        
        printer_handle=win32print.OpenPrinter(printer_name)      
        
        print(win32print.GetPrinter(printer_handle,2)) 
        print(win32print.PRINTER_ATTRIBUTE_WORK_OFFLINE,"sss")
        print()
        
        printer_info = win32print.GetPrinter(printer_handle,2)
        if printer_info['Attributes'] & win32print.PRINTER_ATTRIBUTE_WORK_OFFLINE:
            d='OFFLINE'
        else:
            d='ONLINE'
        printer_status=printer_info['Status']
        # win32print.PRINTER_STATUS_IO_ACTIVE
        print(printer_status)               
        # printer_status_str = status_strings.get(printer_status, "Unknown")
        printer_dict = {
            'name': printer_name,
            'status': printer_status,   
            'handle':d         
        }
        printer_list.append(printer_dict)
    print(printer_list)    
    return printer_list
    


def print_list_names(file_path):
    print_name = win32print.GetDefaultPrinter()
    printer_handle = win32print.OpenPrinter(print_name)

    command = f'PDFtoPrinter "{file_path}" "{print_name}"'
    result = win32api.ShellExecute(
        0, "open", "cmd.exe", f"/c {command}", None, 0)

    # result=win32api.ShellExecute(
    #     0,
    #     "print",
    #      file_path,
    #     f'"{print_name}"',
    #     ".",
    #     0
    # )
    return result


if __name__ == '__main__':
    app.run(host='127.1.0.1', port=32568, debug=True)
