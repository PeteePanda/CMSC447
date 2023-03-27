from flask import Flask, jsonify
from helperFxns import *

app = Flask(__name__)
database = Lyridact_DB("data.db")


@app.route('/api/db/reset')
def api_resetDB():
    return(jsonify(database.reset()))


if __name__ == "__main__":
    app.run(debug=True)