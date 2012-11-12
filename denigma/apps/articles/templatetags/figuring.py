"""Provides a template tag to map figures in a document to its respective references."""
import re

from django import template


register = template.Library()

@register.filter
def figures(text):
    """Maps figure references."""
    global number
    number = 1

    # Figure out all figure names and number figures:
    figure_names = {}
    #rc = re.compile('\*\*(?P<title>Figure: .+?)\.?\*\*')
    rc = re.compile(r'(?P<pre>\.\. figure\:\: .+?)\*\*(?P<title>Figure: .+?)\.?\*\*?', re.DOTALL)

    def translate(match):
        figure_name = match.group('title')
        figure_names[figure_name] = number
        figure_link = '\n.. _`Figure %s`: \n' % number
        figure_number = '**%s.**' % figure_name.replace('Figure: ', 'Figure %s: ' % number)
        globals()['number'] += 1
        #print match.group(0)
        return   figure_link +  match.group('pre') + figure_number         #return figure_number

        # Number all the figure references in text:
    text = rc.sub(translate, text.replace('\r', '')+'\n\n')
    #print text
    for figure_name, figure_number in figure_names.items():
        #print type(figure_name), type(figure_number)
        text = text.replace(figure_name, "`Figure %s`_" % figure_number)
    return text


if __name__ == '__main__':
    string = """dfff
[Figure: Test] sfgf

.. figure:: http:fdsf

   **Figure: Test.**"""

    string = """.. figure:: https://s3.amazonaws.com/circadian/Bidirectional_comparisons_of_DR_ageing_and_juvenile_signatures.png

    **Figure: Bidirectional comparisons of DR, ageing and juvenile signatures.**"""
    #rc = re.compile('\*\*(?P<title>Figure: .+?)\.?\*\*')
    rc = re.compile('\.\. figure\:\: \*\*(?P<title>Figure: .+?)\.?\*\*')
    rc = re.compile(r'(?P<pre>\.\. figure: .+)\*\*(?P<title>Figure: .+?)\.?\*\*', re.DOTALL)
    print re.findall(rc, string)
    text = figures(string)
    print(text)

