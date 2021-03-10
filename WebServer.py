# Try to import all modules
try:
    from flask import Flask, request, render_template # Web-management engine
    import json
except ImportError:
    print("[WARN] You are missing one or more libraries. This script cannot continue.")
    print("Try running in terminal >> python3 -m pip install -r requirements.txt")
    quit()

# Init Flask
app = Flask(__name__)

@app.route("/")
def index():
    # Open JSON file
    try:
        with open("VariableDump.json", "r") as json_file:
            statistics_dict_parent = json.load(json_file)
            statistics_dict = statistics_dict_parent["Statistics"][0]
            json_file.close()
    except FileNotFoundError:
        statistics_dict = []
        pass
    return render_template("index.html", PlaylistURL=str(statistics_dict["PlaylistURL"]), SongsPlayedNum=int(statistics_dict["SongsPlayedNum"]), SongTitle=str(statistics_dict["SongTitle"]), EmbedLink=str(statistics_dict["EmbedLink"]), SongLink=str(statistics_dict["SongLink"]), WeatherDecimal=int(statistics_dict["WeatherDecimal"]), PSADecimal=int(statistics_dict["PSADecimal"]), WelcomeDecimal=int(statistics_dict["WelcomeDecimal"]), WeekdayDecimal=int(statistics_dict["WeekdayDecimal"]), TimeDecimal=int(statistics_dict["TimeDecimal"]))

@app.route("/echo", methods=["POST"])
def echo():
    command = request.form["text"]
    print(command)
    return index()

if __name__ == "__main__":
    app.run(debug="False", port=4024, host="0.0.0.0")