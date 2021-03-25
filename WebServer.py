try:
    # Try to import all modules
    try:
        from flask import Flask, request, render_template # Web-management engine
        import json
        from waitress import serve
        import os.path
        import sys
    except ImportError:
        print("[WARN] You are missing one or more libraries. This script cannot continue.")
        print("Try running in terminal >> python3 -m pip install -r requirements.txt")
        quit()

    # Set port number according to script arguments
    if len(sys.argv) > 1:
        webport = int(sys.argv[-1])

    # Determine main program directory
    maindirectory = os.path.dirname(os.path.abspath(__file__)) # The absolute path to this file

    # Custom Functions
    def suggestion_dump(link):
        data = {}
        data["Suggestion"] = []
        data["Suggestion"].append({"Link": str(link)})
        with open(str(maindirectory) + "/SuggestionDump.json", "w") as jsonfile:
            json.dump(data, jsonfile)

    # Init Flask
    app = Flask(__name__)

    print(f"[INFO] WebServer is now running. View station info and suggest songs here with port {webport}.", end="\n\n")

    @app.route("/")
    def index():
        # Open JSON file
        try:
            with open(str(maindirectory) + "/VariableDump.json", "r") as json_file:
                statistics_dict_parent = json.load(json_file)
                statistics_dict = statistics_dict_parent["Statistics"][0]
                json_file.close()
            return render_template("index.html", PlaylistURL=statistics_dict["PlaylistURL"], SongsPlayedNum=statistics_dict["SongsPlayedNum"], SongTitle=statistics_dict["SongTitle"], EmbedLink=statistics_dict["EmbedLink"], SongLink=statistics_dict["SongLink"], WeatherDecimal=statistics_dict["WeatherDecimal"], PSADecimal=statistics_dict["PSADecimal"], WelcomeDecimal=statistics_dict["WelcomeDecimal"], WeekdayDecimal=statistics_dict["WeekdayDecimal"], TimeDecimal=statistics_dict["TimeDecimal"])
        except FileNotFoundError:
            return render_template("index.html")

    @app.route("/", methods=["POST"])
    def echo():
        command = request.form["videosuggestion"]
        suggestion_dump(command)
        print("[INFO] Suggestion received!")
        return index()

    if __name__ == "__main__":
        # app.run(debug="False", port=4024, host="0.0.0.0") # [No longer used. Run app through Flask]
        serve(app, host="0.0.0.0", port=webport) # Start app with waitress

except OSError:
    print("[INFO] The webserver is already running. This instance will exit.", end="\n\n")
    quit()