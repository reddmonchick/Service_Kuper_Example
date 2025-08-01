import requests
import pytest


def test_excel_api():
    url = "http://localhost:8000/api/v1/parser/process-excel/"
    file_path = 'example.xlsx'


    files = {
    'file': (file_path, open(file_path, 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    }
    data = {
        'command': 'process_excel',
        'shop': 'Kuper' 
    }

    response = requests.post(url, files=files, data=data)
    assert response.status_code == 200

def test_excel_file():
    url = "http://localhost:8000/api/v1/parser/process-excel/"
    file_path = 'example.xlsx'


    files = {
    'file': (file_path, open(file_path, 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    }
    data = {
        'command': 'process_excel',
        'shop': 'Kuper' 
    }

    response = requests.post(url, files=files, data=data)
    with open('output23.xlsx', 'wb') as file:
        file.write(response.content)
    assert response.status_code == 200