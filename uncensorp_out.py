from twisted.web import resource
from mac_db_helper import MacDbHelper
from config import Config
import json
from twisted.web.client import getPage
from twisted.web import server


class UncensorPOutResource(resource.Resource):
  isLeaf = True
  pathFromRoot = '/service/uncensorp_domains'

  def render_GET(self, request):
    d = getPage('http://api.hostip.info/country.php?ip=' + request.getClientIP())
    d.addCallback(self.output_json, request)
    d.addErrback(self.errback, request)
    return server.NOT_DONE_YET

  def output_json(self, value, request):
    macdb = MacDbHelper()
    res = macdb.uncensorp_fetch_by_iso(value)
    macdb.cleanup()

    request.setHeader('Content-Type', 'application/json')

    request.write(json.dumps(res))
    request.finish()

  def errback(self, error, request):
    request.write('Error occurred: %s' % (error))
    request.finish()