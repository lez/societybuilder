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
    a = <x:doctype><html><head><x:frag><script type="text/javascript" src="/static/js/app.js"></script><script type="text/javascript" src="/static/js/jquery.min.js"></script><link href="/static/style/bundle.css" media="all" rel="stylesheet" /></x:frag><title>Title, overwrite me!</title></head><body><ui:header user={user} /></body></html></x:doctype>
    # a = <html><body></body></html>
    return a

class :ui:usermenu(:x:element):
  attribute object user
  category %block

  def render(self):
    user = self.getAttribute('user')
    a = <div id="usermenu">Hello, {user.login}!</div>
    a.appendChild(<ui:logoutbutton />)
    a.appendChild(<ui:creator />)
    return a

class :ui:logo(:x:element):
  category %block
  def render(self):
    return <img src="/static/img/is_logo.gif" width="40" height="40" />



class :ui:signupbox(:x:element):
  category %block

  def render(self):
    a = <div id="signupbox"><form action="/signup" method="post"><input name="login" type="text" placeholder="login" /><input name="passwd" type="password" placeholder="password" /><input name="email" type="text" placeholder="email address" /><input name="submit" type="submit" value="Sign up" /></form></div>
    return a

class :ui:loginbox(:x:element):
  category %block

  def render(self):
    a = <div id="loginbox"><form action="/login" method="post"><input name="login" type="text" placeholder="login" /><input name="passwd" type="password" placeholder="password" /><input name="submit" type="submit" value="Log in" /></form></div>
    return a

class :ui:logoutbutton(:x:element):
  category %block
  def render(self):
    a = <a href="/logout">logout</a>
    return a

class :ui:creator(:x:element):
  category %block
  def render(self):
    a = <div id="creatorbox"><div id="creator"></div><script type="text/javascript">IS.addComposer(document.getElementById('creator'), 'asdf');</script></div>
    return a

