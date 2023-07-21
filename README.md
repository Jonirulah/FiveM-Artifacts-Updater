# FiveM Artifacts Updater for Linux

FiveM Artifacts Updater is just a python script (using webscrap) to update your FiveM artifacts to a build number or the last release of artifacts, made for Linux for people with almost no idea of using it. Updating your artifacts should take less than 1 minute to be honest, but I know from experience that some people can take up to 30 minutes to do so, so this script does it for you in less than 10 seconds. ___(5 if you remove the sleeps)___

To auto-update artifacts for you, you should run a cron job.

## Installation

There are a few libraries that are required in order to run the updater. 

```bash
sudo apt install python3-pip
pip3 install bs4
pip3 install lxml
pip3 install tabulate
```

## Pre-requisites
This script is intended to run with FiveM as a service, there are some people that run FiveM inside a screen (this is not the way to do so). So in order to have this script we need first to have FiveM as a service.

To do that first we need to create the service.
```bash
$ sudo nano /etc/systemd/system/fivem.service
```
We will write the following content in the file.
```bash

[Unit]
Description=FiveM Service
After=network.target

[Service]
ExecStart=/path/to/run.sh
User=fivem # your user
Group=fivem # your group <- usually is you username.

[Install]
WantedBy=multi-user.target
```

Now we have configured our service! Now our FiveM will run as a **service**!


So let's refresh the **systemd** to allow our service to show.

```bash
$ sudo systemctl daemon-reload
```

Now you are good to go!

## Usage

The usage from the script is very straight forward to be honest. Just make sure to edit both of the variables properly and you should be okay, however as much I would like to guarantee you that you will be fine I cannot do so!

If you don't choose a build it will automatically download the latest version for you, if not you can choose whatever version you want, from the first one to the latest one. Just be advised that last versions can break script/server compatibility.

**Unattended mode**

--build or -b to choose a build, use the number of the build or latest.

--clear-cache or -c to clear the server cache.

Example: -b 5488 -c

![Sin título](https://github.com/Jonirulah/FiveM-Artifacts-Updater/assets/25936173/4d7fa7d0-acd7-48ce-a8b1-40c5858cd4b7)

![485e42ae739608c9e94bb17f7e9dd215](https://github.com/Jonirulah/FiveM-Artifacts-Updater/assets/25936173/ad86e02f-e8cd-4163-ad85-3454fab0c102)

![f0bb76f1f685e5614186eac939a3cea4](https://github.com/Jonirulah/FiveM-Artifacts-Updater/assets/25936173/727f2473-fddd-450e-a982-bfdad68053e9)

## License

[MIT](https://choosealicense.com/licenses/mit/)
