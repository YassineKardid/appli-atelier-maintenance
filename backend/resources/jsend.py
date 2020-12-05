from marshmallow import Schema, fields


class JSendSchema(Schema):
    code = fields.Integer()
    status = fields.String()
    data = fields.Dict()
    message = fields.String()


jsend_schema = JSendSchema()


def wrap(resp):
    # TODO: see how we can avoid deserializing the object here, only to reserialize it with the wrapper
    code = resp.status_code
    status = 'error'
    wrapper = { 'code' : code }
    if code == 200:
        status = 'success'
        data = resp.get_json()
        wrapper['data'] = data
    elif code >= 500:
        status = 'error'
    elif code >= 400:
        status = 'fail'

    wrapper['status'] = status
    resp.set_data(jsend_schema.dumps(wrapper).data)  #.data of MarshalResult
    return resp