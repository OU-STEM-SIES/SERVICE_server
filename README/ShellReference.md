# SERVICE

Nearly all the shell commands have been moved into a single setup script, which you can launch as follows:

1. Open a shell
2. To go into the SETUP directory, type

`cd SETUP`

3. To launch the setup script, type

`./setup.sh`

This script can be used for the initial configuration of your downloaded server, to get it in a running state, and it can also set up user accounts (real or fake) and help you build a server image if you need one.

I recommend reading about it in the "Setting up a server" section, before looking at the few remaining items below.

[Setting up a server](ServerSetup.md)

## Shell reference

This document contains a few shell commands relevant to the SERVICE server. Some of these commands are built into the Django framework, or are added by other requirements, but all are relevant to operation and/or maintenance of the server. 

In order to simplify management of the server, most of the regularly-used command sequences have been shortened into `make` scripts. Instead of a list of commands, one can just enter the appropriate `make` command and the appropriate steps will be taken for you. Only the essential scripts will be documented - other scripts are either self-explanatory, or are only there in order to be called by multiple other scripts.

<!--

---
### ```Name```
Description and function

###### Parameters
`Parameters`: Explanation

###### Requirements
Requirements explanation

###### Typical response
```bash
[Example response]
```

-->


## `make` scripts
- <a href="#MakeMM">make mm</a>
- <a href="#MakeM">make m</a>
- <a href="#MakeRun">make run</a>
- <a href="#MakeRunPublic">make runpublic</a>
---
<a name="MakeMM"></a>
### ```make mm```
This is a shorthand for the Django built-in `python manage.py makemigrations` command, which should be executed whenever any database schema changes have been made. It prepares comparison notes ready to bring the database design up to date with changes to the Python/Django database description code. You'll only need this if you modify the schema.

---
<a name="MakeM"></a>
### ```make m```
This is a shorthand for the Django built-in `python manage.py migrate` command, which should be executed after the `make migrations` command whenever any database schema changes have been made. It uses the previously-generated notes to bring the database design up to date with changes to the Python/Django database description code. You'll only need this if you modify the schema.

---
<a name="MakeRun"></a>
### ```make run```
This is a shorthand for the Django built-in `python manage.py runserver` command, which starts the server using a local debugging-only build in web server. This is only needed if you're running a local server - if you've built an image, then the server will always try to run when the corresponding container is active.

---
<a name="MakeRunPublic"></a>
### ```make runpublic```
This is a shorthand for the Django built-in `python3 manage.py runserver 0.0.0.0:8000` command, which starts the server using a local debugging-only build in web server, in a mode where it will respond to incoming requests from other machines on the network. Use this with caution, as it can expose an insecure environment to the local network - which could also expose it to the internet, depending on your network configuration.

This is only needed if you're running a local server - if you've built an image, then the server will always try to run when the corresponding container is active.

---

[Back to README.md](README.md)

Next: [API reference](ApiReference.md)
