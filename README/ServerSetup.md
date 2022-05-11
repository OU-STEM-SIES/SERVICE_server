# SERVICE

There are two primary ways to set up the server code.

##### 1. Download and run directly on your computer.

This is what you'll want to do if you're just exploring the code and experimenting with it. It should run unmodified on most Mac or Linux setups, but it may require some modifications to run under Windows.

##### 2. Install into a Docker/Kubernetes image, and run in a container.

This is how you'd set up if you intend to actually use the server with incoming data from the corresponding mobile app, or some other data source.

## Setting up a server

First, you'll want to set up the server so it'll run on your desktop computer. If that's all you need, it's easy. But if you need to run the server in the open with client apps, you'll want to adjust the configuration and build a Docker image. Fortunately, the setup software will do all this for you in most cases.

These instructions are written for macOS and Linux. Windows users will need to either use a Linux VM of some description, or make some changes to the instructions and/or scripts. The code may not work on Windows unless several changes are made.

I recommend using a Python virtual environment (venv). This keeps all the modules and requirements that the SERVICE server needs in a self-contained area where they can be maintained, updated, or even cleanly removed without affecting any other Python projects. 

## Getting Started

### Prerequisites

You will need a working installation of Python 3, preferably 3.10 or higher, which is current at the time of writing. It is expected that all future 3.x versions should remain compatible.

* [Python 3.10](https://www.python.org)  
You can get this from the [Python website](https://www.python.org). Please follow its installation instructions. Windows users, note that there's a version of Python 3 on the Microsoft Store, but that version is *not* sufficient to run this system. Please use the version from the [Python website](https://www.python.org).

* [SQLite3](https://www.sqlite.org/index.html)  
You'll also need [SQLite3](https://www.sqlite.org/index.html) installed. The version preinstalled on macOS is sufficient, and many Linux distros already have this available, but if yours doesn't, you can download and install by following the instructions on the [SQLite3 website](https://www.sqlite.org/index.html).

* make (optional)  
In rare cases, you might also need the 'make' command-line utility installed. Most uses of this have been superseded by the SETUP scripts, but occasional uses remain. This command is normally preinstalled on most Linux systems. Mac users will need to install the XCode command-line tools as follows:

  1. Open 'Terminal' (located in Applications/Utilities)
  2. In the terminal window, run the command  
`xcode-select --install`.  
  
  4. In the window that pops up, click `Install`, and agree to the Terms of Service.
  5. Once the installation is complete, the command line utilities should be set up properly, although they may only be available to new Terminal windows, so you might need to close and reopen your Terminal.

You'll also need a basic familiarity with the shell - the command line interface to your computer, accessed via the Terminal utility on a Mac, or usually via a Shell icon on Linux GUIs. If you're not using a Graphical User Interface (GUI) on Linux, you're probably already using the shell!

### Installation

Clone the server code repository to your computer as described in the [instructions for cloning a git repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository). Download the SERVICE server code into a working directory of your choosing. Unpack it, if necessary, so that you can see the "README" directory (which contains this file), the "SETUP" directory, and several other files. We'll refer to the directory containing these files as the project's root directory.

### First-time setup

1. Open a shell
2. To go into the SETUP directory, type

`cd SETUP`

3. To launch the setup script, type

`./setup.sh`

The setup script will examine your installation, and you may see a message saying *"Performing first-time setup of SERVICE environment."*. This once-only process will create a Python virtual environment, and install the Python modules required by the SERVICE server in it. This takes a few minutes, depending on the speed of your internet connection.

Once the environment is set up, or if this is not your first time running the setup script (and the environment was set up previously), the setup menu will appear:

```
Initial checks complete. Proceeding with configuration.

> Configure a new SERVICE installation for the first time
  Import additional users from CSV files
  Generate example (fake) Linkworkers, PACs, supporters, moods, and wellbeing data
  Run a local server (without Docker)
  Build a Docker image from your current working installation
  Start a new Docker container based on the image built using the above option
  Quit
```
The first option must be run before anything else will work, but unless you plan a major reconfiguration, it only needs to run once. Use the cursor up and down keys to highlight the first option (it's probably already highlighted) and press enter to select it.

You'll need to answer a few essential questions about how you want the server to work.

1. You'll be asked about DEBUG mode. DEBUG mode is useful if you're going to modify the program code, because it will give you informative error messages and feedback. However, you shouldn't use DEBUG mode on the open internet, because its error messages can reveal sensitive information about your server. Unless you already know you need DEBUG mode, just hit return to leave it off.
2. You'll be asked for a Django secret key. This option is here in case you need to use a specific secret key, but don't worry - if don't already have a preferred one, you can just hit return and the script will generate one for you.
3. You'll be asked about the ALLOWED_HOSTS value. If you're not using a domain name, or don't know, just hit return, and the setup script will use a generic value for now. This is only necessary if you're using a custom domain name to run your server on the internet, in which case it should contain a comma-separated list of hostnames, such as

```
www.myserver.org.uk, myserver.org.uk, service.myserver.org.uk
```


4. You'll be asked for a superuser's credentials. This is to create a master user of the SERVICE server who has access to everything. In sequence, this will ask for the superuser's...
   1. first name (if uncertain, use your own)
   2. last name (if uncertain, use your own)
   3. username (a default will be suggested, and you can just hit return if you don't wish to change it)
   4. email address (if uncertain, use your own)
   5. password for this user on this system (this should be unique)
   6. password again, for verification.
5. Finally, the server's email setup. When a user needs to do something like reset a forgotten password, the system will try to send an email with a password reset link to the user. You can choose how the server should handle this.
   1. If you're just running the server for yourself, on your own desktop, you can choose to just save outgoing messages as text files on your computer. They'll appear in a folder called "sent_emails", but won't actually go anywhere beyond your computer. This is the simplest option.
   2. If you're planning on using a real mail server, but don't have it ready yet, you can have the server use a special Python SMTP debugging server. This will verify that SMTP outgoing email should work, but the message contents will just be sent to the command prompt where the server is running, and won't actually leave your computer.
   3. Finally, if you're ready to use a real SMTP server for real outgoing email messages, select the third option, and you'll be asked for the necessary details:
      1. the FROM address, from which all outgoing emails will come (and to which any replies will go),
      2. the SMTP server's IP address or hostname,
      3. Whether or not TLS encryption can be used (if possible, do use it),
      4. The port number to use for the server (a likely default will be preselected based on your answer to the previous question)
      5. an account username for the SMTP server (optional)
      6. an account password for the SMTP server (optional)
6. Finally, you'll see a summary of your choices, and a message saying

```
Ready to configure. Enter YES to proceed, or anything else to abort.
```
If you're happy with what you've entered, type "YES" and hit return to configure the server. You'll get a message saying that a file called "settings.py" already exists, and asking you to enter "YES" to overwrite it, which you should. This takes only a few seconds. If all goes well, you'll see a message saying:

```
Minimal installation completed. Your server should now be able to run.
```

The server should now work with its default settings. If you need to tweak the configuration, edit the file "covid_stretch/settings.py", with reference to the Django documentation.

## Running the server locally

#### Either (if you prefer the guided option):
From a shell in the `root\SETUP` directory, type 
```
./setup.sh
```
and the setup menu will appear. Select
```
Run a local server (without Docker)
```

#### Or (if you prefer manual control or need to change port):

From a shell in the root/covid_stretch directory, type

```
python3 manage.py runserver
```
for the default port (8000), or 
```
python3 manage.py runserver 0.0.0.0:8080
```
...replacing 8080 with the port you need. Note that ports below 1024 require root privileges or sudo.

#### Or (if you have 'make' installed):

From a shell in the root/covid_stretch directory, type

```
make run
```


#### Then...
 You should see a short status message from Django, like this:
 
```
(venv) √ covid-stretch/covid_stretch % make run                                                                          16:40:06
python3 manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
February 14, 2022 - 16:40:10
Django version 3.2.10, using settings 'covid_stretch.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
Click on the URL in the status message ([http://127.0.0.1:8000](http://127.0.0.1:8000) in the example above) to open the web dashboard. It may take several seconds until the web server actually responds, but when it does, you should see a login page. You can now log in with any superuser or researcher account, as these accounts can see data from other users. Superusers, can also access the underlying Django admin control panel, at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin), but this shouldn't often be necessary as the setup script does all the normal maintenance tasks.

## Building an image, and launching a container
A full explanation of Docker, Kubernetes, and so on is beyond the scope of this document. However, the setup script contains working example code to build a Docker image based on your server, and to create and run a container from that image. If the server is correctly set up for the target environment (Docker, or a Kubernetes cluster) it should work as well as it did locally.

You'll need Docker Desktop (on macOS or Windows) or the Docker daemon (Linux) running in order for those commands to work.

There are additional build scripts for a preconfigured image of an nginx-based reverse proxy server in the SETUP/nginx-image-build subdirectory. This should be added to the Kubernetes pod as a sidecar if you're uploading to a cluster. The nginx.conf file can be mounted via a persistent storage area or a config map.

[Back to README.md](README.md)

Next: [Setting up user accounts](UserSetup.md)
