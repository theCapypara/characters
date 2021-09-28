from abc import ABC, abstractmethod
from collections import Callable
from tempfile import SpooledTemporaryFile
from typing import Union

import pdfrw

from char_sheets.config.character import Character

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'


class AbstractPdfTemplate(ABC):
    def __init__(self, character: Character):
        self.character = character

    @abstractmethod
    def process(self) -> bytes:
        pass


def process_pdf_form_fields(template_path: str, process_fn: Callable[[str], Union[str, bool, None]]) -> bytes:
    template_pdf = pdfrw.PdfReader(template_path)
    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    val = process_fn(key.strip())
                    if val is not None:
                        if type(val) == bool:
                            if val is True:
                                annotation.update(pdfrw.PdfDict(AS=pdfrw.PdfName('Yes')))
                        else:
                            annotation.update(
                                pdfrw.PdfDict(V='{}'.format(val))
                            )
                            annotation.update(pdfrw.PdfDict(AP=''))
    with SpooledTemporaryFile() as b:
        template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        pdfrw.PdfWriter().write(b, template_pdf)
        b.seek(0)
        return b.read()


def pdf_get(obj, f1, f2=None):
    if f1 not in obj:
        return '-'
    if f2 is not None:
        if f2 not in obj[f1]:
            return '-'
        return obj[f1][f2]
    return obj[f1]
