from io import StringIO
from xml.etree import ElementTree

from PySide2 import QtWidgets
from pyside2uic import compileUi


def loadUiType(ui_file):
    parsed_xml = ElementTree.parse(ui_file)
    widget_class = parsed_xml.find('widget').get('class')
    form_class = parsed_xml.find('class').text

    with open(ui_file, encoding='utf8') as input_file:
        output = StringIO()
        compileUi(input_file, output, from_imports=True)
        scope = globals().copy()
        exec(output.getvalue(), scope)
        form_class = scope[f'Ui_{form_class}']
        base_class = getattr(QtWidgets, widget_class)

    return form_class, base_class
