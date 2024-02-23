from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import reqparse

#Initialise the flask class and the API libarary 
#Always include the following two lines of code
app = Flask(__name__)
api = Api(app)

rms ={
    'restaurant' : {'name' : 'KFC', 'Phone Number' : '123-456-7890','address' : 'god help me lane' },
    'menu' : {
        'wings' : {'price' : 10.99, 'quantity' : 10},
    }
}