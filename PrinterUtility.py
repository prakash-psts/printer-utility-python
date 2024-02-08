from flask import Flask, render_template, request, jsonify
from fastapi import FastAPI,APIRouter,UploadFile,Form,Request,Response
from fastapi.middleware.cors import CORSMiddleware
from flask_cors import CORS
import os
import win32print
import win32api
from urllib.parse import quote
import uuid
import time
import asyncio
import uvicorn
from typing import List
import subprocess

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# CORS(app, origins='*')




@app.get("/")
def index():
    return "Welcome to the Printer Utility"


@app.post('/process_form')
async def process_form(file: UploadFile, printer_name: str = Form(...) ):   

    default_printer_name = printer_name

    user_home = os.path.expanduser("~")  
    documents_folder = os.path.join(user_home, "Documents")
    destination_folder = f'{documents_folder}//printedFiles/'

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    printer_list = []
    printers = win32print.EnumPrinters(2)
    for printer in printers:
        printer_name = printer[2]
        printer_list.append(printer_name)

    if default_printer_name in printer_list:
        print(f"{default_printer_name} is in the list.")
    else:
        return {'message': 'An error occurred:', 'response': 'The selected printer does not exist on the device', 'status_code': 400  }


    unique_identifier = str(uuid.uuid4().hex)
    file_extension = ".pdf"
    new_file_name = f"{destination_folder}/new_file_{unique_identifier}{file_extension}"

    with open(new_file_name, "wb") as f:             
            f.write(file.file.read())

    try:
        abs_file_path = os.path.abspath(f"{new_file_name}")
        print_result = await print_files(abs_file_path, default_printer_name)


        # time.sleep(12)
        if os.path.exists(new_file_name):
            os.remove(new_file_name)

        response = {'message': 'File printed', 'response': print_result, 'status_code': 200 }
        return response
    
    except Exception as e:
        if os.path.exists(new_file_name):
            os.remove(new_file_name)
        response = {'message': 'An error occurred:', 'response': 'Something went wrong!', 'status_code': 400 }
        return response
    



@app.post('/print_multifile')
async def printFile(files: List[UploadFile], printer_names: List[str]=Form(...)):  
    
    try:
        user_home = os.path.expanduser("~")
        documents_folder = os.path.join(user_home, "Documents")
        destination_folder = os.path.join(documents_folder, "printedFiles")

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        for file in files:
            for printer_name in printer_names:
                printer_list = [printer[2] for printer in win32print.EnumPrinters(2)]

                if printer_name not in printer_list:
                    return {'message': 'An error occurred', 'response': f'The selected printer "{printer_name}" does not exist on the device', 'status_code': 400 }
                
                unique_identifier = str(uuid.uuid4().hex)         
                file_path = f"{destination_folder}\\new_file_{unique_identifier}.pdf"
                with open(file_path, "wb") as f:             
                    f.write(file.file.read())

                abs_file_path = os.path.abspath(file_path)

                print_result = await print_files(abs_file_path, printer_name)
                if os.path.exists(file_path):
                    os.remove(file_path)    

        response = {'message': 'File printed', 'response': print_result,'status_code':200 }
        return response
    
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        response = {'message': 'An error occurred:','response': 'Something went wrong!','status_code':400}
        return response


@app.get('/printer_list')
def printers_list():

    printer_list = []
    printers = win32print.EnumPrinters(2)


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


async def print_files(file_path, print_name):
    try:      

        # print_name = win32print.GetDefaultPrinter()
        # printer_handle = win32print.OpenPrinter(print_name)
        command = f'PDFtoPrinter "{file_path}" "{print_name}"'      
        
        result = subprocess.run(command, shell=True, check=True)       

            
        return result
    except Exception as e:
        print(e)

if __name__ == '__main__':
    uvicorn.run(app, port=32568, host='127.1.0.1')
