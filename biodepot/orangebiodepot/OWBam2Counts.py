import os
import Orange.data
from Orange.data.io import FileFormat
from orangebiodepot.util.BwBase import OWBwBWidget
from Orange.widgets import gui


class OWBam2Counts(OWBwBWidget):
    name = "BAM to Counts Table"
    description = "Counts BAM files"
    category = "General"
    icon = "icons/bam2counts.svg"

    priority = 10

    inputs = [("GTF file", str, "setGtfFile"),
              ("BAM files", str, "setBamFiles")]

    outputs = [("Counts", str), ("DataTable", Orange.data.Table)]

    want_main_area = False

    docker_image_name = 'biodepot/bam2deseq'
    docker_image_tag = 'latest'

    # worker numbers
    worker_numbers = 2

    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)

        # GUI
        box = gui.widgetBox(self.controlArea, "Info")
        self.lblGtf = gui.widgetLabel(box, 'GTF File: Not Set')
        self.lblBamfiles = gui.widgetLabel(box, 'BAM files: Not Set')

        self.infoLabel = gui.widgetLabel(box, 'Waiting...')
        self.infoLabel.setWordWrap(True)

        self.auto_run = False
        gui.checkBox(self.controlArea, self, 'auto_run', 'Run automatically when input set')
        self.btnRun = gui.button(self.controlArea, self, "Run", callback=self.OnRunClicked)
        self.Flag_isRunning = False

        self.Initialize_InputKeys(['gtf', 'bamfiles'])

        self.setMinimumSize(500, 180)

    def OnRunClicked(self):
        self.startJob(triggerdByButton=True)

    def setGtfFile(self, path):
        self.setDirectories('gtf', path, self.lblGtf)
        self.startJob()

    def setBamFiles(self, path):
        self.setDirectories('bamfiles', path, self.lblBamfiles)
        self.startJob()

    def startJob(self, triggerdByButton=False):
        all_set = all(value is not None for value in [self.getDirectory('gtf'), self.getDirectory('bamfiles')])

        if all_set and (self.auto_run or triggerdByButton):
            self.btnRun.setEnabled(False)
            top_dir = '/data'
            gtf = os.path.join(top_dir, os.path.basename(self.getDirectory('gtf')))
            bamfiles = os.path.join(top_dir, 'bamfiles')
            logfile = os.path.join(bamfiles, 'log.txt')

            volumes = {gtf : self.getDirectory('gtf'),
                       bamfiles : self.getDirectory('bamfiles')}

            cmd = 'Rscript /home/root/bam2counts.R {} {} {} >& {}'.format(gtf, bamfiles, self.worker_numbers, logfile)
            commands = [cmd, "exit"]

            self.dockerRun(volumes, commands)

    def Event_OnRunFinished(self):
        self.btnRun.setEnabled(True)
        tsvFile = os.path.join(self.getDirectory('bamfiles'), 'bamcounts.csv');
        self.send('Counts', tsvFile)
        tsvReader = FileFormat.get_reader(tsvFile)
        data = None
        try:
            data = tsvReader.read()
        except Exception as ex:
            print(ex)
        self.send("DataTable", data)

    def Event_OnRunMessage(self, message):
        self.infoLabel.setText(message)
