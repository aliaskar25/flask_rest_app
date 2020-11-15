from typing import Dict, List, Union

from db import db


ItemJSON = Dict[str, Union[int, str, float, int]]


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(69), unique=True)
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name: str, price: float, store_id: int):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self) -> ItemJSON:
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'store_id': self.store_id
        }

    @classmethod
    def find_by_id(cls, id: int) -> 'ItemModel':
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls) -> List['ItemModel']:
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name: str) -> 'ItemModel':
        return cls.query.filter_by(name=name).first()

    def save_to_db(self) -> ItemJSON:
        db.session.add(self)
        db.session.flush()
        db.session.refresh(self)
        db.session.commit()
        return self.json()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()