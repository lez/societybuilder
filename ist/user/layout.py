#coding: pyxl
from pyxl.html import *
from pyramid.view import view_config
from pyramid.exceptions import HTTPNotFound
from ist.view.element import *
from ist.model.type import User

@view_config(route_name='user_profile', renderer='layout', permission='user')
def show_profile(request):
    try:
        user = User.select().where(User.login == request.matchdict['login']).get()
    except User.DoesNotExist:
        l.info('race')
        raise HTTPNotFound()

    return <frag>\
        # FIXME: read-only if it's not my profile
        <react_restimagefield image="{user.image}" url="/api/me" field="image" reload="{True}" />
        <react_resttextfield text="{user.about}" url="/api/me" field="about" label="About me" />
    </frag>