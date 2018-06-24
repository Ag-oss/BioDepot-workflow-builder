import os
import glob
import sys
import functools
import jsonpickle
from collections import OrderedDict
from Orange.widgets import widget, gui, settings
import Orange.data
from Orange.data.io import FileFormat
from orangebiodepot.util.DockerClient import DockerClient
from orangebiodepot.util.BwBase import OWBwBWidget, ConnectionDict, BwbGuiElements
from PyQt5 import QtWidgets, QtGui

class OWDtoxSAlignment(OWBwBWidget):
    name = "DtoxSAlignment"
    description = "Alignment part of DetoxS standard operating procedure (SOP)"
    category = "RNA-Seq"
    priority = 10
    icon = "/biodepot/orangebiodepot/icons/dtoxs-alignment2.svg"
    want_main_area = False
    docker_image_name = "biodepot/dtoxs_alignment"
    docker_image_tag = "alpine-bwa-python-3.7-0.7.15-r1140-2.7.14-1.0"
    inputs = [("barcodesFile",str,"handleInputsbarcodesFile"),("topDir",str,"handleInputstopDir"),("trigger",str,"handleInputstrigger")]
    outputs = [("topDir",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    topDir=pset(None)
    barcodesFile=pset("barcodes_trugrade_96_set4.dat")
    lanes=pset(6)
    seriesName=pset("20150409")
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open("/biodepot/orangebiodepot/json/DtoxSAlignment.json") as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsbarcodesFile(self, value, sourceId=None):
        self.handleInputs(value, "barcodesFile", sourceId=None)
    def handleInputstopDir(self, value, sourceId=None):
        self.handleInputs(value, "topDir", sourceId=None)
    def handleInputstrigger(self, value, sourceId=None):
        self.handleInputs(value, "trigger", sourceId=None)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"topDir"):
            outputValue=getattr(self,"topDir")
        self.send("topDir", outputValue)
