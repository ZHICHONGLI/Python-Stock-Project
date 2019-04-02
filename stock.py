from tkinter import *
from tkinter import filedialog
import csv
import numpy as np
# import matplotlib.pyplot as plt

root = Tk()


def load():
    dir = filedialog.askopenfilename(initialdir="/",
                                     filetypes=(("CSV File", "*.csv"),
                                                ("All Files", "*.*")),
                                     title="Choose a file."
                                     )
    print(dir)
    global stockData, dateRangeData
    with open(dir) as f:
        stockData = [{k: v for k, v in row.items()}
                     for row in csv.DictReader(f, skipinitialspace=True)]
    print(stockData)

    dateRangeData["startDate"] = stockData[0]["Date"]
    dateRangeData["endDate"] = stockData[-1]["Date"]
    dateRangeData["high"] = float(stockData[0]["Close"])
    dateRangeData["low"] = float(stockData[0]["Close"])
    total = 0
    for i in stockData:
        if float(i["Close"]) > dateRangeData["high"]:
            dateRangeData["high"] = float(i["Close"])
        if float(i["Close"]) < dateRangeData["low"]:
            dateRangeData["low"] = float(i["Close"])
        total += float(i["Close"])

    dateRangeData["avg"] = total/len(stockData)
    print(dateRangeData)
    date_label_content.config(text='{}   to  {} / {} days'.format(
        dateRangeData["startDate"], dateRangeData["endDate"], len(stockData)))
    high_label_content.config(text=dateRangeData["high"])
    low_label_content.config(text=dateRangeData["low"])
    avg_label_content.config(text=dateRangeData["avg"])
    console_label_body.config(text='load from:' + dir)


def clear():
    global stockData
    stockData = []
    date_label_content.config(text='')
    high_label_content.config(text='')
    low_label_content.config(text='')
    avg_label_content.config(text='')
    console_label_body.config(text='data cleard')


def switchFrame(frame):
    review_label.config(text=frame)


def log_motion_event(event):
    global log_drag, x1, x2, y1, y2, mouse_x, mouse_y
    x = event.x
    y = event.y
    if not log_drag:
        mouse_x = x
        mouse_y = y
        log_drag = True
        return
    x1 += (x-mouse_x)
    x2 += (x-mouse_x)
    y1 += (y-mouse_y)
    y2 += (y-mouse_y)
    console_canvas.coords(rect, x1, y1, x2, y2)
    mouse_x = x
    mouse_y = y


def log_release_event(event):
    global log_drag
    log_drag = False


root.title('Stock Py')
# root.geometry('800x500')

bar_frame = Frame(root)
review_frame = Frame(root)
result_frame = Frame(root)
console_frame = Frame(root)

# bar panel
load_btn = Button(bar_frame, text='Load File (.csv)',
                  height=3, width=45, command=load)
load_btn.grid(row=0, column=0)

clear_btn = Button(bar_frame, text='Clear', height=3, width=45, command=clear)
clear_btn.grid(row=0, column=1)

review_btn = Button(bar_frame, text='Review Data', height=3,
                    width=45, command=lambda: switchFrame('Review'))
review_btn.grid(row=1, column=0)

result_btn = Button(bar_frame, text='Analyze Result', height=3,
                    width=45, command=lambda: switchFrame('Result'))
result_btn.grid(row=1, column=1)

# review panel
figure_frame = Frame(review_frame)
figure_frame.grid(row=1, column=0, sticky='NW')
label_1w = Label(figure_frame, text='1W', bg='gray65', width='14')
label_1w.grid(row=0, column=1)
label_1m = Label(figure_frame, text='1 Month', bg='gray70', width='14')
label_1m.grid(row=0, column=2)
label_1y = Label(figure_frame, text='1 Year', bg='gray75', width='14')
label_1y.grid(row=0, column=3)
label_3y = Label(figure_frame, text='3 Years', bg='gray80', width='14')
label_3y.grid(row=0, column=4)
label_5y = Label(figure_frame, text='5 Years', bg='gray85', width='14')
label_5y.grid(row=0, column=5)
maxy_label = Label(figure_frame, text='Max', bg='gray90', width='14')
maxy_label.grid(row=0, column=6)
# canvas_label = Label(figure_frame, height=10, bg='white')
# canvas_label.grid(row=1, column=0)

grid_frame = Frame(review_frame)
grid_frame.grid(row=3, column=0, sticky='NW')
date_label = Label(grid_frame, text='Date Range: ', width='20')
date_label_content = Label(grid_frame, width='50')
date_label.grid(row=0, column=0)
date_label_content.grid(row=0, column=1)
high_label = Label(grid_frame, text='High: ', width='20')
high_label_content = Label(grid_frame, width='20')
high_label.grid(row=1, column=0)
high_label_content.grid(row=1, column=1)
low_label = Label(grid_frame, text='Low: ', width='20')
low_label.grid(row=2, column=0)
low_label_content = Label(grid_frame, width='20')
low_label_content.grid(row=2, column=1)
avg_label = Label(grid_frame, text='Avg: ', width='20')
avg_label.grid(row=3, column=0)
avg_label_content = Label(grid_frame, width='20')
avg_label_content.grid(row=3, column=1)

console_label_header = Label(console_frame, height=1,
                             text='Logs: ', width=90, bg='gray95')
console_label_header.grid(row=0, column=0, sticky='NW')
console_label_body = Label(console_frame, height=1,
                           width=90, bg='gray95')
console_label_body.grid(row=1, column=0, sticky='NW')


console_canvas = Canvas(review_frame, width=810,
                        height=300)  # , highlightthickness=0
console_canvas.bind('<B1-Motion>', log_motion_event)
console_canvas.bind('<ButtonRelease-1>', log_release_event)
console_canvas.focus_set()
console_canvas.grid(row=2, column=0)
mouse_x = 0
mouse_y = 0
log_drag = False

x1 = y1 = 10
y2 = 15
x2 = 400
rect = console_canvas.create_rectangle(x1, y1, x2, y2, fill='gray95')


review_label = Label(bar_frame, height=3, width=90,
                     text='Review', bg='old lace')
review_label.grid(row=2, column=0, columnspan='40')
bar_frame.grid(row=0, column=0)
review_frame.grid(row=1)
# result_frame.grid(row=1, column=0)
console_frame.grid(row=2, column=0, sticky='NW')


# initialize stock data
stockData = []
dateRangeData = {"startDate": "", "endDate": "",
                 "high": "", "low": "", "avg": ""}


mainloop()
