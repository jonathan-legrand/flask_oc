from flask import Flask, render_template, url_for, request
from logging import warning

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

from .utils import find_content, OpenGraphImage


@app.route('/')
@app.route('/index/')
def index():
    description = "Toi, tu sais comment utiliser la console ! \
    Jamais à court d'idées pour réaliser ton objectif, tu es déterminé-e et persévérant-e. \
    Tes amis disent d'ailleurs volontiers que tu as du caractère et que tu ne te laisses pas marcher sur les pieds. \
    Un peu hacker sur les bords, tu aimes trouver des solutions à tout problème. \
    N'aurais-tu pas un petit problème d'autorité ? ;-)"
    page_title = request.args.get("page")
    img = request.args.get("img")
    if img is None:
        warning("No image has been specified")
        img = "tmp/cover_111823112767411.jpg"
    og_url = url_for("static", filename=img, _external=True)
    return render_template("index.html",
                           user_name="JB",
                           user_image=url_for('static', filename='img/profile.png'),
                           description=description,
                           blur=True,
                           page_title=page_title,
                           og_url=og_url,
                           og_img=img
                           )


@app.route('/result/')
def result():
    gender = request.args.get("gender")

    try:
        description = find_content(gender).description
    except IndexError:
        warning("Gender {} is not present in the database".format(gender))
        description = "Tu es unique"

    # print(description)
    user_name = request.args.get("first_name")
    uid = request.args.get("id")
    og_img = OpenGraphImage(uid, user_name, description).location
    og_url = url_for("static", filename=og_img, _external=True)
    profile_pic = 'http://graph.facebook.com/' + uid + '/picture?type=large'
    return render_template("result.html",
                           user_name=user_name,
                           gender=gender,
                           description=description,
                           uid=uid,
                           user_image=profile_pic,
                           og_url=og_url,
                           blur=False)


@app.route('/contents/<int:content_id>/')
def content(content_id):
    return "content_id : " + str(content_id)


if __name__ == "__main__":
    app.run()
