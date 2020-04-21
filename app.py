from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient
from umongo import Instance, Document, fields, validate
from models import Item
from bson.objectid import ObjectId

routes = web.RouteTableDef()

def parse_parameter_key_value(rel_url):
    p1 = rel_url.find("parameter%5B")
    if p1 == -1:
        key = None
        value = None
    else:
        p2 = rel_url.find("%5D=", p1+12)
        if p2 == -1 or p1+12 == p2:
            key = None
            value = None
        else:
            key = rel_url[p1+12:p2]
            p3 = rel_url.find("&", p2+4)
            if p3 == -1:
                value = rel_url[p2+4:]
            else:
                value = rel_url[p2+4:p3]
    return (key, value)

@routes.get('/items')
async def get_items(request):
    name = request.rel_url.query.get('name', '')
    key_value_pair = parse_parameter_key_value(str(request.rel_url))

    find_dict = dict()
    
    if name != '':
        find_dict['name'] = name
    if key_value_pair[0] and key_value_pair[1]:
        find_dict['parameters.'+key_value_pair[0]] = key_value_pair[1]

    if not find_dict:
        return web.json_response(status=422)

    result = Item.find(find_dict)

    if not result:
        return web.json_response(status=404)

    little_view = lambda x: {"name": x["name"], "id": x["id"]}
    return web.json_response([little_view(item.dump()) for item in await result.to_list(10)])

@routes.get('/items/{id}')
async def get_items_by_id(request):
    id = request.match_info.get('id', '')

    result = await Item.find_one({"_id": ObjectId(id)})
    if not result:
        return web.json_response(status=404)
    return web.json_response(result.dump())

@routes.post('/items')
async def insert_item(request):
    name = request.match_info.get('name')
    description = request.match_info.get('description')

    data = await request.json()

    try:
        name = data["name"]
        description = data["description"]
        list_params = data["parameters"]
        parameters = dict()
        for param in list_params:
            parameters[param["key"]] = param["value"]
    except:
        return web.json_response(status=422)

    try:
        await Item.ensure_indexes()
        item = Item(name=name, description=description, parameters=parameters)
        await item.commit()
        return web.json_response(item.dump())
    except:
        return web.json_response(status=500)

app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app)