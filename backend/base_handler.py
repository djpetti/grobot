import logging

import tornado.web


logger = logging.getLogger(__name__)


class BaseHandler(tornado.web.RequestHandler):
  """ Default handler. All other handlers can subclass from this one. """

  def get(self, template):
    """ This is a default GET implementation that renders the requested template
    without any arguments. Ex: If the user requests /main, it will serve
    main.html from the templates directory.
    Args:
      template: The path that the request was made with. """
    # Add a .html suffix if we need to.
    if not template.endswith(".html"):
      template += ".html"
    logger.debug("Serving HTML: %s" % (template))

    self.render(template)
