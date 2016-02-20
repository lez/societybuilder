from react.render import render_component
from react.conf import settings
from ist import ROOT
import os
from json import JSONDecoder
from ist.model.base import ModelEncoder

# TODO: control from .ini files
settings.configure(RENDER=False) # in production: True

def render(jsx_path, props):
    # dirty hack so that JSONEncoder can encode props
    props = JSONDecoder().decode(ModelEncoder().encode(props))

    return render_component(os.path.join(ROOT, 'frontend', 'react_components', jsx_path), props).markup