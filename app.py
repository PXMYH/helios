# from connexion.resolver import RestyResolver
from flask import Flask, render_template
import connexion
from services.bots import Bots

# Create application instance
# app = connexion.FlaskApp(__name__, specification_dir="swagger/")

# # Read the swagger.yml file to configure the endpoints
# app.add_api('api.yaml')

app = Flask(__name__)
app.run(debug=True)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/crawl")
def reap():
    """ 
    start bot crawling sequence 
    """

    print ("Initiating Bot Sequence ...")

    test_bot = Bots()
    test_bot.run_craigbot()

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000, debug=True)


# if __name__ == '__main__':
    # app = connexion.FlaskApp(__name__, specification_dir="swagger/")
    # app.add_api('api.yaml')

    # app.add_api('api.yaml', resolver=RestyResolver('api'))
    # app.add_api('api.yml')
    # app = Flask(__name__)
    # app.run(debug=True)
