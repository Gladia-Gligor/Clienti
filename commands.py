import sqlite3
import qrcode
import sys
import uuid

from tkinter import *

from datetime import datetime
from typing import Dict, Union
from xmlrpc.client import DateTime

#import ezgmail
import openpyxl
import requests

from database import DatabaseManager


db = DatabaseManager("clients.db")


class Command:
    def execute(self): pass


class CreateClientsTableCommand(Command):
    def execute(self):
        db.create_table(
            table_name="clients",
            columns={
                "id": "integer primary key autoincrement",
                "client_name": "text not null",
                "proiect": "text not null",
                "informatii": "text",
                "url": "text not null",
                "date_added": "text not null",
            }
        )


class AddClientCommand(Command):
    def execute(self, data: Dict[str, str], timestamp: Union[str, None] = None) -> str:
        data["date_added"] = timestamp or datetime.utcnow().isoformat()
        db.add(
            table_name="clients", 
            data=data
        )
        return "Fisa client creata!"


class ListClientsCommand(Command):
    def __init__(self, order_by: str = "id") -> None:
        self.order_by = order_by

    def execute(self):
        cursor = db.select("clients", order_by=self.order_by)
        results = cursor.fetchall()
        return results


class CreateQRCommand(Command):
    def execute(self, data:int):
      
       input_URL = db.select_url_by_id(data)
       #input_name = db.select_name_by_id(data)
       #print(input_name)
       
       def get_cursor():
            connection = sqlite3.connect("clients.db")
            return connection.cursor

       def select_name_by_id(cursor:sqlite3.Cursor, id:int):
            sql_query = "SELECT 'client_name' FROM 'clients' WHERE 'id' =?"
            print(sql_query)
            return sql_query

       cursor = get_cursor()
       input_name = select_name_by_id(cursor,data)

       qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=15,
            border=4,
        )

       qr.add_data(input_URL)
       qr.make(fit=True)

       img = qr.make_image(fill_color="red", back_color="white")
       img.save(f"./exports/{input_name}.png")

       #print(qr.data_list)  

class GetClientCommand(Command):
    def execute(self, data: int):
        return db.select(
            "clients",
            {
                "id": data
            }
        ).fetchone()


class EditClientCommand(Command):
    def execute(self, data: Dict[str, str]):
        db.update(
            "clients",
            {
                "id": data["id"]
            },
            data["update"]
        )
        return "Fisa client modificata!"



class DeleteClientCommand(Command):
    def execute(self, data: str) -> str:
        db.delete("clients", {"id": data})
        return "Fisa client stearsa!"


class ExportToExcelCommand(Command):
    def execute(self, data: str) -> str:
        records = ListClientsCommand().execute()
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        for row_index, row in enumerate(records):
            sheet.insert_rows(idx=row_index + 1)
            for column_index, cell_value in enumerate(row):
                sheet.cell(row=row_index + 1, column=column_index + 1, value=cell_value)

        workbook.save(f"./exports/{data}")
        return f"Exported to file {data}"


# class EmailCommand(Command):
#     def execute(self, data: Dict[str, str]) -> str:
#         recipient = data["recipient"]
#         subject = "Your bookmarks from Bark!"
#         body = "Attached to this email you will find your Bark bookmarks."
#         unique_name = str(uuid.uuid1())
#         file_name = f"{unique_name}.xlsx"
#         ExportToExcelCommand().execute(file_name)

#         file_path = f"./exports/{file_name}"

#         ezgmail.send(
#             recipient=recipient,
#             subject=subject,
#             body=body,
#             attachments=[file_path]
#         )

#         return f"Email sent to {recipient}!"

class QuitCommand(Command):
    def execute(self):
        sys.exit()