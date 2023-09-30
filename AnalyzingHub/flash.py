from flask import Flask, render_template
import sqlite3
app = Flask(__name__)
sqldbname = "./db/website.db"

@app.route('/')
def index():
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()

    cursor.execute("Select * from storages")
    data = cursor.fetchall()
    conn.close()

    return render_template("index.html", table=data)


if __name__ == '__main__':
    app.run(debug=True)