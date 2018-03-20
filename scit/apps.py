# -*- coding: utf8 -*-
import scit.api as api
import colander
from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden
from bson import ObjectId

_collection='apps'

def check_app_auth(request):
    token=request.headers.get('X-Access-Token')
    if token:
        app=request.db[_collection].find_one({'token':token})
        if app:
            return
    raise HTTPForbidden()


class AppSchema(colander.Schema):
    name = colander.SchemaNode(
            colander.String(),
        )
    token = colander.SchemaNode(
            colander.String(),
        )

class AppsViews(api.BaseViews):

    @api.view(path='apps', method='GET')
    def view_list(self):

        result=list(self.db[_collection].find({}).sort('name'))
        
        return result

    @api.view(path='apps/{_id}', method='GET')
    def view_get(self):
        _id=_id=ObjectId(self.params['_id'])
        item=self.db[_collection].find_one({'_id': _id})
        if item is None:
            raise HTTPNotFound()

        item['_groups']=self.db[_collection].distinct('group')
        return item

    @api.view(path='apps', method='PUT')
    def view_create(self):
        schema=AppSchema()
        data=self.validated_data(schema)
        self.db[_collection].insert(
            data
        )
        return {
            'message': u'Приложение создано'
        }

    @api.view(path='apps/{_id}', method='POST')
    def view_update(self):
        _id=ObjectId(self.params['_id'])
        item=self.db[_collection].find_one({'_id': _id})
        if item is None:
            raise HTTPNotFound()
        schema=AppSchema()
        data=self.validated_data(schema)
        self.db[_collection].update(
            {'_id': _id},
            {'$set': data}
        )
        return {
            'message': u'Приложение изменено'
        }

    @api.view(path='apps/{_id}', method='DELETE')
    def view_delete(self):
        _id=ObjectId(self.params['_id'])
        item=self.db[_collection].find_one({'_id': _id})
        if item is None:
            raise HTTPNotFound()
        self.db[_collection].remove({'_id': _id})
        return {
            'message': u'Приложение удалено'
        }
    