from db import db

from typing import List


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(69), nullable=False, unique=True)

    items = db.relationship('ItemModel', lazy='dynamic')

    @classmethod
    def find_by_id(cls, id: int) -> 'StoreModel':
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_title(cls, title: str) -> 'StoreModel':
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_all(cls) -> List['StoreModel']:
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
