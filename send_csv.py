from asyncio.windows_events import NULL
import csv
from faulthandler import disable
from operator import delitem
from re import S
from threading import Thread, Event
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
import serial
import time
from serial.threaded import ReaderThread, LineReader
import sys
import traceback
import serial.tools.list_ports
import os

ports = list(map(lambda x : x.name, list(serial.tools.list_ports.comports())))
files = [csv for csv in os.listdir(".") if csv.endswith(".csv")]
root = tk.Tk()
root.title('CSV for Arduino')
root.resizable(False, False)
root.geometry('600x300')

filename = ""
stop_event = Event()
port=ports[0]
filename = files[0]
end=False

class PrintLines(LineReader):
    def connection_made(self, transport):
        super(PrintLines, self).connection_made(transport)
        sys.stdout.write('port opened\n')
        self.write_line('hello world')

    def handle_line(self, data):
        sys.stdout.write('line received: {}\n'.format(repr(data)))

    def connection_lost(self, exc):
        if exc:
            traceback.print_exc(exc)
        sys.stdout.write('port closed\n')

def open_csv():
    global filename, end
    filetypes = (
        ('csv files', '*.csv'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='.',
        filetypes=filetypes)
    
    filename_label.configure(text=filename.split('/')[-1])
    end = True
    
def send_csv():
    t = Thread(target=send_to_arduino)
    t.start()
    

def send_to_arduino():
    global port
    global end
    send_button.state(["disabled"])
    s = serial.serial_for_url(port)
    s.baudrate = 115200
    # print("Start sending CSV...")
    end = False
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        while True:
            for row in reader:
                x = str.encode(",".join(row).replace('\n', ''))
                #print(x)
                s.write(x)
                time.sleep(0.001)

                if stop_event.is_set():
                    end = True
                    break
                if end:
                    break
            if end:
                break
            csvfile.seek(0)
    s.close()
    print("Complete sending CSV!")
    send_button.state(["!disabled"])

    

def com_port_selected(v):
    global port
    port = v

def file_selected(v):
    global filename, end
    filename = v
    end=True

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

filename_label = ttk.Label(
    root,
    text = "File Name"
)

ports_variable = tk.StringVar()

files_variable = tk.StringVar()

com_port_selection = ttk.OptionMenu(
    root,
    ports_variable,
    ports[0],
    *ports,
    command=com_port_selected
)

file_selection = ttk.OptionMenu(
    root,
    files_variable,
    files[0],
    *files,
    command=file_selected
)

open_button.grid(column=0, row=1, sticky='w', padx=10, pady=10)
send_button.grid(column=1, row=1, sticky='w', padx=10, pady=10)
# filename_label.grid(column=0, columnspan=2, row=2, sticky='w', padx=10, pady=10)
file_selection.grid(column=0, row=3, sticky='w', padx=10, pady=10)
com_port_selection.grid(column=0, row=4, sticky='w', padx=10, pady=10)

root.iconbitmap("ignition.ico")
root.mainloop()
stop_event.set()

