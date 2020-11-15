import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from resources.user import (
    UserRegister, User, 
    UserLogin, TokenRefresh, 
    UserLogout, 
)
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from blacklist import BLACKLIST


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', default='sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'aliaskar'
api = Api(app)


jwt = JWTManager(app)

# @jwt.user_claims_loader # claims some info to check in resources

@jwt.token_in_blacklist_loader
def check_token_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

# @jwt.expired_token_loader
# @jwt.invalid_token_loader
# @jwt.unauthorized_loader
# @jwt.needs_fresh_token_loader
# @jwt.revoked_token_loader # Black list for tokens


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Item, '/items/<int:id>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/stores/<int:id>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')


if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
