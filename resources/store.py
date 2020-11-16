from flask_restful import Resource

from flask import request

from flask_jwt_extended import jwt_required

from marshmallow import ValidationError

from schemas.store import StoreSchema

from models.store import StoreModel


store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)


class Store(Resource):
    def get(self, id: int):
        store = StoreModel.find_by_id(id)
        if not store:
            return {'message': 'not found'}, 404
        return store_schema.dump(store), 200

    @jwt_required
    def put(self, id: int):
        new_store = store_schema.load(request.get_json())
        store = StoreModel.find_by_id(id)
        if not store:
            return store_schema.dump(new_store.save_to_db()), 201
        store.title = new_store.title
        return store_schema.dump(store.save_to_db()), 200

    @jwt_required
    def delete(self, id: int):
        store = StoreModel.find_by_id(id)
        if not store:
            return {'message': 'not found'}, 404
        store.delete_from_db()
        return {'message': 'deleted'}, 204
    

class StoreList(Resource):
    def get(self):
        return {'stores': store_list_schema.dump(StoreModel.find_all())}, 200

    @jwt_required
    def post(self):
        new_store = store_schema.load(request.get_json())
        store = StoreModel.find_by_title(new_store.title)
        if not store:
            return store_schema.dump(new_store.save_to_db()), 201
        return {'message': 'already exists'}, 400