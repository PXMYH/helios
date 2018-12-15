# import connexion
# from connexion.resolver import RestyResolver

# if __name__ == '__main__':
#     app = connexion.FlaskApp(__name__, specification_dir='swagger/')
#     app.add_api('api.yaml', resolver=RestyResolver('api'))
#     app.run(port=9999)

from flask import Flask, render_template

app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
