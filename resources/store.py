from flask_restful import Resource, reqparse

from flask_jwt_extended import (
    get_jwt_claims, 
    jwt_required, 
    jwt_optional, 
    get_jwt_identity, 
    fresh_jwt_required
)

from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='required field')

    def get(self, id):
        store = StoreModel.find_by_id(id)
        if store:
            return store.json(), 200
        return {'message': 'not found'}, 404

    def put(self, id):
        data = Store.parser.parse_args()
        store = StoreModel.find_by_id(id)
        if store:
            store.name = data['name']
            updated_store = store.save_to_db()
            return updated_store, 200
        return StoreModel(**data).save_to_db(), 201
    
    @jwt_required
    def delete(self, id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin required'}, 401
        store = StoreModel.find_by_id(id)
        if store:
            store.delete_from_db()
            return {'message': 'deleted'}, 204
        return {'message': 'not found'}, 404


class StoreList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='required field')

    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        if user_id:
            return [store.json() for store in StoreModel.find_all()], 200
        return {
            'items': [store.name for store in StoreModel.find_all()],
            'message': "More data can be show if login"
        }, 200

    @fresh_jwt_required
    def post(self):
        data = Store.parser.parse_args()
        if StoreModel.find_by_name(data['name']):
            return {'message': 'already exists'}, 400

        return StoreModel(**data).save_to_db(), 201
