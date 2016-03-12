#coding: pyxl
from ist.model.type import User, Page
from ist.model.base import ApiEncoder
from ..react import render
from ..util import *

from pyxl.element import x_element
from pyxl import html

import json
import datetime

# helpers
class x_jsx(x_element):

    __validate_attrs__ = False

    def render(self):
        if not hasattr(self, '_react_path'):
            raise AttributeError('_react_path is a mandatory member of x_jsx*')  # TODO fix this antipattern

        self._react_classname = self._react_path.split('.')[0]
        self._react_id = random_string(10)

        render_react_element = '''IS.addAnyReactElement(IS.{class_name}, document.getElementById("{id_name}"), {attr});'''.format(
            class_name=self._react_classname,
            id_name=self._react_id,
            attr=ApiEncoder().encode(self.__attributes__)
        )

        return <frag>
            <div id="{self._react_id}" class="{'wrap_'+self._react_classname.lower()}">{html.rawhtml(render(self._react_path, self._attr))}</div>
            <script type="text/javascript">{html.rawhtml(render_react_element)}</script>
        </frag>


class x_react_commenter(x_jsx):
    _react_path = 'Commenter.jsx'

class x_react_comment(x_jsx):
    _react_path = 'Comment.jsx'

class x_react_commentpanel(x_jsx):
    _react_path = 'CommentPanel.jsx'

class x_react_comments(x_jsx):
    _react_path = 'Comments.jsx'

class x_react_poster(x_jsx):
    _react_path = 'Poster.jsx'

class x_react_post(x_jsx):
    _react_path = 'Post.jsx'

class x_react_test(x_jsx):
    _react_path = 'Test.jsx'

class x_react_images(x_jsx):
    _react_path = 'Images.jsx'

class x_react_profileimage(x_jsx):
    _react_path = 'ProfileImage.jsx'

class x_react_editprofileimage(x_jsx):
    _react_path = 'EditProfileImage.jsx'

class x_react_imagefield(x_jsx):
    _react_path = 'ImageField.jsx'

class x_react_thumbnail(x_jsx):
    _react_path = 'Thumbnail.jsx'

class x_react_userthumbnail(x_jsx):
    _react_path = 'UserThumbnail.jsx'

class x_react_restimagefield(x_jsx):
    _react_path = 'RestImageField.jsx'

class x_react_resttextfield(x_jsx):
    _react_path = 'RestTextField.jsx'

# site elements
class x_layout(x_element):

    # FIXME: <doctype>
    def render(self, user):
        return <html>
            <head>
                <script type="text/javascript" src="/static/js/jquery.min.js"></script>
                <script type="text/javascript" src="/static/js/compiled/app.js"></script>
                <link href="/static/style/bundle.css" media="all" rel="stylesheet" />
                <title>Title</title>
            </head>
            <body>
                <div id="main">
                    <site_header user="{user}" />
                    <sidebar user="{user}" />
                    {self.children()}
                </div>
            </body>
        </html>

class x_site_header(x_element):
    def render(self, user):
        return <div id="header">
            <logo/>
            <div id="jovilag">jóvilág</div>
            <user_header user="{user}" />
        </div>

class x_user_header(x_element):
    def render(self, user):
        a = <div id="user_header"/>
        if user:
            user_parts = [<usermenu user="{user}" />]
        else:
            user_parts = [<loginbox />]
        a.append_children(user_parts)
        return a

class x_usermenu(x_element):
    def render(self, user):
        return <div id="usermenu">
            <logoutbutton />
            <profilemenu user="{user}" />
        </div>

class x_logoutbutton(x_element):
    def render(self):
        return <span class="logoutbutton"><a href="/logout">logout</a></span>

class x_userlink(x_element):
    def render(self, user: User):  # FIXME @required
        return <span class="userlink"><a href="/{user.login}/profile">{user.login}</a></span>

class x_profilemenu(x_element):
  # XXX @required
    def render(self, user: User):
        return <a href="/{user.login}/profile">
            <div id="profilemenu">
                <span class="userlink">{user.login}</span>
                <react_userthumbnail user="{user}" />
            </div>
        </a>

class x_sidebar(x_element):
    def render(self, user: User):
        return <div id="sidebar">
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/page/all">All pages</a></li>
                <if cond="{user}">
                    <li><a href="/page/my">My pages</a></li>
                    <li><a href="/me">Me</a></li>
                    <li><a href="/page/create">Create page</a></li>
                </if>
            </ul>
        </div>

class x_rightbar(x_element):
    def render(self, user):
        x = <div id="rightbar" />
        if not user:
            x.append_children([<signupbox />])
        x.append_children(self.children())
        return x

class x_logo(x_element):
    def render(self):
        return <span id="logo"><a href="/"><img src="/static/img/logo2.png" width="60" height="60"/></a></span>

class x_signupbox(x_element):
    def render(self):
        return <div id="signupbox">
            <p>Sign up for this site.</p>
            <form action="/signup" method="post" class="verticalform">
                  <p><label for="login">Name:</label><input id="login" name="login" type="text" placeholder="login" /></p>
                  <p><label for="passwd">Password:</label><input id="passwd" name="passwd" type="password" placeholder="password" /></p>
                  <p><label for="email">Email:</label><input id="email" name="email" type="text" placeholder="email address" /></p>
                  <p><input name="submit" type="submit" value="Sign up" /></p>
            </form>
        </div>

class x_loginbox(x_element):
    def render(self):
        return <div id="loginbox">
            <form action="/login" method="post">
                <input name="login" type="text" placeholder="login" />
                <input name="passwd" type="password" placeholder="password" />
                <input name="submit" type="submit" value="Log in" />
            </form>
        </div>

class x_poster(x_element):
    def render(self):
        return <div id="posterbox">
            <react_poster />
        </div>

class x_createpage(x_element):
    def render(self):
        js_string = "IS.submit(event, this, function(page){document.location = '/page/'+page.id+'/show';});"
        return <form data-url="/api/page" id="createpage" method="post" onsubmit={js_string}>
            <input type="text" name="name" placeholder="Name" />
            <input type="text" name="description" placeholder="Short description" />
            <input type="checkbox" name="is_owner_public" checked="checked" />
            <input type="submit" name="submit" value="Create Page" />
#            <inputimage name="image" />
        </form>

class x_inputimage(x_element):
    # @required
    def render(self, name):
        return <input type="hidden" name="{name}" />

class x_showpage(x_element):
    def render(self, user: User, page: Page):
        return <div id="showpage">
            <div class="title">{page.name}</div>
        </div>

class x_posts(x_element):
    def render(self, posts, user):
        a = <div id="posts" />

        for post in posts:
            a.append_children([<react_post post="{post}" user="{user}" />])
        return a

class x_user(x_element):
    def render(self, user: User):
        return <div class="user">
            <img src="{user.thumbnail('60x60')}" />
        </div>

class x_content_header(x_element):
    def render(self):
        return <div class="content_header">
            {self.children()}
        </div>