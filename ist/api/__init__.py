# Convention used:
# GET  /api/foo -> all foo objects
# POST /api/foo -> new foo object
# GET  /api/foo/1 -> get one foo object with id 1
# PUT  /api/foo/1 -> modify foo object with id 1
# DELETE /api/foo/1 -> delete foo object with id 1

def api_methods(config):
    config.add_route('user', '/user')
