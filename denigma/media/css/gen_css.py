"""Creates a CSS file containing all the style definitions in the static media directory.

Uses pygments-styles_

.. _pygments-styles: http://pygments.org/docs/styles/

>>> from pygments.styles import STYLE_MAP
>>> STYLE_MAP.keys()
['default', 'emacs', 'friendly', 'colorful',
 'rrt', 'perldoc', 'borland', 'murphy',
 'tango', 'vs', 'trac', 'autumn', 'bw', 'pastie',
 'monokai', 'manni','fruity', 'vim', 'native'] # For dark background

Emacs and perldoc looks good.

Call it this way:
python gen_css.py pygments.css
"""
import sys

from pygments.formatters import HtmlFormatter
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error,\
    Number, Operator, Generic


class CustomStyle(Style):
    """"""
    default_style = ""
    styles = {
        Comment: 'italic #888',
        Keyword: 'bold #005',
        Name: '#f00',
        Name.Function: '#0f0',
        Name.Class: 'bold #0f0',
        String: 'bg:#eee #111'
    }


f = open(sys.argv[1], 'w')

# You can change style and html class here:
f.write(HtmlFormatter(style="perldoc").get_style_defs('.highlight'))#emacs
#f.write(HtmlFormatter(style=CustomStyle).style) #.get_style_defs('highlight'))



f.close()




