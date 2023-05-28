from tkinter import ttk
import threading
import time
from tkinter import *
import os
from tkinter import filedialog
import tkinter.messagebox
from pygame import mixer
from mutagen.mp3 import MP3

root = Tk()

statusbar = ttk.Label(root, text="Music Player", relief=SUNKEN, anchor=W,font='Time 15 bold',background='red',foreground="white")
statusbar.pack(side=BOTTOM, fill=X)

menuebar = Menu(root)
root.config(menu=menuebar)
#root.geometry("300x600")
submenue = Menu(menuebar, tearoff=0)

playlist=[]
#playlist it contains the full path + file name

def browse():
    global filename_path
    filename_path = filedialog.askopenfilename()
    ad_to_list(filename_path)

def ad_to_list(filename):
    filename= os.path.basename(filename_path)
    index=0
    Lb1.insert(index, filename)
    playlist.insert(index,filename_path)
    index+=1

menuebar.add_cascade(label='File', menu=submenue)
submenue.add_command(label='Open', command=browse)
submenue.add_command(label='Exit', command=root.destroy)


def abut():
    tkinter.messagebox.showinfo('About My Music', 'First Project on Python')


submenue = Menu(menuebar, tearoff=0)
menuebar.add_cascade(label='Help', menu=submenue)
submenue.add_command(label='About Us', command=abut)

mixer.init()

root.title("My Music")


leftframe=Frame(root)
leftframe.pack(side=LEFT,padx=30)

Lb1 = Listbox(leftframe)
Lb1.pack()


addbtn=ttk.Button(leftframe, text="Add",command=browse)
addbtn.pack(side=LEFT)

def del_song():
    selected_song = Lb1.curselection()
    selected_song = int(selected_song[0])
    Lb1.delete(selected_song)
    playlist.pop(selected_song)


deletbtn=ttk.Button(leftframe, text="Del",command=del_song)
deletbtn.pack(side=LEFT)

rightframe=Frame(root)
rightframe.pack(side=LEFT)

topframe=Frame(rightframe)
topframe.pack()

lengthtext = ttk.Label(topframe, text='Total Length - 00:00',font='Arial 12 bold')
lengthtext.pack(pady=5)

Currenttime = ttk.Label(topframe, text='Current Time - 00:00',relief=GROOVE)
Currenttime.pack()



# lablephoto=Label(root,image=photo)
# lablephoto.pack()

def show_details(play_song):
    file_data=os.path.splitext(play_song)

    if file_data[1]=='.mp3':
        audio=MP3(play_song)
        total_length=audio.info.length
    else:
        a=mixer.sound(play_song)
        total_length=a.get_length()

    #div diving by 60 and mod find the reminder
    mins,secs=divmod(total_length,60)
    mins=round(mins)
    secs=round(secs)
    timeformat='{:02d}:{:02d}'.format(mins,secs)
    lengthtext['text'] = "Total Length" + " - " + timeformat

    t1=threading.Thread(target=start_count,args=(total_length,))
    t1.start()

def start_count(t):
    global paused
    #mixer.music.get_busy():- it returns the fales when we press stop button
    current_time=0
    while current_time<=t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            Currenttime['text'] = "Current Time" + " - " + timeformat
            time.sleep(1)
            current_time+=1



def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Playing" + " " + os.path.basename(filename_path)
        paused = FALSE
        #playbtn.config(image=pausephoto, command=pause_music)

    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song=Lb1.curselection()
            selected_song= int(selected_song[0])
            play_it=playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing" + " " + os.path.basename(play_it)
            show_details(play_it)
            #playbtn.config(image=pausephoto,command=pause_music)
        except:
           tkinter.messagebox.showerror("Error", "No File Selected")


paused = FALSE


def pause_music():

    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = 'Music Paused'
    #playbtn.config(image=playphoto,command=play_music)


def stop_music():

    global paused
    mixer.music.stop()
    statusbar['text'] = "Stopped"
    paused = FALSE


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)


mute = FALSE


def vol_music():

    global mute
    if mute:
        volbtn.config(image=volphoto)
        scale.set(50)
        mixer.music.set_volume(0.50)
        mute = FALSE
    else:
        volbtn.config(image=mutephoto)
        scale.set(0)
        mixer.music.set_volume(0)
        mute = TRUE


middleframe = Frame(rightframe)
middleframe.pack(pady=10)

playphoto = PhotoImage(file=r'C:/Users/subhash/Pictures/play.png')
playbtn = ttk.Button(middleframe, image=playphoto, command=play_music)
playbtn.grid(row=0, column=0, padx=10)

pausephoto = PhotoImage(file=r'C:\Users\subhash\Pictures\pause.png')
pausebtn = ttk.Button(middleframe, image=pausephoto, command=pause_music)
pausebtn.grid(row=0, column=1, padx=10)

stopphoto = PhotoImage(file=r'C:\Users\subhash\Pictures\stop.png')
stopbtn = ttk.Button(middleframe, image=stopphoto, command=stop_music)
stopbtn.grid(row=0, column=2, padx=10)

bottomframe = Frame(rightframe)
bottomframe.pack(pady=10)

mutephoto = PhotoImage(file=r'C:\Users\subhash\Pictures\mute.png')
volphoto = PhotoImage(file=r'C:\Users\subhash\Pictures\volume.png')
volbtn = ttk.Button(bottomframe, image=volphoto, command=vol_music)
volbtn.grid(row=1, column=2, padx=10)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(50)
mixer.music.set_volume(0.5)
scale.grid(row=1, column=3, pady=15)


def on_closing():
    stop_music()
    root.destroy()

root.protocol("WM_DELETE_WINDOW",on_closing)
root.mainloop()
