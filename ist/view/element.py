from xhpy3.xhpy.pylib import *
from ist.model.page import Page
from ist.model.user import Content, User
from ist.model.base import ModelEncoder
from ..react import render
import json

# helpers
class :x:jsx(:x:unsafe):

  def __str__(self):
    if not hasattr(self, '_react_path'):
      raise AttributeError('_react_path is a mandatory member of :jsx:*')
    self._react_classname = self._react_path.split('.')[0]
    self._react_id = self._react_classname.lower()
    render_react_element = '''IS.addAnyReactElement(IS.{class_name}, document.getElementById("{id_name}"), {attr});'''.format(
      class_name=self._react_classname,
      id_name=self._react_id,
      attr=ModelEncoder().encode(self._attr)
    )
    return '''
    <div id="{id_name}">{rendered}</div>
    <script type="text/javascript">
      {render_client_side}
    </script>
    '''.format(
      id_name=self._react_id,
      rendered=str(render(self._react_path, self._attr)),
      render_client_side=render_react_element
    )

class :react:commenter(:x:jsx):
  _react_path = 'Commenter.jsx'

class :react:creator(:x:jsx):
  _react_path = 'Poster.jsx'

class :react:test(:x:jsx):
  _react_path = 'Test.jsx'


# site elements
class :ui:layout(:x:element):
  attribute object user
  category %block

  def render(self):
    user = self.getAttribute('user')
    return \
    <x:doctype>
      <html>
        <head>
          <script type="text/javascript" src="/static/js/jquery.min.js"></script>
          <script type="text/javascript" src="/static/js/app.js"></script>
          <link href="/static/style/bundle.css" media="all" rel="stylesheet" />
          <title>Title</title>
        </head>
        <body>
          <div id="main">
            <ui:header user={user} />
            <ui:sidebar user={user} />
            <div id="content">
              {self.getChildren()}
            </div>
            <ui:rightbar user={user} />
          </div>
        </body>
      </html>
    </x:doctype>

class :ui:header(:x:element):
  attribute object user
  category %flow

  def render(self):
    user = self.getAttribute('user')
    return \
    <div id="header">
      <ui:logo/>
      <div id="jovilag">jóvilág</div>
      <ui:user_header user={user}/>
    </div>

class :ui:user_header(:x:element):
  attribute object user
  category %flow

  def render(self):
    user = self.getAttribute('user')
    a = <div id="user_header"/>
    if user:
      user_parts = [<ui:usermenu user={user} />]
    else:
      user_parts = [<ui:loginbox />]
    for part in user_parts:
      a.appendChild(part)
    return a

class :ui:usermenu(:x:element):
  attribute object user
  category %block

  def render(self):
    user = self.getAttribute('user')
    return \
    <div id="usermenu">
      Hello, <a href={'/'+user.login+'/profile'}>{user.login}</a>!
      <ui:logoutbutton />
    </div>

class :ui:sidebar(:x:element):
  attribute object user
  category %block

  def render(self):
    user = self.getAttribute('user')
    return \
    <div id="sidebar">
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/page/all">All pages</a></li>
        {<li><a href="/page/my">My pages</a></li> if user else None}
        {<li><a href="/me">Me</a></li> if user else None}
        {<li><a href="/page/create">Create page</a></li> if user else None}
      </ul>
    </div>

class :ui:rightbar(:x:element):
  attribute object user
  category %block

  def render(self):
    user = self.getAttribute('user')

    x = <div id="rightbar" />

    if not user:
      x.appendChild(<ui:signupbox />)

    return x

class :ui:logo(:x:element):
  category %block
  def render(self):
    return <span id="logo"><a href="/"><img src="/static/img/logo2.png" width="60" height="60"/></a></span>

class :ui:signupbox(:x:element):
  category %block

  def render(self):
    return \
    <div id="signupbox">
      <p>Sign up for this site.</p>
      <form action="/signup" method="post" class="verticalform">
        <p><label for="login">Name:</label><input id="login" name="login" type="text" placeholder="login" /></p>
        <p><label for="passwd">Password:</label><input id="passwd" name="passwd" type="password" placeholder="password" /></p>
        <p><label for="email">Email:</label><input id="email" name="email" type="text" placeholder="email address" /></p>
        <p><input name="submit" type="submit" value="Sign up" /></p>
      </form>
    </div>

class :ui:loginbox(:x:element):
  category %block

  def render(self):
    return \
    <div id="loginbox">
      <form action="/login" method="post">
        <input name="login" type="text" placeholder="login" />
        <input name="passwd" type="password" placeholder="password" />
        <input name="submit" type="submit" value="Log in" />
      </form>
    </div>

class :ui:logoutbutton(:x:element):
  category %block
  def render(self):
    return <a href="/logout">logout</a>

class :ui:creator(:x:element):
  category %block

  def render(self):
    return \
    <div id="creatorbox">
      <react:creator />
    </div>

class :ui:createpage(:x:element):
  category %block

  def render(self):
    return \
    <form data-url="/api/page" id="createpage" method="post" onsubmit="IS.submit(event, this);">
      <input type="text" name="name" placeholder="Name" />
      <input type="text" name="description" placeholder="Short description" />
      <input type="checkbox" name="owner_public" checked="checked" />
      <input type="submit" name="submit" value="Create Page" />
      <ui:inputimage name="image" />
    </form>

class :ui:inputimage(:x:element):
  category %block
  attribute string name @required

  def render(self):
    name = self.getAttribute('name')

    return \
    <input type="hidden" name={name}/>


class :ui:showpage(:x:element):
  attribute Page page,
            object user
  category %block

  def render(self):
    page = self.getAttribute('page')
    user = self.getAttribute('user')

    if page.user == user:
      info = "This page is YOURS"
    elif page.owner_public:
      owner = page.user
      info = "Owner: %s" % owner.login
    else:
      info = "Whose page is this?"

    return \
    <div id="showpage">
      <div class="info">{info}</div>
      <div class="title">{page.name}</div>
      <div class="description">{page.description}</div>
    </div>


class :ui:posts(:x:element):
  attribute object posts
  category %block

  def render(self):
    posts = self.getAttribute('posts')

    a = \
    <div id="posts"/>

    for post in posts:
        a.appendChild(<ui:post post={post} />)

    return a


class :ui:user(:x:element):
  attribute User user
  category %block

  def render(self):
    user = self.getAttribute('user')

    return \
    <span class="user">
      {user.login}:
    </span>


class :ui:post(:x:element):
  attribute object post
  category %block

  def render(self):
    post = self.getAttribute('post')

    return \
    <div class="post">
      <ui:user user={post.user} />
      <div class="content">{post.content}</div>
      <div class="when">@{post.created}</div>
    </div>


