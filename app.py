import connexion
from connexion.resolver import RestyResolver
from services.provider import ItemsProvider

if __name__ == '__main__':
    app = connexion.FlaskApp(__name__, specification_dir='swagger/')
    app.add_api('api.yaml', resolver=RestyResolver('api'))
    FlaskInjector(app=app, modules=[configure])
    app.run(port=9999)
