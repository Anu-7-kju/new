from flask import Flask, render_template, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

db = mysql.connector.connect(
    host="centerbeam.proxy.rlwy.net",
    user="root",
    password="XqvARwoftsLzVQmSMXdZZmNviVnYOoCK",
    database="railway",
    port=18096
)

cursor = db.cursor()

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
    try:
        data = request.json

        print("Received:", data)  # 👈 DEBUG

        query = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
        cursor.execute(query, (data["name"], data["email"], data["message"]))

        db.commit()  # 👈 MUST

        print("Inserted successfully")  # 👈 DEBUG

        return jsonify({"message": "Saved successfully!"})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"message": "Error occurred"})
@app.route("/test")
def test():
    cursor.execute("INSERT INTO contacts (name,email,message) VALUES ('test','test','hello')")
    db.commit()
    return "Inserted"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)