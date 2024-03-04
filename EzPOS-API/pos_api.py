from flask import Flask
from flask_restful import Resource, Api
import sqlite3


# Initialise the flask class and the API libarary
# Always include the following two lines of code


rms = {
    "restaurant": {
        "name": "Restaurant Name",
        "Phone Number": "123-456-7890",
        "address": "1 Example Street",
    },
    "menu": {},
}
menu_item_payload = {
    "name": "New Item",
    "uid": 123456,
    "description": "Sample description",
    "category_id": 1,
    "price": 9.99,
    "image_url": "https://example.com/image.jpg",
    "active": 1,
}


class Restaurant(Resource):
    """
    Retrieve restaurant information.
    """

    def get(self):
        """
        Retrieve the restaurant information.
        """
        return rms["restaurant"]


class Menu(Resource):
    """
    Retrieve menu item information.
    """

    def sync(self):
        """
        Retrieve the entire menu.

        Returns:
        - dict: The menu items.
        """
        try:
            return rms["menu"]
        except KeyError:
            return {}

    def synci(self, item):
        """
        Synchronize the item with the menu.

        Args:
            item (str): The item to synchronize.

        Returns:
            dict: A dictionary containing an error message if the item is not on the menu.
        """
        try:
            return rms["menu"][item]
        except KeyError:
            return {f"Error{item} is not on the menu"}


api.add_resource(Restaurant, "/restaurant")
api.add_resource(Menu, "/menu/<item>")


def insert_order(status):
    valid_statuses = ["pending", "processing", "completed", "cancelled"]
    if status not in valid_statuses:
        raise ValueError(f"Invalid status '{status}'. Must be one of {valid_statuses}.")

    db = get_db()
    db.execute("INSERT INTO orders (status) VALUES (?)", (status,))
    db.commit()
