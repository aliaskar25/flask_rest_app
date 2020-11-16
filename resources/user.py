from flask_restful import Resource
from flask import request
from flask_jwt_extended import (
    jwt_required, 
    create_access_token,
    create_refresh_token, 
    jwt_refresh_token_required,
    get_jwt_identity, 
    get_raw_jwt, 
)

from marshmallow import ValidationError

from werkzeug.security import safe_str_cmp

from models.user import UserModel

from schemas.user import UserSchema

from blacklist import BLACKLIST


user_schema = UserSchema()


class UserRegister(Resource):
    def post(self):
        user_data = user_schema.load(request.get_json())
        user = UserModel.find_by_username(user_data.username)
        if not user:
            user = user_data.save_to_db()
            return user_schema.dump(user), 201
        return {'message': 'already exists'}, 400


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}, 204


class UserLogin(Resource):
    def post(self):
        user_data = user_schema.load(request.get_json())
        user = UserModel.find_by_username(user_data.username)
        if user and safe_str_cmp(user.password, user_data.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Invalid credentials'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'logged out'}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=True)
        return {'access_token': new_token}, 200