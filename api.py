from flask import Flask, jsonify, make_response, render_template, request
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
    today = datetime.today().strftime('%Y-%m-%d')
    print("RUNNING GET SONGS")
    return(jsonify(database.sendTodaySongs(today)))

@app.route('/api/updateUser', methods=['POST'])
def api_updateUser():
    cookie = request.cookies.get('cookie')
    content = request.get_json()
    wordList = content['words']
    level = content['level']
    database.updateUser(cookie, wordList, level)
    return ('', 204)

@app.route('/api/getLB', methods=['POST'])
def api_getLeaderboard():
    level = request.get_json()['level']
    print(request.get_json())
    lb = database.getLeaderboard(int(level))
    if lb:
        return(jsonify(lb[:5]), 200)
    else:
        return(jsonify([]), 200)

@app.route('/api/addLBScore', methods=['POST'])
def api_addLBScore():
    content = request.get_json()
    points = content['points']
    level = content['level']
    cookie = content['cookie']
    database.addScoreToLeaderboard(points, cookie, int(level))
    return ('', 204)

@app.route('/', methods=['GET'])
def homePage():

    cookie = request.cookies.get('cookie')
    user = database.getUserFromCookie(cookie)
    if not user:
        resp = make_response(render_template("index.html", wordlist=[], currrentLevel=1))
        newCookie = generateCookie()
        resp.set_cookie('cookie', newCookie)
        database.addNewUser(newCookie)
        return resp
    else:
        
        
        return render_template("index.html", wordlist=user['wordsUsed'], currentLevel=user['levelsUnlocked'])

        
   

        



    


if __name__ == "__main__":
    app.run(debug=True)