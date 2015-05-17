from pyramid.view import view_config


@view_config(route_name='api', renderer='json', request_method='POST')
def content_view(request):
    return {'success': 1}