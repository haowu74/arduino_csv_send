from asyncio.windows_events import NULL
import csv
from operator import delitem
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
import serial
import time

root = tk.Tk()
root.title('CSV for Arduino')
root.resizable(False, False)
root.geometry('300x150')

filename = ""

def open_csv():
    global filename
    filetypes = (
        ('csv files', '*.csv'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    
def send_csv():
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            print(','.join(row))

    

open_button = ttk.Button(
    root,
    text = "Open",
    command=open_csv
)

send_button = ttk.Button(
    root,
    text = "Send",
    command=send_csv
)

open_button.grid(column=0, row=1, sticky='w', padx=10, pady=10)
send_button.grid(column=1, row=1, sticky='w', padx=10, pady=10)

root.mainloop()


