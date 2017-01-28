#coding: pyxl
from sb.model.type import User, Page
from sb.model.base import ApiEncoder
from ..react import render
from ..util import *

from react.exceptions import ReactRenderingError

from pyxl.element import x_element
from pyxl import html

import json
import datetime
import traceback

# helpers
class x_jsx(x_element):

    __validate_attrs__ = False

    def render(self):
        if not hasattr(self, '_react_path'):
            raise AttributeError('_react_path is a mandatory member of x_jsx*')

        self._react_classname = self._react_path.split('.')[0]
        self._react_id = random_string(10)

        render_react_element = '''IS.addAnyReactElement(IS.{class_name}, document.getElementById("{id_name}"), {attr});'''.format(
            class_name=self._react_classname,
            id_name=self._react_id,
            attr=ApiEncoder().encode(self.__attributes__)
        )

        try:
            content = render(self._react_path, self.__attributes__)
        except ReactRenderingError as e:
            print('ERROR RENDERING')
            print(e)
            content = ''

        return <frag>
            <div id="{self._react_id}" class="{'wrap_'+self._react_classname.lower()}">{html.rawhtml(content)}</div>
            <script type="text/javascript">{html.rawhtml(render_react_element + "\n")}</script>
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

class x_react_imagefield(x_jsx):
    _react_path = 'ImageField.jsx'

class x_react_thumbnail(x_jsx):
    _react_path = 'Thumbnail.jsx'

class x_react_userthumbnail(x_jsx):
    _react_path = 'UserThumbnail.jsx'

class x_react_pagethumbnail(x_jsx):
    _react_path = 'PageThumbnail.jsx'

class x_react_restimagefield(x_jsx):
    _react_path = 'RestImageField.jsx'

class x_react_resttextfield(x_jsx):
    _react_path = 'RestTextField.jsx'
