from connexion.resolver import RestyResolver
import connexion

if __name__ == '__main__':
    app = connexion.FlaskApp(__name__, specification_dir='swagger/')
    app.add_api('api.yaml', resolver=RestyResolver('api'))
    app.run(port=9999)

# @app.route("/")
# def hello():
#     return "Hello World!"
