from react.render import render_component
from react.conf import settings
from ist import ROOT
import os
from json import JSONDecoder
from ist.model.base import ApiEncoder

# Server side react rendering

def includeme(config):

    app_settings = config.get_settings()

    print('RENDER', app_settings['react.render'])
    if app_settings['react.render']:
        settings.configure(RENDER=True, RENDER_URL=app_settings['react.render_url'])
    else:
        settings.configure(RENDER=False)


def render(jsx_path, props):
    # dirty and expensive hack so that JSONEncoder can encode props
    props = JSONDecoder().decode(ApiEncoder().encode(props))

    return render_component(os.path.join(ROOT, 'frontend', 'react_components', jsx_path), props).markup