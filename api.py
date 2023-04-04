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
    return(jsonify(database.sendTodaySongs()))

@app.route('/api/updateUser', methods=['POST'])
def api_updateUser():
    cookie = request.cookies.get('cookie')
    content = request.get_json()
    wordList = content['words']
    level = content['level']
    database.updateUser(cookie, wordList, level)
    return ('', 204)
    

@app.route('/', methods=['GET'])
def homePage():

    cookie = request.cookies.get('cookie')
    user = database.getUserFromCookie(cookie)
    if not user:
        resp = make_response(render_template("index.html", wordlist=[], level=1))
        newCookie = generateCookie()
        resp.set_cookie('cookie', newCookie)
        database.addNewUser(newCookie)
        return resp
    else:
        print(user)
        person = json.loads(user[0][0])
        return render_template("index.html", wordlist=person['wordsUsed'], currentLevel=person['levelsUnlocked'])

        
   

        



    


if __name__ == "__main__":
    app.run(debug=True)