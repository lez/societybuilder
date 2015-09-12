from react.render import render_component
from .util import ROOT
import os

def render(jsx_path, props):
    return render_component(os.path.join(ROOT, 'frontend', 'react_components', jsx_path), props).markup