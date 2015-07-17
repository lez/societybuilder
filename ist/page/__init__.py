def page_methods(config):
    config.add_route('createpage', '/create')
    config.add_route('showpage', '/show/{id}')
    config.add_route('showallpages', '/all')
    config.add_route('showmypages', '/my')

