# from connexion.resolver import RestyResolver
from flask import Flask, render_template
from flask import jsonify
import connexion
from services.bots import Bots
from celery import Celery

# Create application instance
# app = connexion.FlaskApp(__name__, specification_dir="swagger/")

# Read the swagger.yml file to configure the endpoints
# app.add_api('api.yaml')

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@app.route("/")
def index():
    return jsonify("Welcome to Helios System")


@celery.task
@app.route("/v1/start")
def reap():
    """ 
    start bot crawling sequence 
    """

    print ("Initiating Bot Sequence ...")

    test_bot = Bots()
    test_bot.run_craigbot()
    return jsonify(interval="10m", result="SUCCESS")


if __name__ == '__main__':
    # app = connexion.FlaskApp(__name__, specification_dir="swagger/")
    # app.add_api('api.yaml')

    # app.add_api('api.yaml', resolver=RestyResolver('api'))
    # app.add_api('api.yml')
    app.run(debug=True)
