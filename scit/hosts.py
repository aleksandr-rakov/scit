# -*- coding: utf8 -*-
import scit.api as api
import colander
from pyramid.httpexceptions import HTTPNotFound
from bson import ObjectId

_collection='hosts'


@colander.deferred
def login_validator(node,kw):
    db=kw['db']
    userid=kw['userid']
    def validator(form, value):
        colander.Length(max=50)(form, value)
        """Проверяем не занят ли логин"""
        if db[_collection].find_one({'login':value,'_id':{'$ne':userid}}):
            raise colander.Invalid(
                    form, 
                    u'Этот логин уже зарегистрирован'
                )
    return validator

class HostSchema(colander.Schema):
    name = colander.SchemaNode(
            colander.String(),
        )
    login = colander.SchemaNode(
            colander.String(),
            validator=login_validator,
        )
    disabled = colander.SchemaNode(
            colander.Bool(),
        )

class HostsViews(api.BaseViews):

    @api.view(path='hosts', method='GET')
    def view_list(self):

        result=list(self.db[_collection].find({}).sort('name'))
        
        return result

    @api.view(path='hosts/{_id}', method='GET')
    def view_get(self):
        _id=_id=ObjectId(self.params['_id'])
        item=self.db[_collection].find_one({'_id': _id})
        if item is None:
            raise HTTPNotFound()
        return item

    @api.view(path='hosts', method='PUT')
    def view_create(self):
        schema=HostSchema().bind(
                db=self.db,
                userid=None
            )
        data=self.validated_data(schema)
        self.db[_collection].insert(
            data
        )
        return {
            'message': u'Хост создан'
        }

    @api.view(path='hosts/{_id}', method='POST')
    def view_update(self):
        _id=ObjectId(self.params['_id'])
        item=self.db[_collection].find_one({'_id': _id})
        if item is None:
            raise HTTPNotFound()
        schema=HostSchema().bind(
                db=self.db,
                userid=_id
            )
        data=self.validated_data(schema)
        self.db[_collection].update(
            {'_id': _id},
            {'$set': data}
        )
        return {
            'message': u'Хост изменен'
        }

    @api.view(path='hosts/{_id}', method='DELETE')
    def view_delete(self):
        _id=ObjectId(self.params['_id'])
        item=self.db[_collection].find_one({'_id': _id})
        if item is None:
            raise HTTPNotFound()
        self.db[_collection].remove({'_id': _id})
        return {
            'message': u'Хост удален'
        }
