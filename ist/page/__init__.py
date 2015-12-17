def page_methods(config):
    config.add_route('createpage', '/create')
    config.add_route('showallpages', '/all')
    config.add_route('showmypages', '/my')
    config.add_route('showpage', '/{id}/show')
    config.add_route('editpage', '/{id}/edit')

