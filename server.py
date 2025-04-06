from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contributors")
def contributors():
    return render_template("contributors.html")

@app.route("/director")
def director():
    return render_template("director.html")

@app.route("/home")
def back():
    return render_template("home.html")

@app.route("/pricing")
def pricing():
    return render_template("pricing.html")

@app.route("/service")
def service():
    return render_template("service.html")

@app.route("/whyUs")
def whyUs():
    return render_template("whyUs.html")




if __name__ == "__main__":
    app.run(debug=True)
