from db import db

from typing import List


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(69), nullable=False, unique=True)
    price = db.Column(db.Float(precision=2), nullable=False)

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    store = db.relationship('StoreModel')

    @classmethod
    def find_by_id(cls, id: int) -> 'ItemModel':
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_title(cls, title: str) -> 'ItemModel':
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_all(cls) -> List['ItemModel']:
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.flush()
        db.session.refresh(self)
        db.session.commit()
        return self

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()