# NOT YET IMPLEMENTED, JUST RETURNS SAME STRING

class WeatherSpeech:
    def __init__(self, weathertext):
        self.weathertext = weathertext

    def returnspeech(self):
        if self.weathertext == "thunderstorm with light rain":
            return "it looks like there is a thunderstorm with a little bit of rain."
        if self.weathertext == "thunderstorm with rain":
            return "it looks like there is a thunderstorm with rain."
        if self.weathertext == "thunderstorm with heavy rain":
            return "it looks like there is a thunderstorm with heavy rain."
        if self.weathertext == "light thunderstorm":
            return "it looks like there is a light thunderstorm."
        if self.weathertext == "thunderstorm":
            return "there is currently a thunderstorm."
        if self.weathertext == "heavy thunderstorm":
            return "there is a heavy thunderstorm outside. Be careful!"
        if self.weathertext == "ragged thunderstorm":
            return "there is a ragged thunderstorm."
        if self.weathertext == "thunderstorm with light drizzle":
            return "there is a thunderstorm with a light drizzle."
        if self.weathertext == "thunderstorm with drizzle":
            return "there is a thunderstorm with drizzle."
        if self.weathertext == "thunderstorm with heavy drizzle":
            return "there is a thunderstorm with a heavy drizzle."
        if self.weathertext == "light intensity drizzle":
            return "there is currently a light drizzle outside."
        if self.weathertext == "drizzle":
            return "there is currently a drizzle outside."
        if self.weathertext == "heavy intensity drizzle":
            return "there is a heavy drizzle outside."
        if self.weathertext == "light intensity drizzle rain":
            return "there is some light inteisity drizzle rain outside."
        if self.weathertext == "drizzle rain":
            return "there is some drizzle rain outside."
        if self.weathertext == "heavy intensity drizzle rain":
            return "there is a heavy intensity drizzle rain outside."
        if self.weathertext == "shower rain and drizzle":
            return "we are having a rain shower and drizzle combo outside."
        if self.weathertext == "heavy shower rain and drizzle":
            return "there is a combination of heavy rain shower and drizzle outside."
        if self.weathertext == "shower drizzle":
            return "there is a shower drizzle outside."
        if self.weathertext == "light rain":
            return "we have some light rain outside."
        if self.weathertext == "moderate rain":
            return "we have some moderate rain outside."
        if self.weathertext == "heavy intensity rain":
            return "we have heavy intensity rain outside."
        if self.weathertext == "very heavy rain":
            return "we are experiencing heavy rain outside."
        if self.weathertext == "extreme rain":
            return "we are experiencing extreme rainfall outside. Be careful!"
        if self.weathertext == "freezing rain":
            return "We are experiencing freezing rain outside."
        if self.weathertext == "light intensity shower rain":
            return "there is a light intensity rain shower outside."
        if self.weathertext == "shower rain":
            return "we have a rain shower outside."
        if self.weathertext == "heavy intensity shower rain":
            return "there is a heavy intensity rain shower outside."
        if self.weathertext == "ragged shower rain":
            return "there is a ragged rain shower outside."
        if self.weathertext == "light snow":
            return "we have light snow outside."
        if self.weathertext == "Snow":
            return "it is currently snowing."
        if self.weathertext == "Heavy snow":
            return "we are experiencing heavy snow outside."
        if self.weathertext == "Sleet":
            return "we are currently experiencing sleet outside."
        if self.weathertext == "Light shower sleet":
            return "we are currently experiencing a light sleet shower outside."
        if self.weathertext == "Shower sleet":
            return "we are currently experiencing a sleet shower outside."
        if self.weathertext == "Light rain and snow":
            return "there is currently a mix of light rain and snow outside."
        if self.weathertext == "Rain and snow":
            return "there is currently a mix of rain and snow outside."
        if self.weathertext == "Light shower snow":
            return "there is a light snow shower outside."
        if self.weathertext == "Shower snow":
            return "we are in a snow shower."
        if self.weathertext == "Heavy shower snow":
            return "we are in a heavy snow shower."
        if self.weathertext == "mist":
            return "there is an abundance of mist outside."
        if self.weathertext == "Smoke":
            return "there is a lot of smoke outside. Be careful!"
        if self.weathertext == "Haze":
            return "it is looking pretty hazy outside."
        if self.weathertext == "sand/ dust whirls":
            return "there are some sand and dust whirls outside. Be careful."
        if self.weathertext == "fog":
            return "there is some fog outside. Be careful driving!"
        if self.weathertext == "sand":
            return "there is a lot of sand outside."
        if self.weathertext == "dust":
            return "there is a lot of dust outside."
        if self.weathertext == "volcanic ash":
            return "there is a lot of volcanic ash outside. Be careful!"
        if self.weathertext == "squalls":
            return "there are some squalls outside."
        if self.weathertext == "tornado":
            return "there is a potential tornado outside. Be careful!"
        if self.weathertext == "clear sky":
            return "there's a clear sky outside."
        if self.weathertext == "few clouds: 11-25%":
            return "there are a few clouds outside."
        if self.weathertext == "scattered clouds: 25-50%":
            return "there are some scattered clouds outside."
        if self.weathertext == "broken clouds: 51-84%":
            return "there are a few broken clouds outside."
        if self.weathertext == "overcast clouds: 85-100%":
            return "it is currently overcast."