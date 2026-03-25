from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# 🔴 Paste your Railway MySQL credentials here
db = mysql.connector.connect(
    host="YOUR_HOST",
    user="YOUR_USER",
    password="YOUR_PASSWORD",
    database="YOUR_DATABASE",
    port=3306   # or your Railway port (sometimes different)
)

cursor = db.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    message TEXT
)
""")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    query = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, email, message))
    db.commit()

    return jsonify({"message": "Saved successfully!"})

if __name__ == "__main__":
    app.run(debug=True)