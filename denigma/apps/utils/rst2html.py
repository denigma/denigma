#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, re
from docutils import nodes, utils
from docutils.parsers.rst.directives import images
from docutils.transforms import TransformError, Transform, parts
from docutils.parsers.rst import Directive, directives, states, roles
from docutils.writers.html4css1 import HTMLTranslator


class math(nodes.Inline, nodes.TextElement):     pass
class nosectnum(nodes.Inline,nodes.TextElement): pass
class displaymath(nodes.Part, nodes.Element):    pass
class eqref(nodes.Inline, nodes.TextElement):    pass
class figref(nodes.Inline, nodes.TextElement):   pass
class abstract(nodes.General, nodes.Element):    pass
class keywords(nodes.General, nodes.Element):    pass
class video(nodes.General, nodes.Inline, nodes.Element): pass
class media(nodes.General, nodes.Inline, nodes.Element): pass

# --- bib_reference -----------------------------------------------------------
#
# 
#
def bib_reference(text):
    if not ':' in text:
        return text
    authors,date = text.split(':')
    authors = authors.split('+')
    if authors[-1] == 'Al':
        return authors[0] + ' et al. ' + date
    elif len(authors) == 1:
        return authors[0] + ' ' + date
    elif len(authors) == 2:
        return authors[0] + ' and ' + authors[1] + ' ' + date
    else:
        return authors[0] + ' et al. ' + date

# --- bib_entry ---------------------------------------------------------------
#
# 
#
def bib_entry(text):
    if not ':' in text:
        return text
    authors,date = text.split(':')
    authors = authors.split('+')
    if authors[-1] == 'Al':
        return authors[0] + ' et al. (' + date + ')'
    elif len(authors) == 1:
        return authors[0] + ' (' + date + ')'
    elif len(authors) == 2:
        return authors[0] + ' and ' + authors[1] + ' (' + date + ')'
    else:
        return authors[0] + ' et al. (' + date + ')'


# --- wrap display math -------------------------------------------------------
#
# 
#
def wrap_displaymath(math, label):
    parts = math.split('\n\n')
    ret = []
    for i, part in enumerate(parts):
        if label is not None and i == 0:
            ret.append('\\begin{split}%s\\end{split}' % part +
                       (label and '\\label{'+label+'}' or ''))
        else:
            ret.append('\\begin{split}%s\\end{split}\\notag' % part)
    return '\\begin{gather}\n' + '\\\\'.join(ret) + '\n\\end{gather}'


# --- sectnum transform -------------------------------------------------------
#
#  This sectnum tranform takes care of nosectnum directives
#
class SectNum(parts.SectNum):
    def update_section_numbers(self, node, prefix=(), depth=0):
        depth += 1
        if prefix:
            sectnum = 1
        else:
            sectnum = self.startvalue
        for child in node:
            if isinstance(child, nodes.section):
                numbers = prefix + (str(sectnum),)
                title = child[0]
                if not child.traverse(nosectnum):
                    # Use &nbsp; for spacing:
                    generated = nodes.generated(
                        '', (self.prefix + '.'.join(numbers) + self.suffix
                             +  u'\u00a0' * 3),
                        classes=['sectnum'])
                    title.insert(0, generated)
                    title['auto'] = 1
                if depth < self.maxdepth:
                    self.update_section_numbers(child, numbers, depth)
                sectnum += 1


# --- Equation references -----------------------------------------------------
#
# This class solves pending equation references throughout the whole document
#
class EquationReferences(Transform):
    default_priority = 260
    def apply(self):
        num = 0
        numbers = {}
        for node in self.document.traverse(displaymath):
            if node['label'] is not None:
                num += 1
                node['number'] = num
                numbers[node['label']] = num
            else:
                node['number'] = None
        for node in self.document.traverse(eqref):
            if node['target'] not in numbers:
                continue
            num = '(%d)' % numbers[node['target']]
            node[0] = nodes.Text(num, num)


# --- Figure references -------------------------------------------------------
#
# This class solves pending figure references throughout the whole document
#
class FigureReferences(Transform):
    default_priority = 260
    def apply(self):
        num = 0
        numbers = {}
        for node in self.document.traverse(nodes.figure):
            if node['label'] is not None:
                num += 1
                node['number'] = num
                numbers[node['label']] = num
            else:
                node['number'] = None
        for node in self.document.traverse(figref):
            if node['target'] not in numbers:
                continue
            num = '(%d)' % numbers[node['target']]
            node[0] = nodes.Text(num, num)


# --- math directive ----------------------------------------------------------
#
#
#
class Math(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {'label': directives.unchanged,
                   'nowrap': directives.flag}
    def run(self):
        latex = '\n'.join(self.content)
        if self.arguments and self.arguments[0]:
            latex = self.arguments[0] + '\n\n' + latex
        node = displaymath()
        node['latex'] = latex
        node['label'] = self.options.get('label', None)
        node['nowrap'] = 'nowrap' in self.options
        ret = [node]
        if node['label']:
            tnode = nodes.target('', '', ids=['equation-' + node['label']])
            self.state.document.note_explicit_target(tnode)
            ret.insert(0, tnode)
        return ret
directives.register_directive('math', Math)


# --- abstract directive ------------------------------------------------------
#
#  
#
class Abstract(Directive):
    required_arguments, optional_arguments = 0,1
    final_argument_whitespace = True
    has_content = True
    def run(self):
        self.assert_has_content()
        node = abstract(self.block_text, **self.options)
        if self.arguments:
            node['title'] = self.arguments[0]
        else:
            node['title'] = u'Abstract'
        node['abstract'] = u'\n'.join(self.content)
        return [node]
directives.register_directive('abstract', Abstract)


# --- keywords directive ------------------------------------------------------
#
# 
#
class Keywords(Directive):
    required_arguments, optional_arguments = 0,1
    final_argument_whitespace = True
    has_content = True
    def run(self):
        self.assert_has_content()
        node = keywords(self.block_text, **self.options)
        if self.arguments:
            node['title'] = self.arguments[0]
        else:
            node['title'] = u'Keywords'
        node['keywords'] = u'\n'.join(self.content)
        return [node]
directives.register_directive('keywords', Keywords)


# --- video directive ---------------------------------------------------------
#
# Video inclusion
#
class Video(images.Image):
    """ Video inclusion """
    def align(argument):
        return directives.choice(argument, images.Image.align_h_values)
    option_spec = {'autoplay': directives.flag,
                   'loop': directives.flag,
                   'controls': directives.flag,
                   'height': directives.length_or_unitless,
                   'width': directives.length_or_percentage_or_unitless,
                   'align': align,
                   'class': directives.class_option}
    def run(self):
        old_image_node = nodes.image
        nodes.image = video
        node = images.Image.run(self)
        nodes.image = old_image_node
        return node
directives.register_directive('video', Video)

# --- media directive ---------------------------------------------------------
#
# Video or image (based on uri extension)
#
class Media(Video,images.Image):
    ''' Media inclusion '''
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = images.Image.option_spec.copy()
    option_spec.update(Video.option_spec.copy())
    def run(self):
        uri = directives.uri(self.arguments[0])
        if uri.split('.')[-1] in ['ogg', 'mpg', 'mp4', 'avi', 'mpeg']:
            return Video.run(self)
        else:
            return images.Image.run(self)
directives.register_directive('media', Media)

# --- figure directive --------------------------------------------------------
#
# figure redefinition to include image or movie inside
#
class Figure(Media):
    """ Figure with caption """
    def align(argument):
        return directives.choice(argument, directives.images.Image.align_h_values)
    def figwidth_value(argument):
        if argument.lower() == 'image':
            return 'image'
        else:
            return directives.length_or_percentage_or_unitless(argument, 'px')
    option_spec = Media.option_spec.copy()
    option_spec['label'] = directives.unchanged_required
    option_spec['figwidth'] = figwidth_value
    option_spec['figclass'] = directives.class_option
    option_spec['align'] = align
    has_content = True
    def run(self):
        figwidth = self.options.pop('figwidth', None)
        figclasses = self.options.pop('figclass', None)
        align = self.options.pop('align', None)
        (media_node,) = Media.run(self)
        if isinstance(media_node, nodes.system_message):
            return [media_node]
        figure_node = nodes.figure('', media_node)
        if figwidth == 'image':
            if PIL and self.state.document.settings.file_insertion_enabled:
                # PIL doesn't like Unicode paths:
                try:
                    i = PIL.open(str(media_node['uri']))
                except (IOError, UnicodeError):
                    pass
                else:
                    self.state.document.settings.record_dependencies.add(
                        media_node['uri'])
                    figure_node['width'] = i.size[0]
        elif figwidth is not None:
            figure_node['width'] = figwidth
        if figclasses:
            figure_node['classes'] += figclasses
        if align:
            figure_node['align'] = align
        if self.content:
            node = nodes.Element()          # anonymous container for parsing
            self.state.nested_parse(self.content, self.content_offset, node)
            first_node = node[0]
            if isinstance(first_node, nodes.paragraph):
                caption = nodes.caption(first_node.rawsource, '',
                    *first_node.children)
                figure_node += caption
            elif not (isinstance(first_node, nodes.comment)
                      and len(first_node) == 0):
                error = self.state_machine.reporter.error(
                    'Figure caption must be a paragraph or empty comment.',
                    nodes.literal_block(self.block_text, self.block_text),
                    line=self.lineno)
                return [figure_node, error]
            if len(node) > 1:
                figure_node += nodes.legend('', *node[1:])
        node = figure_node

        node['label'] = self.options.get('label', None)
        if not node['label']:
            node['label'] = self.options.get('uri')
        node['number'] = None
        ret = [node]
        if node['label']:
            key = node['label']
            tnode = nodes.target('', '', ids=['figure-' + node['label']])
            self.state.document.note_explicit_target(tnode)
            ret.insert(0, tnode)
        return ret
directives.register_directive('figure', Figure)


# --- sectnum directive --------------------------------------------------------
#
# 
#
class Sectnum(Directive):
    """Automatic section numbering."""

    option_spec = {'depth': int,
                   'start': int,
                   'prefix': directives.unchanged_required,
                   'suffix': directives.unchanged_required}
    def run(self):
        pending = nodes.pending(SectNum)
        pending.details.update(self.options)
        self.state_machine.document.note_pending(pending)
        return [pending]
directives.register_directive('sectnum', Sectnum)

# --- nosectnum directive -----------------------------------------------------
#
# 
#
class NoSectnum(Directive):
    """Disable automatic section numbering."""
    required_arguments, optional_arguments = 0,0
    final_argument_whitespace = True
    has_content = False
    def run(self):
        node = nosectnum(self.block_text, **self.options)
        return [node]
directives.register_directive('nosectnum', NoSectnum)


# --- math role ---------------------------------------------------------------
#
# 
#
def math_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    latex = utils.unescape(text, restore_backslashes=True)
    return [math(latex=latex)], []
math_role.content = True
roles.register_canonical_role('math', math_role)




# --- eq role -----------------------------------------------------------------
# 
# `eq` role allows to refer to an equation identified by a label
#
def eq_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    text = utils.unescape(text)
    node = eqref('(?)', '(?)', target=text)
    pending = nodes.pending(EquationReferences)
    inliner.document.note_pending(pending)
    return [node], []
eq_role.content = True
roles.register_canonical_role('eq', eq_role)


# --- fig role ----------------------------------------------------------------
#
# `fig` role allows to refer to a figure identified by a label
#
def fig_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    text = utils.unescape(text)
    node = figref('(?)', '(?)', target=text)
    pending = nodes.pending(FigureReferences)
    inliner.document.note_pending(pending)
    return [node], []
fig_role.content = True
roles.register_canonical_role('fig', fig_role)


# --- html eqref --------------------------------------------------------------
def html_visit_eqref(self, node):
    self.body.append('<a href="#equation-%s">' % node['target'])
def html_depart_eqref(self, node):
    self.body.append('</a>')
HTMLTranslator.visit_eqref = html_visit_eqref
HTMLTranslator.depart_eqref = html_depart_eqref

# --- html figref --------------------------------------------------------------
def html_visit_figref(self, node):
    self.body.append('<a href="#figure-%s">' % node['target'])
def html_depart_figref(self, node):
    self.body.append('</a>')
HTMLTranslator.visit_figref = html_visit_figref
HTMLTranslator.depart_figref = html_depart_figref

# --- html math ---------------------------------------------------------------
def html_visit_math(self, node):
    self.body.append(self.starttag(node, 'span', '', CLASS='math'))
    self.body.append(self.encode(node['latex']) + '</span>')
    raise nodes.SkipNode
HTMLTranslator.visit_math = html_visit_math

# --- html displaymath -------------------------------------------------------
def html_visit_displaymath(self, node):
    if node['nowrap']:
        self.body.append(self.starttag(node, 'div', CLASS='math'))
        self.body.append(node['latex'])
        self.body.append('</div>')
        raise nodes.SkipNode
    for i, part in enumerate(node['latex'].split('\n\n')):
        part = self.encode(part)
        if i == 0:
            # necessary to e.g. set the id property correctly
            if node['number']:
                self.body.append('<span class="eqno">(%s)</span>' %
                                 node['number'])
            self.body.append(self.starttag(node, 'div', CLASS='math'))
        else:
            # but only once!
            self.body.append('<div class="math">')
        if '&' in part or '\\\\' in part:
            self.body.append('\\begin{split}' + part + '\\end{split}')
        else:
            self.body.append(part)
        self.body.append('</div>\n')
    raise nodes.SkipNode
HTMLTranslator.visit_displaymath = html_visit_displaymath

# --- html abstract -----------------------------------------------------------
def html_visit_abstract(self, node):
    self.body.append(self.starttag(node, 'div', CLASS='abstract'))
    self.body.append(self.starttag(node, 'span', suffix='', CLASS='title'))
    self.body.append('%s | </span>\n' % node['title'])
    self.body.append('%s\n</div>\n' % node['abstract'])
    raise nodes.SkipNode
HTMLTranslator.visit_abstract = html_visit_abstract

# --- html keywords -----------------------------------------------------------
def html_visit_keywords(self, node):
    self.body.append(self.starttag(node, 'div', CLASS='keywords'))
    self.body.append(self.starttag(node, 'span', suffix='', CLASS='title'))
    self.body.append('%s | </span>\n' % node['title'])
    self.body.append('%s\n</div>\n' % node['keywords'])
    raise nodes.SkipNode
HTMLTranslator.visit_keywords = html_visit_keywords

# --- html document -----------------------------------------------------------
def html_visit_document(self, node):
    self.head.append('<title>%s</title>\n'
                     % self.encode(node.get('title', '')))
    self.head.append('<script src="jsMath/easy/load.js"></script>\n')
    self.body.append(
        '''\n<noscript>\n'''
        '''  <div style="color:#cc0000; text-align:center">\n'''
        '''   <b>Warning: '''
        '''   <a href="http://www.math.union.edu/locate/jsMath">jsMath</a>\n'''
        '''   requires JavaScript to process the mathematics on this page.<br>\n'''
        '''   If your browser supports JavaScript, be sure it is enabled.</b>\n'''
        '''  </div>\n'''
        '''</noscript>\n\n''')
HTMLTranslator.visit_document = html_visit_document


# --- html citation  ----------------------------------------------------------
def html_visit_citation(self, node):
    label = node[0].astext()
    if ':' in label:
        self.body.append(self.starttag(node, 'div',
            CLASS='bibitem'))
        self.body.append('<p>')
    else:
        self.body.append(self.starttag(node, 'table',
            CLASS='docutils citation',
            frame="void", rules="none"))
        self.body.append('<colgroup><col class="label" /><col /></colgroup>\n'
                         '<tbody valign="top">\n'
                         '<tr>')
    self.footnote_backrefs(node)
def html_depart_citation(self, node):
    label = node[0].astext()
    if ':' in label:
        self.body.append('</p>')
        self.body.append('</div>\n')
    else:
        self.body.append('</td></tr>\n'
                         '</tbody>\n</table>\n')
HTMLTranslator.visit_citation = html_visit_citation
HTMLTranslator.depart_citation = html_depart_citation


# --- html reference ----------------------------------------------------------
def html_visit_reference(self, node):
    atts = {'class': 'reference'}
    if 'refuri' in node:
        atts['href'] = node['refuri']
        if ( self.settings.cloak_email_addresses
             and atts['href'].startswith('mailto:')):
            atts['href'] = self.cloak_mailto(atts['href'])
            self.in_mailto = 1
        atts['class'] += ' external'
    else:
        assert 'refid' in node,\
        'References must have "refuri" or "refid" attribute.'
        atts['href'] = '#' + node['refid']
        atts['class'] += ' internal'
    if not isinstance(node.parent, nodes.TextElement):
        assert len(node) == 1 and (isinstance(node[0], nodes.image) or
                                   isinstance(node[0], video))
        if isinstance(node[0], nodes.image):
            atts['class'] += ' image-reference'
        else:
            atts['class'] += ' video-reference'
    self.body.append(self.starttag(node, 'a', '', **atts))
HTMLTranslator.visit_reference = html_visit_reference


# --- html citation reference --------------------------------------------------
def html_visit_citation_reference(self, node):
    label = bib_reference(node.children[0].astext())
    href = '#' + node['refid']
    if ':' in node.children[0].astext():
        label = '(' + label + ')'
    else:
        label = '[' + label + ']'
    self.body.append(self.starttag(node, 'a', '',
        CLASS='citation-reference', href=href))
    self.body.append(label)
    self.body.append('</a>')
    raise nodes.SkipNode
HTMLTranslator.visit_citation_reference = html_visit_citation_reference


# --- html label ---------------------------------------------------------------
def html_visit_label(self, node):
    label = bib_entry(node.children[0].astext())
    if ':' in node.children[0].astext():
        self.body.append(self.starttag(node, 'span', '%s' % self.context.pop(),
            CLASS='label'))
    else:
        self.body.append(self.starttag(node, 'td', '%s[' % self.context.pop(),
            CLASS='label'))
    self.body.append(label)
    if ':' in node.children[0].astext():
        self.body.append('%s %s' % (self.context.pop(), self.context.pop()))
    else:
        self.body.append(']%s</td><td>%s' % (self.context.pop(), self.context.pop()))
    raise nodes.SkipNode
HTMLTranslator.visit_label = html_visit_label


# --- html caption -------------------------------------------------------------
#
# Add a number to figure caption
#
def html_visit_caption(self, node):
    self.body.append(self.starttag(node, 'p', '', CLASS='caption'))
    number = node.parent['number']
    self.body.append('<span class="figno">Figure %s. </span>' % number)
def html_depart_caption(self, node):
    self.body.append('</p>\n')
HTMLTranslator.visit_caption = html_visit_caption
HTMLTranslator.depart_caption = html_depart_caption


# --- html no sectnum ---------------------------------------------------------
#
# Indicate current section must not be numbered
#
def html_visit_nosectnum(self, node):
    raise nodes.SkipNode
def html_depart_nosectnum(self, node):
    raise nodes.SkipNode
HTMLTranslator.visit_nosectnum = html_visit_nosectnum
HTMLTranslator.depart_nosectnum = html_depart_nosectnum


# --- html video --------------------------------------------------------------
def html_visit_video(self, node):
    atts = {}
    if 'controls' in node:
        atts['controls'] = True
    if 'loop' in node:
        atts['loop'] = True
    if 'autoplay' in node:
        atts['autoplay'] = True
    if 'width' in node:
        atts['width'] = node['width']
    if 'height' in node:
        atts['height'] = node['height']
    style = []
    for att_name in 'width', 'height':
        if att_name in atts:
            if re.match(r'^[0-9.]+$', atts[att_name]):
                # Interpret unitless values as pixels.
                atts[att_name] += 'px'
            style.append('%s: %s;' % (att_name, atts[att_name]))
            del atts[att_name]
    if style:
        atts['style'] = ' '.join(style)
    if (isinstance(node.parent, nodes.TextElement) or
        (isinstance(node.parent, nodes.reference) and
         not isinstance(node.parent.parent, nodes.TextElement))):
        # Inline context or surrounded by <a>...</a>.
        suffix = ''
    else:
        suffix = '\n'
    if 'classes' in node and 'align-center' in node['classes']:
        node['align'] = 'center'
    if 'align' in node:
        if node['align'] == 'center':
            # "align" attribute is set in surrounding "div" element.
            self.body.append('<div align="center" class="align-center">')
            self.context.append('</div>\n')
            suffix = ''
        else:
            # "align" attribute is set in "img" element.
            atts['align'] = node['align']
            self.context.append('')
        atts['class'] = 'align-%s' % node['align']
    else:
        self.context.append('')
    self.body.append(self.starttag(node, 'video', suffix, **atts))
    for filename in node['uri'].split(','):
        self.body.append(self.starttag(node, 'source', '', **{'src' : filename}))
        self.body.append('</source>\n')

def html_depart_video(self, node):
    self.body.append('</video>\n')
    self.body.append(self.context.pop())

HTMLTranslator.visit_video = html_visit_video
HTMLTranslator.depart_video = html_depart_video



from docutils.core import publish_cmdline, default_description
description = ('Generates (X)HTML documents from standalone reStructuredText '
               'sources.  ' + default_description)
publish_cmdline(writer_name='html', description=description)

