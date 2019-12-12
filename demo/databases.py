#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 10/16/19 7:35 PM
# @Author  : dengsc


import datetime
from sqlalchemy.orm import relationship

from .extensions import db

# Alias common SQLAlchemy names
relationship = relationship

basestring = (str, bytes)


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete)
    operations.
    """

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        # Prevent changing ID of object
        kwargs.pop('id', None)
        for attr, value in kwargs.items():
            # Flask-RESTful makes everything None by default :/
            if value is not None:
                setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        try:
            db.session.add(self)
            if commit:
                db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self, commit=True):
        """Remove the record from the database."""
        try:
            db.session.delete(self)
            return commit and db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""
    __abstract__ = True

    def to_json(self):
        result = dict()
        for key in self.__mapper__.c.keys():
            col = getattr(self, key)
            if isinstance(col, datetime.datetime) or isinstance(col, datetime.date):
                col = col.isoformat()
            result[key] = col
        return result


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named
    ``id`` to any declarative-mapped class.
    """
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, _id):
        if _id <= 0:
            raise ValueError('ID must not be negative or zero!')
        if any(
            (isinstance(_id, basestring) and _id.isdigit(),
             isinstance(_id, (int, float))),
        ):
            return cls.query.get(int(_id))
        return None


def reference_col(table_name, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.
    Usage: ::
        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey('{0}.{1}'.format(table_name, pk_name)),
        nullable=nullable, **kwargs)  # pragma: no cover
