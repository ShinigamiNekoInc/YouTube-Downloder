import pytube
from pytube import YouTube
from pytube import Playlist

import tkinter as tk

root = tk.Tk()
root.geometry('500x300') # Size of the window
root.resizable(0, 0) # makes the window adjustable with its features
root.title('youtube downloader')

tk.Label(root, text = 'Youtube Video Downloader', font ='arial 20 bold').pack()
tk.Label(root, text = 'Paste Link Here:', font = 'arial 15 bold').place(x = 160 , y = 60)
link = tk.StringVar()
link_enter = tk.Entry(root, width = 70,textvariable = link).place(x = 32, y = 90)


def DownloaderVideo():
    Downloader(False)

def DownloaderAudio():
    Downloader(True)

def get_link_type (_Link, flag_AudioOnly):
    if flag_AudioOnly == True:
        video_link = _Link.streams.get_audio_only()
    else:
        video_link = _Link.streams.get_highest_resolution()
    return video_link

def Downloader(flag_AudioOnly):
    userLink = str(link.get())
    if userLink:
        result = userLink.find("?list=")
        if result != -1:
            user_Playlist = Playlist(userLink)
            i = 1
            i_sum = len(user_Playlist)
            for video in user_Playlist.videos:
                print("Downloading...")
                video_link = get_link_type(video, flag_AudioOnly)
                video_link.download()
                print("Downloaded " + str(i) + " of " + str(i_sum))
                i = i + 1
        else:
             video = YouTube(userLink)
             video_link = get_link_type(video, flag_AudioOnly)
             video_link.download()
             
        text.set("Downloaded!")

tk.Button(root, text = 'Download audio', font = 'arial 15 bold' ,bg = 'pale violet red', padx = 2, command = DownloaderAudio).place(x=70 ,y = 150)
tk.Button(root, text = 'Download video', font = 'arial 15 bold' ,bg = 'pale violet red', padx = 2, command = DownloaderVideo).place(x=250 ,y = 150)

text = tk.StringVar()
text.set("Waiting user...")

tk.Label(root, textvariable = text, font = 'arial 15').place(x = 180 , y = 210)


root.mainloop()
