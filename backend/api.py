from flask import Flask, jsonify
from helperFxns import *

app = Flask(__name__)
database = Lyridact_DB("data.db")


@app.route('/api/db/reset')
def api_resetDB():
    return(jsonify(database.reset()))

@app.route('/api/downloadSongs')
def api_downloadSongs():
    return(jsonify(database.downloadSongs()))

@app.route('/api/getDailySongs')
def api_getSongs():
    return(jsonify(database.sendTodaySongs()))


if __name__ == "__main__":
    app.run(debug=True)