from flask import Flask, jsonify, make_response, render_template, request
from helperFxns import *


app = Flask(__name__)
database = Lyridact_DB("data.db")

@app.route("/api/PostLeaderboard", methods=['POST'])
def api_postLeaderboard():
    level = request.get_json()['level']
    lb = database.getLeaderboard(int(level))
    if not lb:
        return jsonify([])
    elif len(lb) < 5:
        print("Not enough scores to post")
        return jsonify([])
    else:
        
        prof_url = "https://eope3o6d7z7e2cc.m.pipedream.net/"
        headers = {
            'Content-Type': "application/json"
        }
        data = {
            "data": [
                {
                    "Group": "H",
                    "Title": "Top 5 Scores",
                    f"{lb[0][0]}": f"{lb[0][1]}",
                    f"{lb[1][0]}": f"{lb[1][1]}",
                    f"{lb[2][0]}": f"{lb[2][1]}",
                    f"{lb[3][0]}": f"{lb[3][1]}",
                    f"{lb[4][0]}": f"{lb[4][1]}"
                }
            ]
        }
        res = requests.post(prof_url, headers=headers, data=data)
        if res.status_code == 200:
            print(f"Successfully posted leaderboard {level}")
            print(res.text)
        else:
            print(f"Failed to post leaderboard {level}")
        



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
    user = content['user']
    database.updateUser(cookie, wordList, level, user)
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
    
@app.route('/api/getUsername', methods=['POST'])
def api_getUsername():
    cookie = request.get_json()['cookie']
    username = database.getUserFromCookie(cookie)
    if username:
        return(jsonify(username), 200)
    else:
        return(jsonify(""), 200)

@app.route('/api/addLBScore', methods=['POST'])
def api_addLBScore():
    cookie = request.cookies.get('cookie')
    content = request.get_json()
    points = content['points']
    level = content['level']
    username = content['username']
    database.addScoreToLeaderboard(points, cookie, int(level), username)
    rank = database.getRanking(int(level), points)
    print("rank", rank)
    return jsonify({"rank": rank}), 200

@app.route('/', methods=['GET'])
def homePage():
    cookie = request.cookies.get('cookie')
    user = database.getUserFromCookie(cookie)
    if not user:
        newCookie = generateCookie()
        resp = make_response(render_template("index.html", wordlist=[], currrentLevel=1, playerName=""))
        resp.set_cookie('cookie', newCookie)
        database.addNewUser(newCookie)
        return resp
    else:
        return render_template("index.html", wordlist=user['wordsUsed'], currentLevel=user['levelsUnlocked'],playerName=user['username'])

        
   

        



    


if __name__ == "__main__":
    app.run(debug=True)