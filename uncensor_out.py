from twisted.web import resource
from mac_db_helper import MacDbHelper
from config import Config
import json

class UncensorOutResource(resource.Resource):
  isLeaf = True
  pathFromRoot = '/service/uncensor_domains'

  def render_GET(self, request):
    macdb = MacDbHelper()
    res = macdb.uncensor_fetch_all()
    macdb.cleanup()
    
    request.setHeader('Content-Type', 'application/json')
    
    return json.dumps(res)