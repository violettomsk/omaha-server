from twisted.web import resource
from mac_db_helper import MacDbHelper
from config import Config
import json
from twisted.web.client import getPage
from twisted.web import server
import pycountry


class UncensorPOutResource(resource.Resource):
  isLeaf = True
  pathFromRoot = '/service/uncensorp_domains'

  def render_GET(self, request):
    d = getPage('http://api.hostip.info/country.php?ip=' + request.getHeader('x-forwarded-for'))
    d.addCallback(self.output_json, request)
    d.addErrback(self.errback, request)
    return server.NOT_DONE_YET

  def output_json(self, value, request):
    macdb = MacDbHelper()
    res = macdb.uncensorp_fetch_by_iso(value)
    res = { 'domains': [rec['domain'] for rec in res], 'country_code': value,
            'country_name': pycountry.countries.get(alpha2=value).name.encode('utf-8') }
    macdb.cleanup()

    request.setHeader('Content-Type', 'application/json')

    request.write(json.dumps(res))
    request.finish()

  def errback(self, error, request):
    request.write('Error occurred: %s' % (error))
    request.finish()