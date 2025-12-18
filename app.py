from flask import Flask, render_template, request, redirect
import mysql.connector
import os
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
envuser = os.getenv("user")
envpassword = os.getenv("password")
envhost = os.getenv("host")


app = Flask(__name__)

db = mysql.connector.connect(
    host=envhost,
    user=envuser,
    password=envpassword,
    database="webnovels"
)


@app.route('/')
def index():
    return redirect('/novels')

@app.route("/novels")
def novels():
    cursor = db.cursor()
    cursor.execute("SELECT id, title, description FROM novels")
    novels = cursor.fetchall()
    return render_template("novels.html", novels=novels)

@app.route("/novel/new", methods=["GET", "POST"])
def new_novel():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO novels (title, description) VALUES (%s, %s)",
            (title, description)
        )
        db.commit()
        return redirect("/novels")
    return render_template("new_novel.html")

@app.route("/novel/<id>")
def novel(id):
    cursor = db.cursor()

    
    cursor.execute("SELECT title, description FROM novels WHERE id = %s", (id,))
    novel = cursor.fetchone()

    
    cursor.execute("SELECT id, chapter_no, title FROM chapters WHERE novel_id = %s ORDER BY chapter_no", (id,))
    chapters = cursor.fetchall()

    return render_template("novel.html", novel=novel, chapters=chapters, novel_id=id)


@app.route("/novel/<novel_id>/delete")
def delete_novel(novel_id):
    cursor = db.cursor()


    cursor.execute("DELETE FROM novels WHERE id = %s", (novel_id,))
    db.commit()

    return redirect("/novels")


# ---------- CHAPTERERS ----------

@app.route("/novel/<novel_id>/chapter/new", methods=["GET", "POST"])
def new_chapter(novel_id):
    if request.method == "POST":
        title = request.form["title"]
        chapter_no = request.form["chapter_no"]
        content = request.form["content"]

        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO chapters (novel_id, title, chapter_no, content) VALUES (%s, %s, %s, %s)",
            (novel_id, title, chapter_no, content)
        )
        db.commit()

        return redirect(f"/novel/{novel_id}")

    return render_template("new_chapter.html", novel_id=novel_id)



@app.route("/chapter/<chapter_id>")
def chapter(chapter_id):
    cursor = db.cursor()
    cursor.execute(
        "SELECT novel_id, chapter_no, title, content FROM chapters WHERE id = %s",
        (chapter_id,)
    )
    chapter = cursor.fetchone()

    return render_template("chapter.html", chapter=chapter)


@app.route("/chapter/<chapter_id>/delete")
def delete_chapter(chapter_id):
    cursor = db.cursor()


    cursor.execute("SELECT novel_id FROM chapters WHERE id = %s", (chapter_id,))
    novel_id = cursor.fetchone()[0]


    cursor.execute("DELETE FROM chapters WHERE id = %s", (chapter_id,))
    db.commit()

    return redirect(f"/novel/{novel_id}")






