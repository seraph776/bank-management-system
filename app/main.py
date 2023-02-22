"""
created: 2023/02/22 13:24:46 
@author: seraph★vega
contact: admin@pythonspecialops.com
project: Bank Management System (BMS)
metadoc: BMS that connects to a sqlite3 database
license: MIT
"""

from bms_connection import BMSConnection
from bms_application import BMSApplication


def main():
    conn = BMSConnection()
    app = BMSApplication(conn)
    while True:
        app.display_menu()


if __name__ == '__main__':
    main()
