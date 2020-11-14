from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='required field')
    parser.add_argument('price', type=float, required=True, help='required field')
    parser.add_argument('store_id', type=int, required=True, help='required field')

    # @jwt_required
    def get(self, id):
        item = ItemModel.find_by_id(id)
        if item:
            return {'id': item.id, 'name': item.name, 'price': item.price}
        return {'message': 'not found'}, 404

    # @jwt_required
    def put(self, id):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_id(id)
        if item:
            item.name = data['name']
            item.price = data['price']
            item.store_id = data['store_id']
            try:
                updated_item = item.save_to_db()
            except:
                return {'message smth went wrong'}, 500
            return updated_item, 200
            
        item = ItemModel(**data)
        try:
            item = item.save_to_db()
        except:
            return {'smth went wrong'}, 500
        return item, 201
            
    # @jwt_required
    def delete(self, id):
        item = ItemModel.find_by_id(id)
        if item:
            item.delete_from_db()
            return {'message': 'deleted'}, 204
        return {'message': 'not found'}, 404


class ItemList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='required field')
    parser.add_argument('price', type=float, required=True, help='required field')
    parser.add_argument('store_id', type=int, required=True, help='required field')

    def get(self):
        return [item.json() for item in ItemModel.find_all()], 200

    def post(self):
        data = ItemList.parser.parse_args()
        if ItemModel.find_by_name(data['name']):
            return {'message': 'already exists'}, 400

        item = ItemModel(**data)
        try:
            item = item.save_to_db()
        except:
            return {'message': 'smth went wrong'}, 500

        return item, 201
