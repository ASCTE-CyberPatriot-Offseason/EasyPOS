from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import reqparse

# Initialise the flask class and the API libarary
# Always include the following two lines of code
app = Flask(__name__)
api = Api(app)

rms = {
    'restaurant': {'name': 'KFC', 'Phone Number': '123-456-7890', 'address': 'god help me lane'},
    'menu': {
        'wings': {'price': '10.99', 'quantity_remaining': '10'},
        'fries': {'price': '3.99', 'quantity_remaining': '20'},
        'drink': {'price': '1.99', 'quantity_remaining': '50'}
    }
}


class Restaurant(Resource):
    def get(self):
        return rms['restaurant']


class Menu(Resource):
    @staticmethod
    def get(item):
        try:
            return rms['menu'][item]
        except KeyError:
            return {}

    @staticmethod
    def put(item):
        try:
            rms['menu'][item]
        except KeyError:
            return {f'Error: "{item}" is not on the menu'}

        parser = reqparse.RequestParser()
        parser.add_argument('price')
        parser.add_argument('quantity_remaining')
        result = parser.parse_args()
        print(result)


# Mapping classes to different end points
api.add_resource(Restaurant, '/restaurant')
api.add_resource(Menu, '/menu/<item>')

# Starting the server
if __name__ == '__main__':
    app.run(debug=True)
