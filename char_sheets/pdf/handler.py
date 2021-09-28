# noinspection PyAbstractClass
import logging
import traceback
from typing import Type, Dict

import tornado

from char_sheets.config import load_config
from char_sheets.pdf.template.abstract import AbstractPdfTemplate
from char_sheets.pdf.template.dnd import DndPdfTemplate
from char_sheets.util import make_head

logger = logging.getLogger(__name__)

PDF_HANDLERS: Dict[str, Type[AbstractPdfTemplate]] = {
    'dnd': DndPdfTemplate
}


class CharacterPdfHandler(tornado.web.RequestHandler):
    async def get(self, character_id, *args, **kwargs):
        try:
            char = load_config().get(character_id)
            if char and 'pdf_template' in char:
                if char['pdf_template'] in PDF_HANDLERS:
                    data = PDF_HANDLERS[char['pdf_template']](char).process()
                    self.set_header("Content-Type", 'application/pdf; charset="utf-8"')
                    self.set_header("Content-Disposition", f"attachment; filename={character_id}.pdf")
                    self.write(data)
            else:
                self.set_status(404)
                await self.render("not_found.html", head=make_head())
        except Exception as err:
            self.set_status(500)
            logger.exception(err)
            await self.render("error.html", head=make_head("Error"),
                              trace=traceback.format_exc(), err=err)
