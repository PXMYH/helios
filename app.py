# from connexion.resolver import RestyResolver
from flask import Flask, render_template
from flask import jsonify
import connexion
from services.bots import Bots
from celery import Celery
import requests
import time
import threading
import os

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
# TODO: add configuration management
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
# app.config.from_object('yourapplication.default_settings')
# app.config.from_envvar('YOURAPPLICATION_SETTINGS')
# app.config.from_object('configmodule.DevelopmentConfig')
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


def start_runner(running_port):
    def start_loop(running_port):
        not_started = True
        while not_started:
            print('In start loop')
            try:
                print ("checking app running at port {}".format(running_port))
                running_url = "http://0.0.0.0:" + str(running_port) + "/"
                print ("request sent to {}".format(str(running_url)))
                r = requests.get(str(running_url))
                print("status code is {}".format(str(r.status_code)))
                if r.status_code == 200:
                    print('Server started, quiting start_loop')
                    not_started = False
            except Exception as e:
                print ("Server not yet started, exception: {}".format(str(e)))
            time.sleep(2)

    print('Started runner')
    # need ',' at the end of args to pass as tuple
    thread = threading.Thread(target=start_loop, args=(running_port,))
    thread.start()


if __name__ == '__main__':
    # app = connexion.FlaskApp(__name__, specification_dir="swagger/")
    # app.add_api('api.yaml')

    # app.add_api('api.yaml', resolver=RestyResolver('api'))
    # app.add_api('api.yml')
    print('Starting runner')
    port = int(os.environ.get('PORT', 5000))
    start_runner(port)
    app.run(host='0.0.0.0', port=port, debug=False)
