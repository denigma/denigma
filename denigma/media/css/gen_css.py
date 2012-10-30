"""Created a CSS file containing all the style definitios in the static media directory.

Call it this way:
python gen_css.py pygments.css
"""
import sys

from pygments.formatters import HtmlFormatter

f = open(sys.argv[1], 'w')

# You can change style and html class here:
f.write(HtmlFormatter(style="colorful").get_style_defs('.highlight'))

f.close()
