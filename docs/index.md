# BioDepot-Workflow-builder (Bwb)
# MANUAL

![](images/image19.png) ![](images/image23.png) 
   


Bioinformatics Group
University of Washington Tacoma

## GENERAL INFORMATION

The BioDepot-workflow-builder (Bwb) can be used to build bioinformatics workflows by combining  interchangeable and encapsulated widgets, allowing researchers to easily implement and test new algorithms and observe how the outputs differ. Widgets call  Docker containers to execute software tools that could potentially be written in a different programming language, require different system configurations and/or developed by different research groups.


Docker Image	: [https://hub.docker.com/r/biodepot/bwb/](https://hub.docker.com/r/biodepot/bwb/)

Source code	: [https://github.com/BioDepot/BioDepot-workflow-builder](https://github.com/BioDepot/BioDepot-workflow-builder)

Demo video	: [https://youtu.be/VY1peA4ITog](https://youtu.be/VY1peA4ITog) 
.
### Overview: Running Bwb
<div class="lower_alpha"></div>1\. Install Docker
2\. Start the container with Bwb by executing the following Docker command by typing into a window (Linux) or on the Docker command line (Windows/macOs)
```bash 
    docker run --rm   -p 6080:6080 \
    -v  ~/Desktop/:/data  \
    -v  /var/run/docker.sock:/var/run/docker.sock \
    biodepot/bwb
```
3\. Open a browser and connect to the Bwb container by typing the following url in the address bar of your browser. In Linux the url is:

   [http://localhost:6080](http://localhost:6080)    

For cloud instances and remote servers use the ip of the instance or remote server instead of localhost.

For Windows and Macs the url is [http://192.168.99.100:6080](http://192.168.99.100:6080) 

For Windows and Macs the IP may vary depending on your setup - instructions are [here](#findip) to find it)

4\. To quit the container, right click inside the browser and choose the QUIT container option. Alternatively, you can also stop it by finding the container id and stopping the container. Quitting the browser just closes the viewport to the container - it does not stop the container.




## Installing and starting Docker

### Linux
<a name="DockerInstall"></a>
1\. Update your package manager index. 

On Debian based distros such as Ubuntu the package manager is apt-get
```bash
sudo apt-get -y update
```
On Redhat based distros such as Fedora/Centos the package manager is dnf or yum  on older systems
```bash
sudo dnf -y update
```
2\. Install Docker.
    Ubuntu;
```bash
sudo apt-get -y install docker-engine
```
Fedora/Centos:
```bash
sudo dnf -y install docker
```
3\.  Start the Docker daemon.
```bash
sudo service docker start
```
4\.  Verify docker is installed correctly.
```bash
sudo docker run hello-world
```

The last command downloads a test image and runs it in a container. When the container runs, it prints an informational message. Then, it exits

For more information please refer to -     

[https://docs.docker.com/engine/installation/linux/ubuntulinux/](https://docs.docker.com/engine/installation/)


### macOS

1\. Download the Docker package -  [Docker for Mac](https://download.docker.com/mac/stable/Docker.dmg)
2\. To install Docker: double-click Docker.dmg to open the installer, then drag Moby the whale to the Applications folder.		

![](images/image1.png) 

3\. To start Docker: double-click Docker.app in the Applications folder. (In the example below, the Applications folder is in "grid" view mode.)

![](images/image13.png)     

You will be asked to authorize Docker.app with your system password after you launch it. Privileged access is needed to install networking components and links to the Docker apps.The whale in the top status bar indicates that Docker is running, and accessible from a terminal.

![](images/image16.png) 


### Windows

1\. To install Docker,

 * download to the package - [Docker for Windows](https://download.docker.com/win/stable/Docker%20for%20Windows%20Installer.exe)   
 * go to folder where the installation file (Installer.exe) is saved and run (double-click) the installation file. 
 * click the installer link to download.
 * follow the install wizard to accept the license, authorize the installer, and proceed with the install.
 * when it completes, the installer reports it was successful:
 * click the finish button to complete the installation. 
![](images/image21.png) 

2\.  To start Docker,
* search for Docker, select the app in the search results, and click it (or hit Return).
![](images/image11.png) 
* when the whale in the status bar stays steady, Docker is up-and-running, and accessible from any terminal window.
![](images/image20.png) 


* if the whale is hidden in the Notifications area, click the up arrow on the taskbar to show it. To learn more, see [Docker Settings](https://docs.docker.com/docker-for-windows/#docker-settings).
* If you just installed the app, you also get a popup success message with suggested next steps, and a link to this documentation. 
![](images/image15.png) 


### On The Cloud

On the cloud, BwB can also be run on any cloud instance. Please refer to the Linux and Windows instructions to install Docker on the cloud instance.


#### Amazon AWS

1\.  Login to your console and create a new EC2 instance of ubuntu (Here we are using ubuntu you can choose operating system of your choice)

2\.  Select the configuration and click on "Review and Launch"

3\.  You will be prompted to associate a ssh key pair with the instance, you can use an existing key pair or create a new one. The key will be downloaded onto the computer  which will be later used to ssh into the machine.
![](images/image9.png) 

4\.  Once the instance is running select your instance and scroll right for security groups.

5\.  From "Actions" button select "Edit inbound rules" 

![](images/image5.png) 

6\.  Add a new http rule for port 6080 to access the GUI from the container

![](images/image10.png) 

7\.  Copy the public dns of the instance 

![](images/image22.png) 

8\.  SSH into the instance by typing the following command into the terminal. 
(Type the commands in the directory where the ssh key of AWS instance was downloaded)
```bash
 #(demo.pem is name of the key)
 chmod 400 demo.pem 	`
 ssh -i demo.pem ubuntu@public-dns-of-aws-instance
```
9\.  After you are logged use the instructions [here](#DockerInstall) to install Docker on Linux.

10\. Configure the firewall using the instructions here [http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/authorizing-access-to-an-instance.html](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/authorizing-access-to-an-instance.html) 


## Starting Bwb

After you have installed Docker on your machine, you are now ready to start your Bwb session to create and execute Docker container workflows. Bwb comes inside its own Docker container so it is first necessary to launch Docker as shown in the previous sections depending on which platform is being used.

Then run the following commands on command prompt / terminal. 
1\.  Download the docker image containing Bwb. 

```bash
docker pull biodepot/bwb:latest
```
![](images/image2.png) 
    
2\.  Start the Bwb container 

```bash
docker run --rm -p 6080:6080 -v ${PWD}:/data -v /var/run/docker.sock:/var/run/docker.sock biodepot/bwb
```

This command will launch a mini-webserver and start a windowing environment inside the container. The Bwb application is automatically launched upon running the container and appears as a maximized window on the Desktop inside the container. In the above command we have set the port to be 6080 and the current directory is mapped to the /data directory inside the container. However, all this is hidden from view until the user connects to the container using a browser. 

To access the container open up a browser window and type in the IP of the container and port that it is listening to into the address bar. For a local installation using Linux, the IP of the container is localhost or 127.0.0.1 so the user would type localhost:6080 into the address bar of the browser. For a remote installation, the ip is the ip of the server.
<a name="findip"></a>
For Macs and Windows machines the local ip is usually [192:168:99:100](http://192:168:99:100:6080) but if that does not work you can find the IP with the following command in a terminal if using Linux/MacOS or in the Docker window if using Windows.

```bash
docker ps
```

More information about finding Docker IP is available here: [https://docs.docker.com/machine/reference/ip](https://docs.docker.com/machine/reference/ip/)

Once connected. A window similar to Figure 1 should appear showing a maximized Bwb window. The interface is a standard windowing one implemented using fluxbox. The icons in the upper right hand corner are used to iconify (hide), minimize/maximize and close the window. Clicking on the area taskbar at the bottom can be used to toggle between windows or hide/show them. In the Bwb window itself is a large drawing canvas. Right-clicking on the canvas brings up the tool menu which has a list of all the available widgets. Widgets can also be dragged onto the canvas from the toolbox on the left. Bwb starts with the Bwb widget toolbox section open. The original Orange ML widgets for machine learning are also available. The different toolbox sections can be opened by clicking on the toolbox banner. 

Note that the Bwb windowing system is inside the browser window. You still have access to whatever windowing system you are using on your host machine. If your browser closes or go to another url, nothing happens to Bwb - the browser merely provides a viewport to the Bwb container. Refreshing or reconnecting the browser to the container IP allows you to interact with Bwb again.

![ ](images/image4.png  "Figure 1: Maximized Bwb window")

Figure 1: Maximized Bwb window

![ ](images/image8.png  "Figure 2: Multiple Bwb windows on Desktop")

Figure 2:  Multiple Bwb windows on Desktop

If we hide/iconify the window by clicking on the taskbar or clicking on the iconify button in the upper right hand corner of the window, we see the Desktop itself as shown in figure 2. Right clicking on the Desktop brings up a menu of available applications and the option to QUIT the container. Unlike closing the browser window, this command will actually kill the webserver resulting in the container being stopped. The menu also gives the option of opening another Bwb instance or a terminal. Multiple applications can be launched at same time - and the user even has the option of using different workspaces (up to 4) to quickly cycle through different windows.

## WIDGETS 


### Using widgets


![ ](images/image12.png  "Figure 3: Different types of widgets")

Figure 3:  Different types of widgets

The widget is the main unit of the workflow. Available  widgets are available in the toolbox on the left hand side of the Bwb window. Widgets can specify input, output or software modules. Widgets are dragged from the toolbox onto the canvas and connected to indicate the flow of data. the output of a widget becomes the input of the next connected widget. In this way an analytical pipeline consisting of different modules can transform input data into the final output results.  Many of the software widgets utilize Docker containers that require docker engine. When widgets that are using Docker containers are used, the container will be automatically downloaded from DockerHub if it is not available locally.


### Detailed description of individual widgets


#### Custom container widget

This widget is designed to facilitate the task of importing existing scripts and executables into Bwb without writing a full widget. Three elements are specified, a container with the required executables and dependencies, a set of mount points that point to where the input and output files will reside, and a starting command, for example to run a script. The example below shows how this can be used to run an R script that converts bamfiles to counts. Python and Perl scripts can be run changing the container to one that has Python and/or Perl installed.  Stock containers for all the major scripting languages and packages such as Bioconductor are available on Docker Hub.

![ ](images/image7.png  "Custom container widget")
 
![ ](images/image17.png  "Custom container widget form")

#### Load CSV

This widget plays a role as bridge between CSV file and the [Data Table] widget of Orange. It widget support two kind of sources (channels): a CSV file or a directory. If the source is a directory, the widget will scan that folder and list all CSV or TSV files. The CSV or TSV file will be loaded when user select them or specify the particular file name.

![ ](images/image18.png  "Load CSV widget")

![ ](images/image14.png  "Load CSV inputs")


The above example showsthe output of _Bam to Counts connected_ to the Directory of _Load Counts Table_. Once the procedure Bam to Counts finished, it will send <code><em>/data/bamfiles</em></code> to [Load CSV] widget, the [Load CSV] widget will scan this folder list all *.csv or *.tsv files.


## WIDGET DEVELOPMENT GUIDE


### 1. Development environment

We provide additional tools in a the biodepot/bwb-widget-dev for development of widgets. This includes a full-fledged editor, geany, some graphics tools for making icons and firefox for cutting pasting from stack overflow and other resources and for editing json files inside the container.

### Bwb widget development

#### Introduction
A widget consists of a python script that defines the inputs/outputs, names, and supporting files such as icons along with the actual commands to be executed. In the case of Bwb, these are usually, docker commands that are accessed using the Python API (DockerPy).

Orange provides a very tutorial for developing a widget from scratch. [http://orange-development.readthedocs.io/tutorial.html](http://orange-development.readthedocs.io/tutorial.html)

#### Automated generation of widgets from json descriptor files
We have greatly simplified and automated the widget development process. The user provides the details of the executable or script, the inputs, outputs, flags and arguments in a json file. The createWidget scripit then creates the Python script and copies it to the correct location. The widget then appears on the next launch of the Bwb process which can be done without closing the container. This is made possible by refactoring and abstracting the code in a BwBase class.

The construction of a widget is reduced to editing a Json file. For more complicated widgets - the automatically produced python script can be customized and the defaults extended or overridden if desired The fields are described below.

There 3 steps to creating and sharing a widget:

1	Edit json file
2	Running createWidget tool to make widget
3	Save copy of biodepot file and rebuild container

The main step is creating or editing the json file which is given below:

#### Description of json descriptor 

The json file describes a dict structure in Python which will be read into the dict *data* in the widget python script.

There are 15 primary fields to the object

**'name' : **<*str*> -name of widget
**'category : **<*str*> -may be used in future to group widgets by function
**'icon' :** <*str*> -path of icon file to be used by bwb
**'priority' :**  <*int*>  -priority of widget
**'want_main_area' :** <*bool*> -use only if custom code needs second drawing area
**'docker_image_name' :** <*str*> - name of docker image to launch
**'docker_image_tag' :**  <*str*> tag of docker image e.g. latest
**'persistent_settings' :** <*str* or *list*> - 'all', 'none' or list of settings values that will be saved and restored upon launch
**'command' :** <*str*> the command that will be launched 
**'inputs'** : <*OrderedDict*> -attributes that can obtain values from other widgets
	\<*str*> attribute to be input : <*dict*>
		**'type' :**
			 
	callback            'inputs'   : OrderedDict([ ('indexFile', {'type':str, 'callback' : None}),
                                       ('fastqFiles',  {'type':str, 'callback' : None})
                                    ]),
            'outputs'  : OrderedDict([ ('outputDir', {'type':str})
                                    ]),
            'volumeMappings' : [{'conVolume':'/root/output','attr':'outputDir','default':'/data/output'},
                                {'conVolume':'/root/fastq' , 'attr':'fastqFiles'},
                                {'conVolume':'/root/reference', 'attr':'indexFile','default':'/data/reference'}
                               ],
            'requiredParameters' : ['outputDir','indexFile','fastqFiles'],
            'parameters': OrderedDict([('outputDir',{'flags':['-o','--output-dir='], 'label':'Output directory', 'type': "directory"}),
                                       ('indexFile',{'flags':['-i','--index='], 'label':'Index file', 'type':'file'}),
                                       ('fastqFiles' ,{'flags':[],'label':'fastq files', 'type': "files",'filePattern':["*.fastq.*"]}),
                                       ('bias',     {'flags':['--bias'],'label':'Perform sequence based bias correction','type': 'binary'}),
                                       ('bootstrap',{'flags':['-b','--bootstrap-samples='],'label':'Number of bootstrap samples','type': 'int','default': 1}),
                                       ('seed',     {'flags':['--seed='],'label':'Seed for bootstrap sampling','type': 'int','gui':'Ledit', 'default' : 42}),
                                       ('plaintext',{'flags':['--plaintext'],'label':'Output plaintext instead of HDF5','type': 'bool', 'default' : False}),                                         
                                       ('fusion',   {'flags':['--fusion'],'label':'Search for fusion genes','type': 'bool', 'default' : False}),
                                       ('single',   {'flags':['--single'],'label':'Quantify single-end reads','type': 'bool', 'default' : False}),    
                                       ('single_overhang',   {'flags':['--single-overhang'],'label':'Include reads that go beyond transcript start','type': 'bool', 'default' : False}),                                       
                                       ('fr_stranded',   {'flags':['--fr-stranded'],'label':'strand specific read - first read forward','type': 'bool', 'default' : False}),
                                       ('rf_stranded',   {'flags':['--rf-stranded'],'label':'strand specific read - first read reverse','type': 'bool', 'default' : False}),
                                       ('fragment_length',   {'flags':['-l','--fragment-length'],'label':'Estimated fragment length','type': 'double', 'default' : None}),
                                       ('stdev',    {'flags':['-s','--sd'],'label':'Standard deviation of fragment length','type': 'double', 'default' : None}),
                                       ('nThreads' ,{'flags':['-t','--threads='],'label':'Number of threads','type': 'int','default':1}),
                                       ('pseudoBam',{'flags':['--pseudobam'],'label':'Save alignments to BAM file','type': 'bool','default':False}),                                                                            
                                       ('genomeBam',{'flags':['--genomebam'],'label':'Project alignments to sorted BAM file','type': 'bool','default':False}),
                                       ('gtf' ,{'flags':['--gtf'],'label':'GTF file', 'type': "file"}),                                                                                
                                       ('chromosomes' ,{'flags':['-c','--chromosomes'],'label':'Chromosome file', 'type': "file"})
                           ]
                          )
        }


![ ](images/image3.png  "BwBase class")

There is considerable boilerplate code in developing a containerized widget. To minimize the amount of repetitive code that needs to be written, we provide the BwBase class. The schema for an instance of this class is shown above for a widget connected the OWBam2Counts widget. BwBase handles tasks related to calling the Docker API, such as pulling an image and starting a container. It also takes care of the directories when connected with other widgets (in the example above, the OWBam2Counts widget). 

The key individual components of the class are:

#### Event_OnRunMessage:

Triggered by BwBase to indicate the status of docker container, for now, the possible values are: Running and Finished.

#### Event_OnRunFinished:

Triggered when the docker container was exited. 

#### dockerRun(self, volumes = None, commands = None, environments = None)

    volumes: dictionary that define the mapping between host and container

    commands: list of commands, e.g. ["echo hello", "exit"]

    environments: dictionary of environments variables.

#### setDirectories(self, key, path, ctrlLabel = None)

    Store the path of directories.

    key: the name of this path.

    path: real full path.

    ctrlLabel: optional, used to display the path on label.

#### getDirectory(self, key)

    return the stored path by name.

A Hello world example as following:

![ ](images/image6.png  "BwBase class: Hello World")

