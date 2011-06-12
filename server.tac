#   Copyright (C) 2011 Crystalnix <vgachkaylo@crystalnix.com>

#   This file is part of omaha-server.

#   omaha-server is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   omaha-server is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with omaha-server.  If not, see <http://www.gnu.org/licenses/>.

from twisted.application import service, internet
from twisted.web import server, resource
from twisted.web.static import File
from chained_ssl import ChainedOpenSSLContextFactory
from update import UpdateXMLProcessor
from config import Config
from twisted.web.script import ResourceScriptWrapper
import os

if not os.path.exists(Config.bitpopDirectory):
    os.mkdir(Config.bitpopDirectory, 0755)
if not os.path.isdir(Config.bitpopDirectory):
    os.remove(Config.bitpopDirectory)
    os.mkdir(Config.bitpopDirectory, 0755)
    
root = resource.ForbiddenResource()
err = resource.ForbiddenResource()
root.putChild("service", err)
upd = UpdateXMLProcessor()
err.putChild("update2", upd)
admin = ResourceScriptWrapper('auth.rpy')
err.putChild('admin', admin)

css = resource.ForbiddenResource()
css.putChild('style.css', File('css/style.css'))
css.putChild('upload.css', File('css/upload.css'))
root.putChild('css', css)

js = resource.ForbiddenResource()
js.putChild('upload.js', File('js/upload.js'))
root.putChild('js', js)

insecureDomainResource = resource.ForbiddenResource()
bitpopDir = File(Config.bitpopDirectory)
insecureDomainResource.putChild(Config.bitpopDirectory, bitpopDir)
insecErr = resource.ForbiddenResource()
insecureDomainResource.putChild("service", insecErr)
insecUpd = UpdateXMLProcessor()
insecErr.putChild("update2", insecUpd)

httpSite = server.Site(insecureDomainResource)
httpsSite = server.Site(root)

application = service.Application('House of Life Update Portal')
application.management = ResourceScriptWrapper('admin.py')
httpService = internet.TCPServer(80, httpSite, interface=Config.domainName)
httpsService = internet.SSLServer(443, httpsSite, ChainedOpenSSLContextFactory(
                                      privateKeyFileName="cert/privkey.pem",
                                      certificateChainFileName="cert/server_chain.pem"),
                                  interface=Config.domainName)
httpService.setServiceParent(application)
httpsService.setServiceParent(application)