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
        if self.weekdaynum == 0:
            if self.timeofdaynum >= 0 and self.timeofdaynum < 8:
                return "https://www.youtube.com/playlist?list=PLjzeyhEA84sQKuXp-rpM1dFuL2aQM_a3S"
            if self.timeofdaynum >= 8 and self.timeofdaynum < 12:
                return "https://www.youtube.com/playlist?list=PLOci2rRb5g3iUxFh_olD0dWGpzWPwdlOi"
            if self.timeofdaynum >= 12 and self.timeofdaynum < 16:
                return "https://www.youtube.com/playlist?list=PLGBuKfnErZlD_VXiQ8dkn6wdEYHbC3u0i"
            if self.timeofdaynum >= 16 and self.timeofdaynum < 20:
                return "https://www.youtube.com/playlist?list=PLNxOe-buLm6cz8UQ-hyG1nm3RTNBUBv3K" 
            if self.timeofdaynum >= 20 and self.timeofdaynum < 24:
                return "https://www.youtube.com/playlist?list=PL4033C6D21D7D28AC"
        
        if self.weekdaynum == 1:
            if self.timeofdaynum >= 0 and self.timeofdaynum < 8:
                return "https://www.youtube.com/playlist?list=PLwIEpqpG3Tr8aI2HwnT1YwNtDMVKf8KUO"
            if self.timeofdaynum >= 8 and self.timeofdaynum < 12:
                return "https://www.youtube.com/playlist?list=PL7IiPgV2w_VZn8EgvZR8ohux9A5uup91n" 
            if self.timeofdaynum >= 12 and self.timeofdaynum < 16:
                return "https://www.youtube.com/playlist?list=PLqEuUDDiORrjQk6OzZ1xhPiVE8DYglCqe"
            if self.timeofdaynum >= 16 and self.timeofdaynum < 20:
                return "https://www.youtube.com/playlist?list=PLGbwKffY2xoKTszTk57KAuLY26xAClErq"
            if self.timeofdaynum >= 20 and self.timeofdaynum < 24:
                return "https://www.youtube.com/playlist?list=PLhmtZUpTH9coZD4Y0XNID7tZFmLo1bytt"
        
        if self.weekdaynum == 2:
            if self.timeofdaynum >= 0 and self.timeofdaynum < 8:
                return "https://www.youtube.com/playlist?list=PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj" 
            if self.timeofdaynum >= 8 and self.timeofdaynum < 12:
                return "https://www.youtube.com/playlist?list=PL7IiPgV2w_VaEvjQ8YedFjlcGTbhCze9U"
            if self.timeofdaynum >= 12 and self.timeofdaynum < 16:
                return "https://www.youtube.com/playlist?list=PL7Q2ZklqtR8B_EAUfXt5tAZkxhCApfFkL"
            if self.timeofdaynum >= 16 and self.timeofdaynum < 20:
                return "https://www.youtube.com/playlist?list=PLpuDUpB0osJmZQ0a3n6imXirSu0QAZIqF" 
            if self.timeofdaynum >= 20 and self.timeofdaynum < 24:
                return "https://www.youtube.com/playlist?list=PLetgZKHHaF-Zq1Abh-ZGC4liPd_CV3Uo4" 

        if self.weekdaynum == 3:
            if self.timeofdaynum >= 0 and self.timeofdaynum < 8:
                return "https://www.youtube.com/playlist?list=PL4QNnZJr8sRNKjKzArmzTBAlNYBDN2h-J"
            if self.timeofdaynum >= 8 and self.timeofdaynum < 12:
                return "https://www.youtube.com/playlist?list=PLV9du90-nOngPg_V4By29gvrovqAguGuN" 
            if self.timeofdaynum >= 12 and self.timeofdaynum < 16:
                return "https://www.youtube.com/playlist?list=PLwg8VB64LkBIxBe-PdjFO-7TTMxi9k1ro" 
            if self.timeofdaynum >= 16 and self.timeofdaynum < 20:
                return "https://www.youtube.com/playlist?list=PLX9U3Rv7Wy7Wbi3iV2uxFo8BOVHjIehUc" 
            if self.timeofdaynum >= 20 and self.timeofdaynum < 24:
                return "https://www.youtube.com/playlist?list=PLrZlOVu0fKqHo1ilGq8vYCuC7mUWej_nP"

        if self.weekdaynum == 4:
            if self.timeofdaynum >= 0 and self.timeofdaynum < 8:
                return "https://www.youtube.com/playlist?list=PLCD0445C57F2B7F41" 
            if self.timeofdaynum >= 8 and self.timeofdaynum < 12:
                return "https://www.youtube.com/playlist?list=PLGBuKfnErZlAkaUUy57-mR97f8SBgMNHh" 
            if self.timeofdaynum >= 12 and self.timeofdaynum < 16:
                return "https://www.youtube.com/playlist?list=PLGBuKfnErZlCkRRgt06em8nbXvcV5Sae7"
            if self.timeofdaynum >= 16 and self.timeofdaynum < 20:
                return "https://www.youtube.com/playlist?list=PLRZlMhcYkA2Fhwg-NxJewUIgm01o9fzwB"
            if self.timeofdaynum >= 20 and self.timeofdaynum < 24:
                return "https://www.youtube.com/playlist?list=PLXRivw5Pd9qlM5efsL4c7js8teYFVy3Dk"

        if self.weekdaynum == 5:
            if self.timeofdaynum >= 0 and self.timeofdaynum < 8:
                return "https://www.youtube.com/playlist?list=PLxvodScTx2RtAOoajGSu6ad4p8P8uXKQk"
            if self.timeofdaynum >= 8 and self.timeofdaynum < 12:
                return "https://www.youtube.com/playlist?list=PLrnb8c3hFJatjyJ-wFMuFGANNoo7-LZsG" 
            if self.timeofdaynum >= 12 and self.timeofdaynum < 16:
                return "https://www.youtube.com/playlist?list=PL4BrNFx1j7E5qDxSPIkeXgBqX0J7WaB2a" 
            if self.timeofdaynum >= 16 and self.timeofdaynum < 20:
                return "https://www.youtube.com/playlist?list=PL6rfTXx-6y2U9LPalxmyWb4Z9_YDomxfs" 
            if self.timeofdaynum >= 20 and self.timeofdaynum < 24:
                return "https://www.youtube.com/playlist?list=PLbcjjn493-S_DcwEVTPkVRz5zZQSo3hjE"

        if self.weekdaynum == 6:
            if self.timeofdaynum >= 0 and self.timeofdaynum < 8:
                return "https://www.youtube.com/playlist?list=PLiy0XOfUv4hFHmPs0a8RqkDzfT-2nw7WV"
            if self.timeofdaynum >= 8 and self.timeofdaynum < 12:
                return "https://www.youtube.com/playlist?list=PL8F6B0753B2CCA128" 
            if self.timeofdaynum >= 12 and self.timeofdaynum < 16:
                return "https://www.youtube.com/playlist?list=PLDC827E741DA933F0" 
            if self.timeofdaynum >= 16 and self.timeofdaynum < 20:
                return "https://www.youtube.com/playlist?list=PLk-_AvR22RueziRgt5GVuirih223y1UNJ" 
            if self.timeofdaynum >= 20 and self.timeofdaynum < 24:
                return "https://www.youtube.com/playlist?list=PL3O5lr1JOzLe6CXisC7PSbveY6IBLxdlg" 
    
    def get_weekdaytext(self):
        if self.weekdaynum == 0:
            if self.timeofdaynum >= 0 and self.timeofdaynum < 8:
                return "Well, it's Monday. Why are you up so early? We're playing rock music all day! Let's start off your early morning with some blues music."
            if self.timeofdaynum >= 8 and self.timeofdaynum < 12:
                return "Well, it's Monday morning. We're playing rock music all day! Let's get your day started with some punk rock."
            if self.timeofdaynum >= 12 and self.timeofdaynum < 16:
                return "Hope you're having a solid Monday afternoon. We're playing rock music all day! Let's get the blood pumping with some heavy metal."
            if self.timeofdaynum >= 16 and self.timeofdaynum < 20:
                return "It's Monday evening. We're playing rock music all day! Here's some classics that you should be familiar with."
            if self.timeofdaynum >= 20 and self.timeofdaynum < 24:
                return "It's Monday night. Let's end the day the right way with some death metal."
        
        if self.weekdaynum == 1:
            if self.timeofdaynum >= 0 and self.timeofdaynum < 8:
                return "It's officially Tuesday. Today, we're focusing on comedy, parodies, and generally weird music! Let's start with some comedy rock."
            if self.timeofdaynum >= 8 and self.timeofdaynum < 12:
                return "It's Tuesday morning. Today, we're focusing on comedy, parodies, and generally weird music! Here's some messed up music with weird edits to get you going!"
            if self.timeofdaynum >= 12 and self.timeofdaynum < 16:
                return "It's Tuesday afternoon. We're focusing on comedy, parodies, and generally weird music! Right now, you're listening to some masterpieces from YouTuber Magik Mike!"
            if self.timeofdaynum >= 16 and self.timeofdaynum < 20:
                return "It's Tuesday evening. We're focusing on comedy, parodies, and generally weird music! Let's listen to some hits from Weird Al Yankovic!"
            if self.timeofdaynum >= 20 and self.timeofdaynum < 24:
                return "It's Tuesday night. Let's end the day of weird music with some horror country."
        
        if self.weekdaynum == 2:
            if self.timeofdaynum >= 0 and self.timeofdaynum < 8:
                return "It's officially hump day. Today's theme is nostalgic music! Time for you to jam out to some recent pop hits."
            if self.timeofdaynum >= 8 and self.timeofdaynum < 12:
                return "It's the morning of hump day. Today's theme is nostalgic music! Let's get you started with some internet classics."
            if self.timeofdaynum >= 12 and self.timeofdaynum < 16:
                return "It's Wednesday afternoon. You've made it over the hump of hump day! Today's theme is nostalgic music, and we're listening to music around 2010."
            if self.timeofdaynum >= 16 and self.timeofdaynum < 20:
                return "It's Wednesday night. The theme is nostalgic music. We'll go further back in time and listen to music from the 2000s."
            if self.timeofdaynum >= 20 and self.timeofdaynum < 24:
                return "It's Wednesday night. Let's end the day with some hip hop and rap."

        if self.weekdaynum == 3:
            if self.timeofdaynum >= 0 and self.timeofdaynum < 8:
                return "It's now Thursday morning, and early at that. Today we're focusing on music from around the world. Let's start with some K pop."
            if self.timeofdaynum >= 8 and self.timeofdaynum < 12:
                return "It's Thursday morning. Today we're focusing on music from around the world. You're about to hear country anthems and world propaganda."
            if self.timeofdaynum >= 12 and self.timeofdaynum < 16:
                return "Thursday afternoon. We're focusing on music from around the world. Let's listen to some Mongolian Throat Singing."
            if self.timeofdaynum >= 16 and self.timeofdaynum < 20:
                return "It's Thursday evening. We're focusing on music from around the world. Now, let's take a trip to Africa."
            if self.timeofdaynum >= 20 and self.timeofdaynum < 24:
                return "It's Thursday night. Let's end our world music theme with some American patriotic music."

        if self.weekdaynum == 4:
            if self.timeofdaynum >= 0 and self.timeofdaynum < 8:
                return "It's early Friday morning. Today's decade day! We'll start by listening to the best of the eighties."
            if self.timeofdaynum >= 8 and self.timeofdaynum < 12:
                return "Friday is here. Today's decade day! Next, we'll hear the best of the seventies."
            if self.timeofdaynum >= 12 and self.timeofdaynum < 16:
                return "It's Friday afternoon. Today's decade day! We're moving on to the best of the sixties."
            if self.timeofdaynum >= 16 and self.timeofdaynum < 20:
                return "It's Friday evening. Today's decade day! Let's listen to the best of the 40s!"
            if self.timeofdaynum >= 20 and self.timeofdaynum < 24:
                return "It's Friday night. Let's end the day with music from the roaring twenties!"

        if self.weekdaynum == 5:
            if self.timeofdaynum >= 0 and self.timeofdaynum < 8:
                return "Today's Saturday, time to relax and have fun! We'll start the morning with some orchestral music."
            if self.timeofdaynum >= 8 and self.timeofdaynum < 12:
                return "Today's Saturday, time to relax and have fun! Let your morning begin with popular video game soundtracks."
            if self.timeofdaynum >= 12 and self.timeofdaynum < 16:
                return "Today's Saturday, time to relax and have fun! Let's continue your afternoon with some film scores!"
            if self.timeofdaynum >= 16 and self.timeofdaynum < 20:
                return "Today's Saturday, time to relax and have fun! Now that it's the evening, we'll listen to songs in musical theater."
            if self.timeofdaynum >= 20 and self.timeofdaynum < 24:
                return "It's Saturday night, still time to relax and have fun! We'll end the day with some pirate metal."

        if self.weekdaynum == 6:
            if self.timeofdaynum >= 0 and self.timeofdaynum < 8:
                return "It's Sunday. We're serving jazz all day baby. Smooth jazz will be deployed in 3, 2, 1."
            if self.timeofdaynum >= 8 and self.timeofdaynum < 12:
                return "It's Sunday morning. We're serving jazz all day baby. Let's start your morning by listening to important figures in jazz."
            if self.timeofdaynum >= 12 and self.timeofdaynum < 16:
                return "It's Sunday afternoon. We're serving jazz all day baby. Time to get moving to some big band music."
            if self.timeofdaynum >= 16 and self.timeofdaynum < 20:
                return "It's Sunday evening. We're serving jazz all day baby. Let's cool down to some bossa nova."
            if self.timeofdaynum >= 20 and self.timeofdaynum < 24:
                return "It's Sunday night. Let's end the day with some jazz fusion."
    
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