from docx import Document
from docx.shared import RGBColor
from collections import defaultdict
import xml.etree.ElementTree as ET
nsmap = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def get_common_style(paragraph):

    if paragraph.text == "":
        return (
            None,
            None,
            False,
            None,
            False,
            False,
        )

    font_size = defaultdict()
    bold = defaultdict()
    italic = defaultdict()
    underline = defaultdict()
    font_color = defaultdict()
    font_name = defaultdict()

    for run in paragraph.runs:
        font_size[run.font.size] = font_size.get(run.font.size, 0) + len(run.text)
        font_color[run.font.color.rgb] = font_color.get(run.font.color.rgb, 0) + len(
            run.text
        )
        font_name[run.font.name] = font_name.get(run.font.name, 0) + len(run.text)
        italic[run.italic] = italic.get(run.italic, 0) + len(run.text)
        bold[run.bold] = bold.get(run.bold, 0) + len(run.text)
        underline[run.underline] = underline.get(run.underline, 0) + len(run.text)

    font_size = dict(sorted(font_size.items(), key=lambda item: item[1], reverse=True))
    font_color = dict(
        sorted(font_color.items(), key=lambda item: item[1], reverse=True)
    )
    font_name = dict(sorted(font_name.items(), key=lambda item: item[1], reverse=True))
    bold = dict(sorted(bold.items(), key=lambda item: item[1], reverse=True))
    underline = dict(sorted(underline.items(), key=lambda item: item[1], reverse=True))
    italic = dict(sorted(italic.items(), key=lambda item: item[1], reverse=True))

    return (
        list(font_size.keys())[0],
        list(font_name.keys())[0],
        list(bold.keys())[0],
        list(font_color.keys())[0],
        list(underline.keys())[0],
        list(italic.keys())[0],
    )


def qn(tag):
    prefix, tagroot = tag.split(':')
    uri = nsmap[prefix]
    return '{{{}}}{}'.format(uri, tagroot)

def check_if_paragraph_has_text(paragraph):
    # root = ET.fromstring(paragraph._p.xml)

    # for child in root.iter():
    #     if child.tag == qn('w:t') and child.text != '':
    #         return True

    if paragraph.text != '':
        return True

    return False

def check_if_cell_is_string(cell):
    if cell.data_type == 's' and cell.value != '':
        return True
    
    return False