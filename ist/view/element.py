from xhpy3.xhpy.pylib import *
from ist.model.page import Page

class :ui:header(:x:element):
  attribute object user
  category %flow

  def render(self):
    user = self.getAttribute('user')
    a = <div id="header"><ui:logo/></div>
    if user:
      user_parts = [<ui:usermenu user={user} />]
    else:
      user_parts = [<ui:loginbox />, <ui:signupbox />]
    for part in user_parts:
      a.appendChild(part)
    return a

class :ui:page(:x:element):
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
          <ui:header user={user} />
          <ui:sidebar user={user} />
          {self.getChildren()}
        </body>
      </html>
    </x:doctype>

class :ui:usermenu(:x:element):
  attribute object user
  category %block

  def render(self):
    user = self.getAttribute('user')
    return \
    <div id="usermenu">
      Hello, {user.login}!
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
        <li><a href="/page/create">Create page</a></li>
      </ul>
    </div>

class :ui:logo(:x:element):
  category %block
  def render(self):
    return <span>logo</span>

class :ui:signupbox(:x:element):
  category %block

  def render(self):
    return \
    <div id="signupbox">
      <form action="/signup" method="post">
        <input name="login" type="text" placeholder="login" />
        <input name="passwd" type="password" placeholder="password" />
        <input name="email" type="text" placeholder="email address" />
        <input name="submit" type="submit" value="Sign up" />
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
      <div id="creator"></div>
      <script type="text/javascript">IS.addComposer(document.getElementById('creator'), 'asdf');</script>
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
