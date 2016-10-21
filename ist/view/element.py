#coding: pyxl
from ist.model.type import User, Page
from ist.model.base import ApiEncoder
from ist.view.react import *
from ..react import render
from ..util import *

from react.exceptions import ReactRenderingError

from pyxl.element import x_element
from pyxl import html

import json
import datetime
import traceback

# site elements
class x_layout(x_element):

    # FIXME: <doctype>
    def render(self, user):
        return <html>
            <head>
                <script type="text/javascript" src="/static/js/jquery.min.js"></script>
                <script type="text/javascript" src="/static/js/compiled/app.js"></script>
                <link href="/static/style/bundle.css" media="all" rel="stylesheet" />
                <link href="https://fonts.googleapis.com/css?family=Denk+One" rel="stylesheet" />
                <title>Title</title>
            </head>
            <body>
                <site_header user="{user}" />
                <div id="main">
                    <sidebar user="{user}" />
                    {self.children()}
                </div>
            </body>
        </html>

class x_site_header(x_element):
    def render(self, user):
        return <div id="ribbon">
            <div id="header">
                <logo/>
                <div id="jovilag"><a href="/">Jóvilág</a></div>
                <span id="egyutt">Együtt építjük</span>
                <user_header user="{user}" />
            </div>
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
    # TODO @required
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
                <li><a href="/">Főoldal</a></li>
                <li><a href="/page/all">Összes oldal</a></li>
                <if cond="{user}">
                    <li><a href="/page/my">Saját oldalak</a></li>
                    <li><a href="/{user.login}">Saját üzenőfal</a></li>
                    <li><a href="/page/create">Új oldal</a></li>
                </if>
            </ul>
        </div>

class x_rightbar(x_element):
    def render(self, user):
        x = <div id="rightbar" />
        if not user:
            x.append_children([<signup_info />])
        x.append_children(self.children())
        return x

class x_logo(x_element):
    def render(self):
        return <span id="logo"><a href="/"><img src="/static/img/logo.png" width="172" height="100"/></a></span>

class x_signupbox(x_element):
    def render(self):
        js_string = "IS.submit(event, this, function(user){document.location = '/hello';});"
        return <div id="signupbox">
            <p>Regisztráció</p><br/>
            <form data-url="/api/signup" id="signupbox" method="post" onsubmit={js_string} class="verticalform">
                <field name="login" type="text" placeholder="login">Név:</field>
                <field name="passwd" type="password" placeholder="jelszó">Jelszó:</field>
                <field name="email" type="text" placeholder="email">Email:</field>
                <p><input name="submit" type="submit" value="Regisztrálok" /></p>
            </form>
        </div>

class x_field(x_element):
    def render(self, name, type, placeholder):
        return <frag>
            <p>
                <label for="{name}">{self.children()}</label>
                <input id="{name}" name="{name}" type="{type}" placeholder="{placeholder}" />
                <span id="{name}_error" class="error"></span>
            </p>
        </frag>

class x_signup_info(x_element):
    def render(self):
        return <div id="signup_info">
            <p>Csatlakozz a Jóvilág közösséghez!</p><br/>
            <a href="/signup">Regisztráció</a>
        </div>

class x_loginbox(x_element):
    def render(self):
        js_string = "IS.submitLogin(event, this, function(user){document.location = '/';});"
        return <div id="loginbox">
            <form data-url="/api/login" id="login" method="post" onsubmit={js_string}>
                <input name="login" type="text" placeholder="login" />
                <input name="passwd" type="password" placeholder="jelszó" />
                <input name="submit" type="submit" value="Belépés" />
                <p id="error">
                    <span class="error"></span>
                </p>
            </form>
        </div>

class x_poster(x_element):
    def render(self):
        return <div id="posterbox">
            <react_poster />
        </div>

class x_createpage(x_element):
    def render(self):
        js_string = "IS.submit(event, this, function(page){document.location = '/'+page.permalink;});"
        return <form data-url="/api/page" id="createpage" method="post" onsubmit={js_string} class="verticalform">
            <react_imagefield name="image" />
            <field type="text" name="name" placeholder="téma, helység, cég...">Oldal neve</field>
            <field type="text" name="description" placeholder="Tömör leírás">Leírás</field>
            <input type="submit" name="submit" value="Oldal létrehozása" />
        </form>

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

class x_breadcrumb(x_element):
    def render(self, href):
        return <div>
            <a href={href}>
                &lt; {self.children()}
            </a>
        </div>

class x_page(x_element):
    def render(self, page: Page):
        return <div class="page">\
            <a href="/{page.permalink}">
                <if cond="{page.image}">
                    <img src="{page.image.uri(thumbnail='100x100')}"/>
                </if>
                <br/>
                {page.name}
            </a>
        </div>
