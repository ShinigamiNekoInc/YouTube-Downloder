import pytube
from pytube import YouTube
from pytube import Playlist

def main():
    userLink = 'https://www.youtube.com/watch?v=Y7VGOnV2QhU&ab_channel=PrettyRecklessVEVO'
    #video = YouTube(userLink)
    #video_link = video.streams.filter(file_extension='mp4')
    #video_link.download()
    YouTube(userLink).streams.first().download()
    print("Done!")
    

if __name__ == "__main__":
    main()
