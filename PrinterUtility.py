from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import win32print
import win32api
from urllib.parse import quote
import uuid
import time
import subprocess

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

    # Get the user's home directory
    user_home = os.path.expanduser("~")

    # Construct the path to the "Documents" folder
    documents_folder = os.path.join(user_home, "Documents")
    destination_folder = f'{documents_folder}//printedFiles/'

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    unique_identifier = str(uuid.uuid4().hex)
    file_extension = ".pdf"
    new_file_name = f"{
        destination_folder}/new_file_{unique_identifier}{file_extension}"

    pdf_file.save(new_file_name)

    try:
        abs_file_path = os.path.abspath(f"{new_file_name}")
        print_result = print_files(abs_file_path, default_printer_name)

        response = {'message': 'File printed', 'response': print_result}

        # time.sleep(12)
        if os.path.exists(new_file_name):
            os.remove(new_file_name)

        return jsonify(response), 200

    except Exception as e:
        if os.path.exists(new_file_name):
            os.remove(new_file_name)
        response = {'message': 'An error occurred:',
                    'response': 'Something went wrong!'}
        print(e, 'ee')
        return jsonify(response), 400


@app.route('/print_multifile', methods=['POST'])
def printFile():

    pdf_file = request.files.getlist("files")
    default_printer_name = request.form.getlist('printer_names')

    try:
        user_home = os.path.expanduser("~")
        documents_folder = os.path.join(user_home, "Documents")
        destination_folder = os.path.join(documents_folder, "printedFiles")

        print_response = []

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        for file in pdf_file:
            for printer_name in default_printer_name:
                printer_list = [printer[2]
                                for printer in win32print.EnumPrinters(2)]

                if printer_name not in printer_list:
                    return jsonify({'message': 'An error occurred', 'response': f'The selected printer "{printer_name}" does not exist on the device', 'status_code': 400}), 400

                unique_identifier = str(uuid.uuid4().hex)
                file_path = f"{destination_folder}\\new_file_{
                    unique_identifier}.pdf"
                with open(file_path, "wb") as f:
                    f.write(file.file.read())

                abs_file_path = os.path.abspath(file_path)

                print_result = print_files(abs_file_path, printer_name)
                print_response.append(print_result)

                if os.path.exists(file_path):
                    os.remove(file_path)

        response = {'message': 'File printed',
                    'response': print_response, 'status_code': 200}
        return jsonify(response), 200

    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        response = {'message': 'An error occurred:',
                    'response': 'Something went wrong!', 'status_code': 400}
        print(e, "ee")
        return jsonify(response), 400


@app.route('/printer_list', methods=['GET'])
def printers_list():

    printer_list = []
    # 2 means enumerate locally installed printers
    printers = win32print.EnumPrinters(2)
    # print(printers)

    for printer in printers:
        printer_name = printer[2]
        printer_handle = win32print.OpenPrinter(printer_name)

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
    return printer_list


def print_files(file_path, print_name):

    # printer_handle = win32print.OpenPrinter(print_name)
    # command = f'PDFtoPrinter "{file_path}" "{print_name}"'
    # result = subprocess.run(command, shell=True, check=True)

    # result = win32api.ShellExecute(
    #     0, "open", "cmd.exe", f"/c {command}", None, 0)

    # result=win32api.ShellExecute(
    #     0,
    #     "print",
    #      file_path,
    #     f'"{print_name}"',
    #     ".",
    #     0
    # )

    try:
        result = subprocess.run(
            ['PDFtoPrinter', file_path, print_name], capture_output=True, text=True)
        if result.returncode == 0:
            return {'status': 'success', 'message': 'File printed successfully'}
        else:
            return {'status': 'error', 'message': result.stderr}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


if __name__ == '__main__':
    app.run(host='127.1.0.1', port=32568, debug=True)
