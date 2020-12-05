from flask import Flask, render_template, request
from score_manager import ScoreManager
from score import Score

app = Flask(__name__)
score_manager = ScoreManager()

@app.route('/')
def homepage():
    """ Renders homepage listing all scores. """
    return render_template("score_view.html", scores=score_manager.scores)

@app.route('/api/list', methods=["GET"])
def list_all_scores():
    """ Renders web page listing all scores """
    return {"scores": score_manager.scores}

@app.route('/api/list', methods=["DELETE"])
def remove_user_scores():
    data = request.get_json()

    if data and "name" in data:
        name_existed = score_manager.remove_user_score(data["name"])
    else:
        name_existed = False

    return ("", 204) if name_existed else ("Invalid data received", 400)

@app.route("/api/new", methods=["PUT"])
def add_new_score():
    data = request.get_json()

    try:
        score = Score(data["name"], data["score"])
    except:
        return "Invalid data provided.", 400

    score_manager.add_score(score)
    return ("", 204)

if __name__ == "__main__":
    app.run(debug=True)