from docutils import nodes
from docutils.parsers.rst import directives
from docutils.core import publish_parts

CODE = """\
<object type="application/x-shockwave-flash"
        width="%(width)s"
        height="%(height)s"
        class="youtube-embed"
        data="http://www.youtube.com/v/%(yid)s">
    <param name="movie" value="http://www.youtube.com/v/%(yid)s"></param>
    <param name="wmode" value="transparent"></param>
</object>
"""

# CODE = """\
# <embed
# width="%(width)s" height="%(height)s"
# src="http://www.youtube.com/v/%(yid)s"
# type="application/x-shockwave-flash">
# </embed>
# """

PARAM = """\n    <param name="%s" value="%s"></param>"""

def youtube(name, args, options, content, lineon,
            contentOffset, blockText, state, stateMachine):
    """Restructured text extension for inserting youtube embedded videos"""
    if len(content) == 0:
        return
    string_vars = {
        'yid': content[0],
        'width': 425,
        'height': 344,
       # 'extra': ''
    }
    extra_args = content[1:] # Becuase content[0] is ID
    extra_args = [ea.strip().split('=') for ea in extra_args] # key=value
    extra_args = [ea for ea in extra_args if len(ea) == 2] # drop bad lines
    extra_args = dict(extra_args)
    if 'width' in extra_args:
        string_vars['width'] = extra_args.pop('width')
    if 'height' in extra_args:
        string_vars['height'] = extra_args.pop('height')
    if extra_args:
        params = [PARAM % (key, extra_args[key]) for key in extra_args]
        #string_vars['extra'] = "".join(params)
    return [nodes.raw('', CODE % (string_vars), format='html')]
youtube.content = True
directives.register_directive('youtube', youtube)


def main():
    source = """\
This is some text.

.. youtube:: 2A2XBoxtcUA

This is some more text.
"""
    doc_parts = publish_parts(source,
                              settings_overrides={'output_encoding': 'utf8',
                                                  'initial_header_level': 2},
                              writer_name="html")
    print(doc_parts['html_body'])

if __name__ == '__main__':
    main()
