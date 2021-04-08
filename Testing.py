"""
UNIT TESTING:
- Case 1: Negative port number
- Case 2: Negative value for maximum song length
- Case 3: City name as int instead of string
- Case 4: Playlist URL links to different website
- Case 5: Negative number in random bounds
"""

# Import Unittest module
import unittest

# Import RadioHost class
from RadioHost import RadioHost

# Custom error for a negative port number
class NegativePortNumber(Exception):
    pass

# Custom error for negative value in song length
class NegativeMaximumSongLength(Exception):
    pass

# Custom error if playlist URL is not in correct domain
class PlaylistDomainError(Exception):
    pass

# Custom error for negative value in random bounds
class NegativeRandomBounds(Exception):
    pass

class TestRadio(unittest.TestCase):
    def setUp(self):
        self.maininstance = RadioHost()

    def test_negative_port(self):
        testinstance = lambda: self.maininstance.startradio("TestPort",False)
        try:
            self.assertRaises(NegativePortNumber, testinstance)
        except AssertionError:
            print("Success.")
    
    def test_negative_song_length(self):
        testinstance = lambda: self.maininstance.startradio("TestSongLength",False)
        try:
            self.assertRaises(NegativeMaximumSongLength, testinstance)
        except AssertionError:
            print("Success.")
    
    def test_city_name_as_string(self):
        testinstance = lambda: self.maininstance.startradio("TestCityName",False)
        try:
            self.assertRaises(TypeError, testinstance)
        except AssertionError:
            print("Success.")
    
    def test_playlist_URL_in_domain(self):
        testinstance = lambda: self.maininstance.startradio("TestPlaylistDomain",False)
        try:
            self.assertRaises(PlaylistDomainError, testinstance)
        except AssertionError:
            print("Success.")
    
    def test_negative_random_bounds(self):
        testinstance = lambda: self.maininstance.startradio("TestRandomBounds",False)
        try:
            self.assertRaises(NegativeRandomBounds, testinstance)
        except AssertionError:
            print("Success.")

if __name__ == '__main__':
    unittest.main()