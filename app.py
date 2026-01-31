from flask import Flask, render_template, g, request,redirect
import sqlite3
from flask_session import Session

app = Flask(__name__)
app.secret_key = "replace-with-a-secret"
app.config['SESSION_TYPE'] = 'filesystem'
app.config["SESSION_PERMANENT"] = False
Session(app)

DATABASE = 'database.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()



@app.route("/", methods=["GET", "POST"])
def index():
    db = get_db()
    tasks = db.execute("SELECT * FROM task").fetchall()
    if request.method == "POST":
        changestatus = request.form.get("cstatus")

    return render_template("index.html", tasks=tasks)   



@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        db = get_db()
        taskname = request.form.get("taskname")
        desc = request.form.get("desc")
        status = request.form.get("status")
        db.execute("INSERT INTO task (taskname,description,status) VALUES (?,?,?)",(taskname,desc,status))
        db.commit()
        return redirect("/")





@app.route("/change", methods=["POST"])
def change():
    db = get_db()
    taskid = request.form.get("taskid")
    new_status = request.form.get("cstatus")
    if not taskid or not new_status:
        return redirect("/")
    db.execute("UPDATE task SET status = ? WHERE id = ?", (new_status, taskid))
    db.commit()
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    db = get_db()
    taskid = request.form.get("taskidd")
    if not taskid:
        return redirect("/")
        
    db.execute("DELETE FROM task WHERE id = ?",(taskid,))
    db.commit()
    return redirect("/")

@app.route('/edit', methods=['POST'])
def edit():
    db = get_db()
    taskid = request.form.get('taskid')
    name = request.form.get('taskname')
    desc = request.form.get('desc')
    status = request.form.get('status')
    db.execute('UPDATE task SET taskname=?, description=?, status=? WHERE id=?',
               (name, desc, status, taskid))
    db.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
