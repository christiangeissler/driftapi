# Quickstart:
Have docker installed
run in root: docker compose --profile racedisplay up --build
visit localhost:8080 in your browser and create a game.
Open Drift-App, in the race setup menue enter the local ip-adress of the server (on windows: open cmd, type "ipconfig" to see the ip adresses) with a /game at the end (example: 192.188.22.54/game) as the server uri and choose the same game_id as when you created the game.
Start the game and drive. You should see the round times appearing on the score board.



# driftapi
An openapi proposal and reference server implementation for submitting sturmkind app's racing information

The goal is to have a scoreboard with live-information outside of the app that can show what's going on in the race and that can export the statistics of the race after it is completed.

This folder contains:
driftapi - The fastapi implementation of the proposed openapi and the backend of the server.
streamlit - The web-frontend server that accesses the backend server, offers race management and the live-scoreboard.

# vision & use case
The basic idea behind this api is to establish a standard for the dr!ft app to inform third-party apps during a race about the progress. Ideally, the players will enter the uri of the webservice where this api is implemented on at the beginning / in the settings of the app. When they start a game and such an uri is set, the app then sends information such as when a barcode has been detected to the api. Behind the api, the webserver can use the information to provide a lap counter or the fastest lap times overview and much more.

For robustness reasons, the whole interaction is considered to be one way. Under no circumstances should the webserver be able to influence the app and the app should always expect the webserver to be malicious. Therefore, all calls should be done in an asynchroneous way and the app should never expect to get anything back for the calls.

# detailed use case
## 1 Step ##
first, the user enters a uri into the dr!ft app settings and chooses a displayed user name. The uri is a combination of the adress where the webservice is located plus an identifier to allow the same webservice to distinguis different races. Example for such an uri:

"https://driftevent.de/racingserver/game/race143"

Where "https://driftevent.de/racingserver" is the root where the service runs, and "race143" is an identifier for a specific race, event, challenge or whatever.

In the beginning, this uri will be entered manually in the app, at a future stage, a QR-Code reader could be used to set it more convenient.

## 2nd Step ## (Optional)
After setting the uri, the app can call the following uri to check if it is correct and a service is running on the other side. This will also return the race settings that then will be used as preset in the drift-app.

https://driftevent.de/racingserver/game/race143/ping

## 3rd Step ##
Then, the user just starts a normal race/gymkhana/free run as usual. Upon entering the game but before the user starts the motor, the drift app in our example can call

https://driftevent.de/racingserver/game/race143/enter

to submit the car and race settings as well as the user name that can be displayed on a score board. For legal / privacy reasons, this choosen user name does not need to be identical with the sturmkind user name.

Note: All the calls to /events/* require a timestamp (down to fractions of seconds) and a uuid. The timestamp can be based on the system time of the device, as only the difference between the timestamps is required to calculate the lap times etc., so it is not important to exactly sync it. The uuid needs to stay the same for the race but does and must not be the sturmkind account name. One idea for it would be to generate a random cryptic uuid whenever the user enters a new uri in step 1.

## 4th Step ##
When the player starts the motor of the car, the drift app in our example calls
https://driftevent.de/racingserver/game/race143/start

## 5th Step ##
Whenever the app recognizes that a barcode has been detected, it calls 

https://driftevent.de/racingserver/game/race143/target

See the api documentation for the required body. This tells the server when and which barcode has been crossed, which allows for counting laps, lap times etc.
This is the most important API call. Note: for now, no further information that that is passed, maybe in the future, also the speed and drift angle might get submitted as well.

## 6th Step ##
When the user stops the motor (and therefore, finishes the run), the app send the finish information to the api.

https://driftevent.de/racingserver/game/race143/end


# installation
Make sure that docker (https://www.docker.com/products/docker-desktop/) is installed and accessible from your console/shell.

After cloning the repository, you can startup the service by running

docker compose --profile racedisplay up --build

in the root directory of the project (the one containing the docker-compose.yml file). This will build and then start three containers:

1) a MongoDB server running a database
2) the fastapi server with the driftapi and the backend logic
3) a streamlit server that offers the scoreboard (the racedisplay service)

After that, visit localhost:8080 to see the scoreboard or localhost:8001/docs to view the api.

Note: The correct uri for the drift-app to enter stuff is <ip of the host>:8080/game/<game_id>, use "ifconfig" on unix or "ipconfig" on windows shell to get the ip of the host.

# using this code
After running, a local webserver should be open and accessible via a webbrowser entering "localhost:8001". A small welcome message should appear. Go to /docs to browse the interface description. You can also download an openapi.json description of the interface that can be used in code-generators etc. to generate a server stub implementing this interface.

Currently, there is also a small MongoDB database already integrated behind the api, so feel free to test it out using the swagger ui. Enter a race, submit barcode events and use the /yourraceid/events put call to see the entered events.

# whats next?
Please check the concept and feel free to send me any questions to: geissler@illusion-games.de.
