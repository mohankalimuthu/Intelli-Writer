from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)


from flask_cors import CORS
CORS(app)

EXCEL_FILE = "C:\\Users\\hp\\Downloads\\project (1)\\project\\register_data.xlsx"

@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        print("Received Data:", data)  

        if not data:
            return jsonify({"message": "No data received!"}), 400

        useremail = data.get("useremail")
        username = data.get("username")
        password = data.get("password")

        if os.path.exists(EXCEL_FILE):
            df = pd.read_excel(EXCEL_FILE)
        else:
            df = pd.DataFrame(columns=["Email", "Username", "Password"])

        new_data = pd.DataFrame([[useremail, username, password]], columns=["Email", "Username", "Password"])
        df = pd.concat([df, new_data], ignore_index=True)

        
        df.to_excel(EXCEL_FILE, index=False)
        print("Data stored successfully!")  

        return jsonify({"message": "Registration successful!"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    
    

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    try:
        df = pd.read_excel(EXCEL_FILE)

       
        user = df[(df["Username"] == username) & (df["Password"] == password)]

        if not user.empty:
            return jsonify({"message": "Login successful!", "redirect": "/indexX.html"}), 200
        else:
            return jsonify({"message": "Invalid username or password!"}), 401

    except FileNotFoundError:
        return jsonify({"message": "No registered users found!"}), 400
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(debug=True)
