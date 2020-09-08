from flask import Flask
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://test:test@db/notable'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# important to create app before import
# https://stackoverflow.com/questions/34281873/how-do-i-split-flask-models-out-of-app-py-without-passing-db-object-all-over
from apis import api
api.init_app(app)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')




