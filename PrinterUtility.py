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
import requests

app = Flask(__name__)
CORS(app, origins='*')


@app.route('/')
def home():
    return 'Welcome to the Home Page!'


@app.route('/process_form', methods=['POST'])
def process_form():

    pdf_file = request.files["file"]
    default_printer_name = request.form.get('printer_name')

    printer_list = []
    printers = win32print.EnumPrinters(2)
    for printer in printers:
        printer_name = printer[2]
        printer_list.append(printer_name)

    if default_printer_name in printer_list:
        print(f"{default_printer_name} is in the list.")
    else:
        return jsonify({'message': 'An error occurred:', 'response': 'The selected printer does not exist on the device'}), 400

    destination_folder = "upload/"
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    unique_identifier = str(uuid.uuid4().hex)
    file_extension = ".pdf"
    new_file_name = f"{destination_folder}/new_file_{unique_identifier}{file_extension}"
    pdf_file.save(new_file_name)

    try:
        abs_file_path = os.path.abspath(f"{new_file_name}")
        print_result = print_list_names(abs_file_path, default_printer_name)

        response = {'message': 'File printed', 'response': print_result}

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
    # 2 means enumerate locally installed printers
    printers = win32print.EnumPrinters(2)
    print(printers)
    for printer in printers:
        printer_name = printer[2]
        printer_handle = win32print.OpenPrinter(printer_name)

        print(win32print.GetPrinter(printer_handle, 2))
        print(win32print.PRINTER_ATTRIBUTE_WORK_OFFLINE, "sss")
        print()

        printer_info = win32print.GetPrinter(printer_handle, 2)
        if printer_info['Attributes'] & win32print.PRINTER_ATTRIBUTE_WORK_OFFLINE:
            d = 'OFFLINE'
        else:
            d = 'ONLINE'
        printer_status = printer_info['Status']

        # win32print.PRINTER_STATUS_IO_ACTIVE
        # printer_status_str = status_strings.get(printer_status, "Unknown")
        printer_dict = {
            'name': printer_name,
            'status': printer_status,
            'handle': d
        }
        printer_list.append(printer_dict)
    print(printer_list)
    return printer_list


def print_list_names(file_path, print_name):
    # print_name = win32print.GetDefaultPrinter()

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
