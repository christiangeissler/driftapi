# Dr!ft Community API Racing Server
 
* [What is this?](#introduction)
* [How do I install this?](#installation)
* [How do I start and stop this?](#start)
* [How do I operate this?](#operation)
* [Typical errors and how to hopefully fix them](#errors-and-solutions)
* [Dr!ft Community API](#drift-community-api)


# Introduction
This Dr!ft racing server has two goals: Firstly as a prototype to develop and test the Dr!ft Community API, and secondly to give you a preview of what is possible with it. The Dr!ft Racingserver can be set up locally on a laptop and provides you with a website where you can create races, view the race progress of the participants and download the results as a .csv file for import into Excel & co.

Attention: This server is not suitable to put it openly on the internet. The generated website has e.g. no security measures like a user administration or password protection, i.e. everyone who knows the address of the website can create, delete races etc. there. So better use it only locally and with people who don't do crap with it. In the future we will certainly see even better racing servers that run on the Internet and on which everyone can comfortably create their own races without installation, but that will still take a while. This racing server is for the time being a fast development of a solid base. If you want to know more about the development etc., have a look at the chapter [Dr!ft Community API](#drift-community-api)

# Installation
First, you need to install the "Docker" software on your PC. This is available for Windows, iOS and Linux and you can get a convenient desktop version here:

https://www.docker.com/products/docker-desktop

Install the software, then open a console window in the same folder where this guide is located. On Windows you can do this with "Shift+Rightclick"->"Open PowerShell window here". As a test if the installation worked, you can run

>docker run hello-world

to test if the installation worked. If that runs, you can install the racing server by typing the following command in the same console (or copy the command and right click in the console, that will paste the text there):

>docker compose --profile racedisplay up --build

Now this may take a while because Docker has a lot to do. But the nice thing is that you only have to do this once at the beginning or only when you change the code. After the command is done, it should say something like this:

>[+] Running 4/4
> - Network driftapi_default Created
> 0.0s
> - Container driftapi-driftapi-db-1 Created
> 0.1s
> - Container driftapi-racedisplay-service-1 Created
> 0.2s
> - Container driftapi-driftapi-service-1 Created 0.2s

This means that everything worked and the racing server is already running in the background. You can stop the server by pressing "Ctrl+C" in the console.

# Start
Change to the folder of the server (where this tutorial is), open a console and write:

>docker compose --profile racedisplay up

You should see a lot of text in the console, but as soon as you see the lines with "Created" which also appear during the installation, the services are running and the server can be used. See the following chapter for operation.

# Stop
Close the console window or press "Ctrl + C" in the console window to stop the running processes. Entering the command

>docker compose --profile racedisplay down

removes the containers from the system and is recommended for a clean exit.

# Operation
Open a browser of your choice and enter the following address:

>localhost:8080

You should get to the main menu of the server, from where you can create races (Create New Game) or view previously created races (Show Game). Note: Once a race is created, the server will accept data from the app regardless of whether you leave the browser window open or which race you are currently viewing. So feel free to create multiple races that will be used by players at the same time.

## Create New Game
Choose a Game ID without spaces. Tip: Choose short, simple identifiers, because the players have to enter them in the app. Then click on "Create" to create a race or select "Optional settings" beforehand to make settings for the players. When a player synchronizes with the server, the settings selected here will be used as race settings (note: the players can still change these afterwards, these are only a "suggestion"). On the left side at "Enable..." a check mark must be set at an option, on the right side the concrete value is set. Most options should be self-explanatory, so here are just a few hints for the more complicated ones:

* Track name - Currently not used, but is intended to be included in the data export.
* Enable time limit - Currently not used, but will be used later for server-side implemented time races.
* Enable Joker Lap Counter - If set, the joker lap counter will be incremented as soon as the selected target is passed. Note: If this is the start/finish target, then both a normal lap and a joker lap will be counted.
* Enable precondition - If you drive Rallycross or Rally, you probably need the normal targets for other purposes. In this case you can set here which other target has to be passed before the actual joker target selected above, so that it counts as a joker target. Attention: There must always be some time between the recognition of two targets, otherwise the second target will not be recognized. This is necessary because sometimes targets are placed twice or even three times so that they are recognized in any case.

After clicking on the "Create" button, a race is created and you switch to the race view.

## Race view
In the race view you see a table with one row per player. As soon as a player joins a game, i.e. clicks on the race start in the race menu and then the dashboard appears, but before he starts the engine, his name appears in this list. So you can see who is already ready to start the race.

Below the table there are two fold-out menus. Under "Game Settings" you can see a summary of the race settings. Under "Connection Info" there is information on how to join this race. The QR code contains the URL below it for easier joining. But beware: unfortunately, the URL is often not correct. As a rule, the IP address, i.e. the combination of numbers there, must be replaced by another one. See also [The IP under Connection Info is not correct](#the-ip-under-connection-info-is-not-correct).

At the bottom there are four buttons:

* Download - Here you can download the current race data as .csv or .json file to import it e.g. into Excel.
* Remove Player - Deletes a specific player name from the table (if something went wrong).
* Reset Game - Deletes ALL results from the list, but the race remains.
* Delete Game - Deletes the complete race and all related data from the server and returns to the main menu

# Errors and solutions

* [Docker compose does not work](#docker-compose-does-not-work).
* [The IP under connection info is not correct](#the-ip-under-connection-info-is-not-correct)
* [The drift-app does not find the server](#the-drift-app-does-not-find-the-server)
* [The times in the racing server do not match exactly with those in the app](#the-times-in-the-racing-server-don't-match-exactly-with-those-in-the-app)
* [A player is listed twice](#a-player-is-listed-doubly-in-the-list)


## Docker compose is not working ##
This can be due to several reasons, the most common ones are listed here:

### Reason 1: Docker is not running in the background ###
The most common reason is that the docker service is not running in the background. Make sure docker is running. By default, docker will ask during installation if you want it to start automatically on systemstart. If you didn't agree to that, then start docker itself before running docker compose.

### Reason 2: Not enough disk space ###
The second common reason is lack of disk space. Make sure you have enough free space on your system disk (around 5GB). If you use the server frequently, it makes sense to delete older docker files from time to time. If you have Docker Desktop installed, you can do this quite easily via the GUI. See [solution: reset](#solution:-reset).

### Reason 3: Something went wrong when creating the services ###
Happens rarely, just follow the instructions in [solution: reset](#solution:-reset).

### Solution: Reset ###
Make sure there are no containers running. In the Docker Desktop GUI, click on the top button in the left sidebar ("Containers/Apps"). Stop all containers that are visible there and delete them. After that, click on "Images" in the left sidebar. Delete all of them here as well. Then do the same with the "Volumes" below. Then follow the instructions in the [Installation](#installation) chapter right after Docker is installed.

## The IP under Connection Info is not correct ##
The problem is known and is on the "todo" list. Determine the IP of the laptop on which the server is running manually, e.g. via the console command "ipconfig" under windows or "ifconfig" under linux/ios. Then open the file ".env" in the root directory of the project and change the line

>STREAMLIT_HOSTNAME=127.0.0.1

so that instead of 127.0.0.1 it says your host IP. With my Windows PC I get several different network addresses via the command "ipconfig" for example, the correct one is the one under "Ethernet-Adapter Ethernet", because my PC is connected via cable to my WLAN router. If you are with the PC directly in the WLAN, then better look for a WIFI adapter, but it is important that the adapter name does not contain "vEthernet", because that is only a virtual network adapter of docker.

## The drift app does not find the server ##
Check if you are using the correct IP address (if necessary determine it manually, see above points). If the address is correct, but no race with this name exists, then a red cross appears in the app. In this case, simply create a race on the server with this name.

## The times in the race server do not exactly match those in the app ##
It can happen that the times are different by a few milliseconds, so far I have noticed differences around +- 0.004 seconds. This bug is known and already on the "todo" list.

## A player is twice in the list ##
This can happen if two players have chosen the same name or the app has been completely off in between, or you have switched to another smartphone. Because the API is not allowed to automatically give out your real Sturmkind account names for legal reasons, we use a feature that changes from time to time for the assignment. I recommend to create a new race in the server for each race you run, or to press the reset button in between. You could also delete specific player names from the list.

# Drift Community API
The Dr!ft Community API is the core of the development and the Sturmkind Dr!ft App is programmed to communicate with servers that implement this API. The core of the thinking is that most of the time the app doesn't expect a specific response, it just sends a short message to the set URI whenever something interesting happens (a race is set, started or finished or a barcode is read). This project basically shows you how to implement a racing server based on the API.

This basically involves three components: A database (MongoDB), a backend (driftapi-service) and a frontend (racedisplay-service). Using the startup command mentioned earlier, docker starts these three components in small virtual machines so that no additional software needs to be installed on the host system. This should allow you to run this project on windows, ios and linux equally.

There is no need for another folder for the database, but the backend with the implementation of the API and the background logic can be found in the /driftapi folder and the frontend in the /streamlit folder. Both are written in Python.

In the long run it would be better to implement the whole thing completely as an online platform and use a table based database for performance reasons.

The technical description of the API can be found in this folder in the file "openapi.json" or when you start the server, in a more graphically appealing form at the address 

>localhost:8080/docs

You can import the OpenAPI file to [postman](https://www.postman.com/) or [swagger.io](swagger.io) to view it.

If you have further questions, I recommend to ask them directly in the [Sturmkind Forum](https://community.sturmkind.com) in the corresponding section about the Community API, so that others can benefit from the answers there.

# What's next?
With the release of the Community API Sturmkind takes a first step towards multiplayer support. But the road is far from over, because even if you can set up a first racing server here with this project, not every user has the desire and time to run his own server locally. If you want to try yourself on the further development or a self-development of a server, you are invited to discuss with us in the Sturmkind forum, to present your project and to ask questions about the API etc. there. Because the core idea of the API is that we as a community can do all kinds of creative things with it.