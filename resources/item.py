from flask_restful import Resource

from flask import request

from flask_jwt_extended import jwt_required

from marshmallow import ValidationError

from schemas.item import ItemSchema

from models.item import ItemModel


item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):
    def get(self, id: int):
        item = ItemModel.find_by_id(id)
        if item:
            return item_schema.dump(item), 200
        return {'message': 'not found'}, 404

    @jwt_required
    def put(self, id: int):
        new_item = item_schema.load(request.get_json())
        item = ItemModel.find_by_id(id)
        if not item:
            return item_schema.dump(new_item.save_to_db()), 201
        item.title = new_item.title
        item.price = new_item.price
        return item_schema.dump(item.save_to_db()), 200

    @jwt_required
    def delete(self, id: int):
        item = ItemModel.find_by_id(id)
        if not item:
            return {'message': 'not found'}, 404
        item.delete_from_db()
        return {'message': 'deleted'}, 204


class ItemList(Resource):
    def get(self):
        return {'items': item_list_schema.dump(ItemModel.find_all())}, 200

    @jwt_required
    def post(self):
        new_item = item_schema.load(request.get_json())
        item = ItemModel.find_by_title(new_item.title)
        if not item:
            return item_schema.dump(new_item.save_to_db()), 201
        return {'message': 'already exists'}, 400
