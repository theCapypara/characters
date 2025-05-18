import logging
import traceback

import importlib.resources
import tornado
from tornado.ioloop import IOLoop
from tornado.web import Application

from char_sheets import ui_methods
from char_sheets.config import load_config
from char_sheets.pdf.handler import CharacterPdfHandler
from char_sheets.util import make_head

logger = logging.getLogger(__name__)
PORT = 7554


# noinspection PyAbstractClass
class ListHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        try:
            await self.render("list.html", head=make_head(), characters=load_config())
        except Exception as err:
            self.set_status(500)
            logger.exception(err)
            await self.render("error.html", head=make_head("Error"),
                              trace=traceback.format_exc(), err=err)


# noinspection PyAbstractClass
class CharacterHandler(tornado.web.RequestHandler):
    async def get(self, character_id, *args, **kwargs):
        try:
            char = load_config().get(character_id)
            if char:
                await self.render("char.html", head=make_head(char['full_name'], char), char=char)
            else:
                self.set_status(404)
                await self.render("not_found.html", head=make_head())
        except Exception as err:
            self.set_status(500)
            logger.exception(err)
            await self.render("error.html", head=make_head("Error"),
                              trace=traceback.format_exc(), err=err)


def main():
    routes = [
        (r"/", ListHandler),
        (r"/character/(?P<character_id>[^\/]+).pdf", CharacterPdfHandler),
        (r"/character/(?P<character_id>[^\/]+)/?", CharacterHandler),
    ]
    logger.info('Starting!')

    app = Application(routes,
                    template_path=importlib.resources.files(__name__) / 'web/views',
                    static_path=importlib.resources.files(__name__) / 'web/static',
                    debug=True, ui_methods=ui_methods)
    app.listen(PORT)
    IOLoop.current().start()


if __name__ == '__main__':
    main()