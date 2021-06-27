import logging
import traceback

import pkg_resources
import tornado
from tornado.ioloop import IOLoop
from tornado.web import Application

from char_sheets import ui_methods
from char_sheets.config import load_config

logger = logging.getLogger(__name__)
PORT = 7554


def make_head(subtitle=None, char=None):
    if subtitle:
        subtitle = ' - ' + subtitle
    else:
        subtitle = ''
    return {
        'title': "Para's Characters" + subtitle,
        'description': char['short_description'] if char else "An index of Parakoopa's TTRPG characters",
        'og_title': subtitle if subtitle else "Para's Characters",
        'og_site_name': "Para's Characters",
        'og_image': char.spec('general')['images'][0] if char else '/static/android-icon-192x192.png'
    }


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


routes = [
    (r"/", ListHandler),
    (r"/character/(?P<character_id>[^\/]+)/?", CharacterHandler),
]
logger.info('Starting!')

app = Application(routes,
                  template_path=pkg_resources.resource_filename(__name__, 'web/views'),
                  static_path=pkg_resources.resource_filename(__name__, 'web/static'),
                  debug=True, ui_methods=ui_methods)
app.listen(PORT)
IOLoop.current().start()
