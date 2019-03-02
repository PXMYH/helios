# from connexion.resolver import RestyResolver
from flask import Flask, render_template
from flask import jsonify
import connexion
from services.bots import Bots
from celery import Celery
import requests
import time
import threading

# Create application instance
# app = connexion.FlaskApp(__name__, specification_dir="swagger/")

# Read the swagger.yml file to configure the endpoints
# app.add_api('api.yaml')


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

celery = make_celery(app)


@app.route("/")
def index():
    return jsonify("Welcome to Helios System")


@celery.task()
@app.before_first_request
@app.route("/v1/start")
def activate_reap():

    def reap():
        """
        start bot crawling sequence
        """

        print ("Initiating Bot Sequence ...")

        test_bot = Bots()
        test_bot.run_craigbot()
        return jsonify(interval="10m", result="SUCCESS")

    thread = threading.Thread(target=reap)
    thread.start()


def start_runner():
    def start_loop():
        not_started = True
        while not_started:
            print('In start loop')
            try:
                r = requests.get('http://localhost:5000/')
                if r.status_code == 200:
                    print('Server started, quiting start_loop')
                    not_started = False
                print(r.status_code)
            except:
                print('Server not yet started')
            time.sleep(2)

    print('Started runner')
    thread = threading.Thread(target=start_loop)
    thread.start()


if __name__ == '__main__':
    # app = connexion.FlaskApp(__name__, specification_dir="swagger/")
    # app.add_api('api.yaml')

    # app.add_api('api.yaml', resolver=RestyResolver('api'))
    # app.add_api('api.yml')
    print('Starting runner')
    start_runner()
    app.run(debug=True)
