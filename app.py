from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

db = mysql.connector.connect(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=os.getenv("MYSQLPORT")
)

@app.route("/")
def home():
    return "Portfolio Running"

@app.route("/contact", methods=["POST"])
def contact():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    cursor = db.cursor()
    sql = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, email, message))
    db.commit()

    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)