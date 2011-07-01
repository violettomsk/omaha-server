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

from twisted.web import resource
from config import Config
from new_full import NewFullResource
from new_delta import NewDeltaResource
from switch import SwitchResource

from util import *

class UpdateManager(resource.Resource):
    isLeaf = False
    pathFromRoot = '/service/admin'

    def __init__(self):
        resource.Resource.__init__(self)
        self.newFull = NewFullResource()
        self.putChild('new_full', self.newFull)
        self.newDelta = NewDeltaResource()
        self.putChild('new_delta', self.newDelta)
        self.switch = SwitchResource()
        self.putChild('switch', self.switch)
        self.putChild('', self)

    def render_GET(self, request):
        mainDict = loadJsonAndCheckIfLatestKeyExists(Config.bitpopUpdateInfoFile)
        bitpopInfo = mainDict['jsonData']
        latestExists = mainDict['latestExists']

        output = """<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="chrome=1">

    <title>House of Life Update Manager</title>

    <!-- CSS: implied media="all" -->
    <link rel="stylesheet" href="/css/style.css?v=2">
</head>
<body>
    <div id="container">
        <header>
            <h1>House of Life Update Manager</h1>
        </header>
        <div id="main" role="main">"""

        output += """
            <h2>BitPop</h2>"""
        if not latestExists:
            output += """
            <p>There are no BitPop updates available.</p>"""
        else:
            output += """
            <p>Latest BitPop version: {0}</p>""".format(bitpopInfo["latest"])
            output += """
            <h3>Update files</h3>
            <ul>
                <li><a href="{0}">full update v{1}</a></li>""".format(getUpdateURL(bitpopInfo['latest']),
                                                                      bitpopInfo['latest'])
            if bitpopInfo.has_key('delta') and type(bitpopInfo['delta']) == type([]):
                for deltaFromVersion in bitpopInfo['delta']:
                    output += """
                <li><a href="{0}">delta update from v{1}</a></li>""".format(
                        getUpdateURL(bitpopInfo['latest'], deltaFromVersion),
                        deltaFromVersion)
        output += """
            </ul>"""

        bitpopNewDict = loadJsonAndCheckIfLatestKeyExists(Config.bitpopNewUpdateInfoFile)
        bitpopNewInfo = bitpopNewDict['jsonData']
        bitpopNewLatestExists = bitpopNewDict['latestExists']

        if not bitpopNewLatestExists:
            output += """
            <p><a href="{0}">Add new full version installer</a></p>""".format(self.pathFromRoot + '/new_full')
        else:
            output += """
            <h3>Uploaded new version {0}</h3>""".format(bitpopNewInfo['latest'])
            if bitpopNewInfo.has_key('delta') and type(bitpopNewInfo['delta']) == type([]):
                output += """
                <ul>"""
                for newDeltaFrom in bitpopNewInfo['delta']:
                    output += """
                    <li>delta from {0}</li>""".format(newDeltaFrom)
                output += """
                </ul>"""
            output += """
            <p><a href="{0}">Add new delta update installer</a></p>
            <p><a href="{1}">Switch to new version ({2})</a></p>""".format(
                self.pathFromRoot + '/new_delta', self.pathFromRoot + '/switch', bitpopNewInfo['latest'])
        output += """
        </div>
        <footer>
        </footer>
    </div>
</body>
</html>"""
        return output
