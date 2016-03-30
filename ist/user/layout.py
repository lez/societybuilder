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

    return <frag>
        # FIXME: read-only if it's not my profile
        <react_restimagefield image="{user.image}" url="/api/me" field="image" reload="{True}" />
        <react_resttextfield text="{user.about}" url="/api/me" field="about" label="About me" />
        <if cond="{user == request.user}">
            <a href="/{user.login}/change_password">Change password</a>
        </if>
    </frag>


@view_config(route_name='user_change_password', renderer='layout', permission='user')
def change_password(request):
    try:
        user = User.select().where(User.login == request.matchdict['login']).get()
        if user != request.user:
            raise HTTPNotFound()
    except User.DoesNotExist:
        raise HTTPNotFound()

    js_string = "IS.submit(event, this, function(user){document.location.reload(true);});"
    return <div id="change_password">
        <form data-url="/api/change_password" method="post" class="verticalform" onsubmit={js_string}>
            <field name="passwd" type="password" placeholder="current">Current password:</field>
            <field name="new_passwd" type="password" placeholder="new">New password:</field>
            <field name="new_passwd_again" type="password" placeholder="repeat new">Repeat new password:</field>
            <p><input name="submit" type="submit" value="Change" /></p>
        </form>
    </div>
