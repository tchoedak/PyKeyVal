from types import new_class
from sqlalchemy import Table, MetaData, String, Column
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func, create_engine


def generate_keyval_model(table, tablename):
    class KeyVal(object):
        def __init__(self, key, val):
            __tablename__ = tablename
            self.key = key
            self.val = val

    mapper(KeyVal, table)
    return KeyVal


class SQLiteKeyVal(object):
    def __init__(self, url='', name=None, **options):
        self._engine = create_engine(url)
        self._connection = None
        self._session = None
        metadata = MetaData(self._engine)
        namespace = options.get('namespace')
        self.tablename = '_'.join(filter(None, [name, namespace]))
        self.table = Table(
            self.tablename,
            metadata,
            Column('key', String, primary_key=True),
            Column('val', String),
        )
        self.table.create(checkfirst=True)
        self.KeyVal = generate_keyval_model(self.table, self.tablename)

    @property
    def session(self):
        if self._session:
            return self._session
        else:
            Session = sessionmaker()
            Session.configure(bind=self._engine)
            self._session = Session()
            return self._session

    @property
    def connection(self):
        if self._connection:
            return self._connection
        else:
            self._connection = self._engine.connect()
            return self._connection

    def set(self, key, val):
        item = self._get(key)
        item_result = item.first()
        if item_result:
            item_result.val = val
            self.session.commit()
        else:
            item = self.KeyVal(key=key, val=val)
            self.session.add(item)
            self.session.commit()

    def _get(self, key):
        val = self.session.query(self.KeyVal).filter(self.KeyVal.key == key)
        return val

    def get(self, key):
        row = self._get(key).first()
        if row:
            return self._get(key).first().val
        else:
            return row

    def delete(self, key):
        val = self._get(key)
        key_exists = val.first() is not None
        if key_exists:
            val.delete()
            self.session.commit()
        return key_exists

    def clear(self):
        self.session.query(self.KeyVal).delete()
        self.session.commit()
        return True
