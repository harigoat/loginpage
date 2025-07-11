from flask import Flask, redirect, render_template,request,url_for
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user_found = False
    user_correct = False
    
    try:
        with open("users.txt",'r') as f:
            lines=f.readlines()
            for line in lines:
                stored_user , stored_pass = line.strip().split(":")
                if stored_user == username:
                    user_found = True
                    if stored_pass == password:
                        user_correct = True
                        break
    except FileNotFoundError:
        open("users.txt",'w').close()
    if user_found and user_correct:
        return f"<h1> HI! {username}</h1>"
    elif user_found and not user_correct:
        return "<h3 style='color:red;'>Incorrect password. Try again.</h3>"
    else:
        return redirect(url_for("register", new_user=username))
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        with open("users.txt", "a") as f:
            f.write(f"{username}:{password}\n")
        return redirect(url_for("home"))
    new_user = request.args.get("new_user", "")
    return render_template("register.html", new_user=new_user)

@app.route("/forgot")
def forgot_password():
    return "<h3>Password recovery is not implemented yet.</h3>"

@app.route("/defaultpage")
def defaultpage():
    return render_template("defaultpage.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)


    
