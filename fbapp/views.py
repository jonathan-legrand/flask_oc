from flask import Flask, render_template, url_for, request
from logging import warning

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

from .utils import find_content


@app.route('/')
@app.route('/index/')
def index():
    user_image = url_for("static", filename="img/profile.png")
    description = "Toi, tu sais comment utiliser la console ! \
    Jamais à court d'idées pour réaliser ton objectif, tu es déterminé-e et persévérant-e. \
    Tes amis disent d'ailleurs volontiers que tu as du caractère et que tu ne te laisses pas marcher sur les pieds. \
    Un peu hacker sur les bords, tu aimes trouver des solutions à tout problème. \
    N'aurais-tu pas un petit problème d'autorité ? ;-)"
    return render_template("index.html", user_name="JB", user_image=user_image, description=description,
                           blur=True)


@app.route('/result/')
def result():
    gender = request.args.get("gender")

    try:
        description = find_content(gender).description
    except IndexError:
        warning("Le genre demandé n'est pas dans la base de données")
        description = "Tu es unique"

    print(description)
    user_name = request.args.get("first_name")
    uid = request.args.get("id")
    #user_image = url_for("static", filename="tmp/cover_111823112767411.jpg")
    profile_pic = 'http://graph.facebook.com/' + uid + '/picture?type=large'
    return render_template("result.html",
                           user_name=user_name,
                           gender=gender,
                           description=description,
                           uid=uid,
                           user_image=profile_pic,
                           blur=False)


@app.route('/contents/<int:content_id>/')
def content(content_id):
    return "content_id : " + str(content_id)


if __name__ == "__main__":
    app.run()
