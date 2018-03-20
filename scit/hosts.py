# -*- coding: utf8 -*-
import scit.api as api
import colander
from pyramid.httpexceptions import HTTPNotFound
from bson import ObjectId
from collections import OrderedDict
import ipaddr
import re
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.response import Response
from scit.apps import check_app_auth

_collection='hosts'


@colander.deferred
def ip_validator(node,kw):
    db=kw['db']
    host_id=kw['host_id']
    def validator(form, value):
        iplist_validator(form, value)
        ips=split_list(value)
        for ip in ips:
            if db[_collection].find_one({'ip':ip,'_id':{'$ne':host_id}}):
                raise colander.Invalid(
                        form, 
                        u'Такой IP уже есть'
                    )
    return validator

def one_ip_validator(node,value):
    try:
        ipaddr.IPNetwork(value)
    except:
        raise colander.Invalid(
                node,
                u'Неверный формат "%s"'%value
            )

def split_list(text):
    return re.split('[\s,;,\,]+', text)

def iplist_validator(node,value):
    ips=split_list(value)
    for ip in ips:
        one_ip_validator(node,ip)

def portlist_validator(node,value):
    ports=split_list(value)
    for port in ports:
        try:
            if int(port)<=0:
                raise
        except:
            raise colander.Invalid(
                node,
                u'Неверный формат порта'
            )

class HostSchema(colander.Schema):
    name = colander.SchemaNode(
            colander.String(),
        )
    ip = colander.SchemaNode(
            colander.String(),
            validator=ip_validator,
        )
    open_ports = colander.SchemaNode(
            colander.String(),
            missing='',
            validator=portlist_validator
        )
    group = colander.SchemaNode(
            colander.String(),
            missing=''
        )
    comment = colander.SchemaNode(
            colander.String(),
            missing=None
        )

class HostsViews(api.BaseViews):

    @api.view(path='hosts', method='GET')
    def view_list(self):

        result=list(self.db[_collection].find({}).sort('name'))
        
        return result

    @api.view(path='hosts/by_group', method='GET')
    def view_list_by_group(self):

        result=list(self.db[_collection].find({}).sort([('group',1),('name',1)]))

        groupped=OrderedDict()
        for x in result:
            group=x.get('group','')
            if not group in groupped:
                groupped[group]={
                    'name': group,
                    'hosts': []
                }
            groupped[group]['hosts'].append(x)
        
        return groupped.values()

    @api.view(path='hosts/_groups', method='GET')
    def view_get_groups(self):
        return self.db[_collection].distinct('group')

    @api.view(path='hosts/{_id}', method='GET')
    def view_get(self):
        _id=_id=ObjectId(self.params['_id'])
        item=self.db[_collection].find_one({'_id': _id})
        if item is None:
            raise HTTPNotFound()

        item['_groups']=self.db[_collection].distinct('group')
        return item

    @api.view(path='hosts', method='PUT')
    def view_create(self):
        schema=HostSchema().bind(
                db=self.db,
                host_id=None
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
                host_id=_id
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


    @api.view(path='app/hosts', method='GET', permission=NO_PERMISSION_REQUIRED)
    def view_app_api(self):

        check_app_auth(self.request)

        q={}
        group=self.modifers.get('group')
        if group:
            q['group']=group
        
        hosts=list(self.db[_collection].find(q).sort([('group',1),('name',1)]))
        result=''
        group_added=False
        last_group=None
        for host in hosts:
            for ip in split_list(host['ip']):
                if not group_added or last_group!=host['group']:
                    if group_added:
                        result+='\n'
                    result+=u"#GROUP: %s\n"%(host['group'] or 'NO_GROUP')
                    last_group=host['group']
                    group_added=True

                result+=u"#%s\n%s\n"%(host['name'],ip)

        return Response(result,content_type='text',charset='utf8')
