# -.- coding: utf8 -.-
"""Formats an article."""
import re
from datetime import datetime

from django import template


register = template.Library()

@register.filter
def footer(text, insert="###Page###"):
    """Inserts a a footer into a text, which is by default a page count."""
    return text + "\n.. footer:: " + insert + "\n"

@register.filter
def header(text, insert=datetime.now):
    """Inserts a header into a text, by default inserts the current time"""
    return text + "\n.. header:: " + insert + "\n"

@register.filter
def link(name, url=None):
    """Generates an rst external link by passing in a name and a url."""
    if not url:
        url = 'http://denigma.de/articles/' + name
    return  "`%s`_\n\n.. _`%s`: %s" % (name, name, url)

@register.filter
def coverPage(text):
    """Creates a Cover page break at ``@@@@``."""
    return text.replace('@@@@', """
.. raw:: pdf

    SetPageCounter 0 alpha

.. raw:: pdf

    PageBreak oneColumn

.. raw:: pdf

    SetPageCounter 2 lowerroman
""")

@register.filter
def pageBreak(text):
    """Breaks text into pages at ``++++`` (or eliminates ++++ transitions in html outputs)."""
    return text.replace("\n\n++++\n\n", '\n\n.. raw:: pdf\n\n    PageBreak oneColumn\n\n')

@register.filter
def tablesAndFigures(text):
    """Generates a list of all table and figures in a text."""
    header = '==========================\nList of Figures and Tables\n=========================='
    items = [header]
    rc = re.compile(r'\.\. figure\:\:.+?\*\*(?P<name>Figure \d+\:.+?)\.\*\*', re.DOTALL)
    items.extend(re.findall(rc, text))
    rc = re.compile(r'\.\. table\:\: \*\*(?P<name>Table \d+\: .+?)\*\*.')
    items.extend(re.findall(rc, text))

    def translate(match):
        return "\n\n".join(items)

    rc = re.compile(header)
    print re.findall(rc, text)
    return rc.sub(translate, text)


def glossary(text):
    glossary = {}
    findings = re.findall("[A-Z]{2,}", unicode(text)) #More than two capital letters.
    #print findings
    abbreviation_explained = re.findall("[a-z]?[A-Z]{2,}[a-z]? \(.*?\)", unicode(text)) #"([a-z]{1})?[A-Z]{2,}([a-z]{1})? \(.*?\)"
    for abbreviation_explaination in abbreviation_explained:
        #print abbreviation_explaination
        abbreviation = abbreviation_explaination.split(' (')[0]
        explaination = abbreviation_explaination.split('(')[1].split(')')[0]
        glossary[abbreviation] = explaination

    explaination_abbreviated = re.findall("\(([a-z]?[A-Z]{2,}[a-z]?)\)", unicode(text))
    #print explaination_abbreviated
    for explaination_abbreviation in explaination_abbreviated:
        number_of_words = len(explaination_abbreviation)
        if explaination_abbreviation[-1] == 's': # Plural
            number_of_words -= 1
            # Form a regular expression to fetch the explaination in front the abbreviation:
        word = '[A-Z,a-z,0-9]+ '
        regex = '%s\([a-z]?[A-Z]{2,}[a-z]?\)' % (word * number_of_words)
        #print regex
        results = re.findall(regex, unicode(text))
        for result in results:
            explaination = result.split('(')[0]
            abbreviation = result.split(' (')[1].split(')')[0]

            if explaination.startswith('19') or explaination.startswith('20'): continue
            try: # Continue if just a number as it is fetched Initial/year from the references.
                int(explaination)
                continue
            except:
                pass

            glossary[abbreviation] = explaination
            #print result

    abbreviations = "\n".join(["%s\n    %s" % (k, v) for k, v in glossary.items()])
    if "Glossary" in text:
        #print("Glossary in structure")
        #print(abbreviations)
        text = text.replace('========\nGlossary\n========', '========\nGlossary\n========\n%s' % abbreviations)
        #print text
    else:
        text += '========\nGlossary\n========\n'+abbreviations
    return text

def tablesAndFigures_test():
    string = """
==========================
List of Figures and Tables
==========================
Number Page

.. _`Figure 6`:
.. figure:: https://s3.amazonaws.com/gerontogenes/Common_terms.png
   :width: 400
   :height: 300

.. figure:: https://s3.amazonaws.com/gerontogenes/Common_terms_shared.png

   **Figure 6: Common terms shared by gerontogenes and ageing-suppressor genes.**


    .. _`Table 3`:
    .. table:: **Table 3: Induced and suppressed interactions common to yeast, worm and fly**. The functional enriched terms for either up- or down-regulated interaction associated to the DR-induced gene expression changes of multiple species (budding yeast, nematode, fruit fly) aer listed.

.. _`Figure 6`:
.. figure:: https://s3.amazonaws.com/gerontogenes/Common_terms.png
   :width: 400
   :height: 300

.. figure:: https://s3.amazonaws.com/gerontogenes/Common_terms_shared.png

   **Figure 7: Common terms shared by gerontogenes and ageing-suppressor genes.**


    .. _`Table 4`:
    .. table:: **Table 3: Induced and suppressed interactions common to yeast, worm and fly**. The functional enriched terms for either up- or down-regulated interaction associated to the DR-induced gene expression changes of multiple species (budding yeast, nematode, fruit fly) aer listed.


    """
    print tablesAndFigures(string)


if __name__ == '__main__':
   tablesAndFigures_test()