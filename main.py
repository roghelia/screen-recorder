import tkinter as tk
from tkinter.ttk import *

import tkinter.filedialog as fd
from tkinter.messagebox import showinfo, showerror

import pyautogui # provide clean gui
import subprocess


def start_recording():
    start_stop_btn.config(text='Stop')
    hint_lbl.config(text='Press Stop to Stop Recording', foreground='#d32f2f')
    #remove the function access, before you enter the initials.

    root.iconify()
    record_screen()


def record_screen():
    out_file = file_entry.get()
    dimensions = res_x.get() + "x" + res_y.get()

    off_x = offset_x.get()
    off_y = offset_y.get()
    fps = fps_spin.get()

    global rec_proc

    try:
        rec_proc = subprocess.Popen(["ffmpeg", "-f", "gdigrab", "-framerate", fps, "-offset_x", off_x, "-offset_y", off_y, "-video_size", dimensions, "-i", "desktop", out_file, "-loglevel", "error"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    except Exception as e:
        print(e)


def stop_recording():
    start_stop_btn.config(text='Start')
    hint_lbl.config(text='Press Start to Start Recording', foreground='#388e3c')

    global rec_proc

    rec_proc.communicate(b'q')
    showinfo(title='Info', message='File Saved Successfuly')


def btn_handler():
    out_file = file_entry.get()

    global recording
    recording = not recording

    if out_file != '':
        if recording:
            start_recording()

        else:
            stop_recording()

    else:
        showerror(title='Error', message='File path is not provided')


def open_file_dialog():
    location = fd.asksaveasfilename(title='Choose Destination', initialfile='Output', defaultextension='mp4', filetypes=[('All Files', '*')])
    file_entry.delete(0, 100)
    file_entry.insert(0, location)


root = tk.Tk()
root.title('Record Screen')
root.resizable(False, False)

frame = Frame(root)
frame.pack(padx=8, pady=8)

file_lbl = Label(frame, text='Filename')
file_lbl.grid(row=0, column=0, padx=4, pady=4, sticky='w')

file_entry = Entry(frame, width=24)
file_entry.grid(row=0, column=1, pady=4)

file_dialog = Button(frame, text='...', width=4, command=open_file_dialog)
file_dialog.grid(row=0, column=2, padx=4, pady=4)

label_res = Label(frame, text='Dimension')
label_res.grid(row=1, column=0, padx=4, pady=4, sticky='w')

res_frame = Frame(frame)
res_frame.grid(row=1, column=1, pady=4, sticky='w')

res_lbl_x = Label(res_frame, text='X:')
res_lbl_x.grid(row=0, column=0, padx=4)

res_x = Entry(res_frame, width=8)
res_x.grid(row=0, column=1, padx=(0, 6))

res_lbl_y = Label(res_frame, text='Y:')
res_lbl_y.grid(row=0, column=2, padx=4)

res_y = Entry(res_frame, width=8)
res_y.grid(row=0, column=3, padx=(0, 6))

res_x.insert(0, '1920')
res_y.insert(0, '1080')

offset_lbl = Label(frame, text='Offset')
offset_lbl.grid(row=2, column=0, padx=4, pady=4, sticky='w')

offset_frame = Frame(frame)
offset_frame.grid(row=2, column=1, pady=4, sticky='w')

offset_lbl_x = Label(offset_frame, text='X:')
offset_lbl_x.grid(row=0, column=0, padx=4)

offset_x = Entry(offset_frame, width=8)
offset_x.grid(row=0, column=1, padx=(0, 8))

offset_lbl_y = Label(offset_frame, text='Y:')
offset_lbl_y.grid(row=0, column=2, padx=4)

offset_y = Entry(offset_frame, width=8)
offset_y.grid(row=0, column=3, padx=(0, 8))

offset_x.insert(0, '0')
offset_y.insert(0, '0')

fps_lbl = Label(frame, text='FPS')
fps_lbl.grid(row=3, column=0, padx=4, pady=4, sticky='w')

fps_spin = Spinbox(frame, width=4)
fps_spin.grid(row=3, column=1, padx=4, pady=4, sticky='w')
fps_spin.set(30)

action_btn_frame = Frame(frame)
action_btn_frame.grid(row=4, column=0, columnspan=3, pady=(24, 4))

recording = False
rec_proc = None

start_stop_btn = Button(action_btn_frame, text='Start', command=btn_handler)
start_stop_btn.grid(row=0, column=0, padx=2)

exit_btn = Button(action_btn_frame, text='Exit', command=root.destroy)
exit_btn.grid(row=0, column=1, padx=2)

hint_lbl = Label(frame, text='Press Start to start recording', foreground='#388e3c')
hint_lbl.grid(row=6, column=0, columnspan=3, padx=4)

root.mainloop()
