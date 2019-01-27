# from connexion.resolver import RestyResolver
from flask import Flask, render_template
import connexion

# Create application instance
app = connexion.FlaskApp(__name__, specification_dir="swagger/")

# # Read the swagger.yml file to configure the endpoints
app.add_api('api.yaml')

@app.route("/")
def home():
    return render_template("home.html")

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    # app = connexion.FlaskApp(__name__, specification_dir="swagger/")
    # app.add_api('api.yaml')

    # app.add_api('api.yaml', resolver=RestyResolver('api'))
    # app.add_api('api.yml')
    app.run(debug=True)
