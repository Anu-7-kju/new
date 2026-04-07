from flask import Flask, render_template, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

db = mysql.connector.connect(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=int(os.getenv("MYSQLPORT", 3306))
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
    print("🔥 ROUTE HIT")   # MUST PRINT

    try:
        data = request.get_json()
        print("DATA:", data)

        cursor.execute(
            "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
            (data["name"], data["email"], data["message"])
        )
        db.commit()

        print("✅ INSERTED")

        return jsonify({"message": "Saved successfully!"})

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"message": "Error"})
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)