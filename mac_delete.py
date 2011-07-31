from twisted.web import resource
from mac_db_helper import MacDbHelper
import re

class MacDeleteResource(resource.Resource):
  pathFromRoot = "/service/admin/mac/delete"
  isLeaf = True  
  
  def render_GET(self, request):
    tr = re.compile('.*/(\d*)$')
    m = re.match(tr, request.path)
    if len(m.groups()) == 0:
      request.setResponseCode(400) # Bad request
      return "Error: Bad request."
    update_id = m.groups()[0]
    
    macdb = MacDbHelper()
    upd = macdb.delete(int(update_id))
    macdb.cleanup()
        
    return """<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="refresh" content="3;url=/service/admin">
  <title>Release notes changed</title>
</head>
<body>
  <h1>Success</h1>
  <p>Record has been deleted successfully. You will be redirected in 3 seconds.</p>
</body>
</html>
"""