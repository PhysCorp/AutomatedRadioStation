# Import modules
import youtube_dl # Video downloading
import os # Run external commands in Linux [1/2]
import os.path # Run external commands in Linux [2/2]

class Playlist:
    def __init__(self, weekdaynum, timeofdaynum):
        self.weekdaynum = weekdaynum
        self.timeofdaynum = timeofdaynum
    
    def download_entire_playlist(self, url):
        # Determine main program directory
        maindirectory = os.path.dirname(os.path.abspath(__file__)) # The absolute path to this file
        # Download the playlist with YouTube-DL
        downloadlist = []
        downloadlist.append(str(url))
        ydl_opts = {"outtmpl": str(maindirectory) + "/DownloadedSongs/%(id)s.%(ext)s", "ignoreerrors": True, "format": "bestaudio[ext=m4a]", "geobypass": True, "noplaylist": True, "source_address": "0.0.0.0", "download_archive": str(maindirectory) + "/SongArchive.txt", "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "vorbis"}]}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(downloadlist)
            # info = ydl.extract_info(musicplaylist, download=True)

    def get_URL(self):
        if self.weekdaynum == 0 or self.weekdaynum == 2 or self.weekdaynum == 4 or self.weekdaynum == 6:
            if self.timeofdaynum >= 0 and self.timeofdaynum < 8:
                return "https://www.youtube.com/playlist?list=PLOfwJR8nfyhq97jFb1ucscqPQSQh3v00G"
            if self.timeofdaynum >= 8 and self.timeofdaynum < 12:
                return "https://www.youtube.com/playlist?list=PLlt4xZeez_gk74mAMH_BdJ5wIWK4uCCOz"
            if self.timeofdaynum >= 12 and self.timeofdaynum < 16:
                return "https://www.youtube.com/playlist?list=PLp7pAH9am84PWy7pcQDmQBZCZ0xMXFtCS"
            if self.timeofdaynum >= 16 and self.timeofdaynum < 20:
                return "https://www.youtube.com/playlist?list=PL6F9CFDEB562DF8E1" 
            if self.timeofdaynum >= 20 and self.timeofdaynum < 24:
                return "https://www.youtube.com/playlist?list=PLdgIMWt3XyJz_vJUnAln8ca0o-58k1iVk"
        
        if self.weekdaynum == 1 or self.weekdaynum == 3 or self.weekdaynum == 5:
            if self.timeofdaynum >= 0 and self.timeofdaynum < 8:
                return "https://www.youtube.com/playlist?list=PLdgIMWt3XyJz_vJUnAln8ca0o-58k1iVk"
            if self.timeofdaynum >= 8 and self.timeofdaynum < 12:
                return "https://www.youtube.com/playlist?list=PL6F9CFDEB562DF8E1" 
            if self.timeofdaynum >= 12 and self.timeofdaynum < 16:
                return "https://www.youtube.com/playlist?list=PLp7pAH9am84PWy7pcQDmQBZCZ0xMXFtCS"
            if self.timeofdaynum >= 16 and self.timeofdaynum < 20:
                return "https://www.youtube.com/playlist?list=PLlt4xZeez_gk74mAMH_BdJ5wIWK4uCCOz"
            if self.timeofdaynum >= 20 and self.timeofdaynum < 24:
                return "https://www.youtube.com/playlist?list=PLOfwJR8nfyhq97jFb1ucscqPQSQh3v00G"
    
    def get_weekdaytext(self):
        if self.weekdaynum == 0 or self.weekdaynum == 2 or self.weekdaynum == 4 or self.weekdaynum == 6:
            if self.timeofdaynum >= 0 and self.timeofdaynum < 8:
                return "Why are you up so early? Regardless, let's start off your early morning with some well-known classical music."
            if self.timeofdaynum >= 8 and self.timeofdaynum < 12:
                return "Good morning! Let's get your day started with the best of Mozart."
            if self.timeofdaynum >= 12 and self.timeofdaynum < 16:
                return "Hope you're having a great afternoon. Let's listen to some well-known baroque music."
            if self.timeofdaynum >= 16 and self.timeofdaynum < 20:
                return "Good evening. Here are some songs with the chaconne classical style."
            if self.timeofdaynum >= 20 and self.timeofdaynum < 24:
                return "Let's end the day by continuing chaconne music, focusing on the works of Bach."
        
        if self.weekdaynum == 1 or self.weekdaynum == 3 or self.weekdaynum == 5:
            if self.timeofdaynum >= 0 and self.timeofdaynum < 8:
                return "Why are you up so early? Regardless, let's start off your early morning with chaconne music, focusing on the works of Bach."
            if self.timeofdaynum >= 8 and self.timeofdaynum < 12:
                return "Good morning! Let's get your day started by continuing songs in the chaconne classical style."
            if self.timeofdaynum >= 12 and self.timeofdaynum < 16:
                return "Hope you're having a great afternoon. Let's listen to some well-known baroque music."
            if self.timeofdaynum >= 16 and self.timeofdaynum < 20:
                return "Good evening. Here are some songs with the best of Mozart."
            if self.timeofdaynum >= 20 and self.timeofdaynum < 24:
                return "Let's end the day by continuing with some well-known classical music."
    
    def get_savedweekday(self):
        return self.weekdaynum
    
    def get_savedtime(self):
        if self.timeofdaynum >= 0 and self.timeofdaynum < 8:
            return "Early Morning"
        if self.timeofdaynum >= 8 and self.timeofdaynum < 12:
            return "Morning"
        if self.timeofdaynum >= 12 and self.timeofdaynum < 16:
            return "Afternoon"
        if self.timeofdaynum >= 16 and self.timeofdaynum < 20:
            return "Evening"
        if self.timeofdaynum >= 20 and self.timeofdaynum < 24:
            return "Late Night"