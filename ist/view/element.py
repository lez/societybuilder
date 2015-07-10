from xhpy3.xhpy.pylib import *

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
          <script type="text/javascript" src="/static/js/app.js"></script>
          <script type="text/javascript" src="/static/js/jquery.min.js"></script>
          <link href="/static/style/bundle.css" media="all" rel="stylesheet" />
          <title>Title, overwrite me!</title>
        </head>
        <body>
          <ui:header user={user} />
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
      <ui:creator />
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

