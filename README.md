# DR!FT Community API & Racing Server #
[English Manual](README_EN.md)
 
* [Was ist das hier?](#einleitung)
* [Wie installier ich das?](#installation)
* [Wie starte und beende ich das?](#start)
* [Wie bediene ich das?](#bedienung)
* [Typische Fehler und wie man sie hoffentlich behebt](#fehler-und-lösungen)
* [DR!FT Community API](#drift-community-api)


# Einleitung
Dieser DR!FT Racingserver verfolgt zwei Ziele: Zum einen als Prototyp um die DR!FT Community API zu entwickeln und zu testen, zum anderen um euch einen Ausblick darauf zu geben, was damit alles möglich ist. Der DR!FT Racingserver kann lokal auf einem Laptop aufgesetzt werden und stellt euch dort dann eine Webseite bereit, auf der ihr Rennen anlegen, den Rennfortschritt der Teilnehmer anschauen und die Ergebnisse im Anschluss als .csv Datei für den Import in Excel & co herunter laden könnt.

Achtung: Dieser Server ist nicht dazu geeignet, ihn offen ins Internet zu stellen. Die generierte Webseite hat z.B. keinerlei Sicherheitsmaßnahmen wie eine Benutzerverwaltung oder Passwortschutz, d.h. jeder der die Adresse der Webseite kennt kann dort Rennen anlegen, löschen etc.. Benutzt ihn also besser nur lokal und mit Leuten, die da keinen Mist mit machen. Wir werden in Zukunft sicherlich noch bessere Racingserver sehen, die dann im Internet laufen und auf denen jeder ohne Installation bequem selbst seine Rennen auf machen kann, aber das wird noch eine Weile dauern. Dieser Racingserver dient erst mal der schnellen Entwicklung einer soliden Basis. Wenn du mehr zur Entwicklung etc. wissen willst, schau mal ins Kapitel  [DR!FT Community API](#drift-community-api)

# Installation
Zunächst musst du die Software "Docker" installieren. Diese gibt es für Windows, iOS und Linux und eine bequeme Desktop-Version bekommst du hier:

https://www.docker.com/products/docker-desktop

Unter Windows musst du noch das Kernel-Upgrade für WSL2 installieren:
https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi

Und Hyper-V sowie Containers in den Windows Einstellungen aktivieren (geht wohl auch ohne bei Windows Home):
https://www.c-sharpcorner.com/article/how-to-install-docker-desktop-and-troubleshoot-issues-in-windows-machine/

Um zu testen, dass du Docker richtig installiert hast, öffne eine Konsole (Unter Windows geht das über "Shift+Rechtsklick"->"PowerShell Fenster hier öffnen") und tippe den folgenden Befehl, gefolgt von "Enter":

>docker run hello-world

Docker dient als Ausführungsumgebung für die Server, diese laufen als virtuelle Maschinen in Docker, so dass wir keine weitere Software direkt auf deinem PC installieren müssen.

Als Zweites musst du dieses Projekt hier herunter laden. Dazu kannst du oben rechts auf den grünen "Code" Button klicken und wählst "Download ZIP" aus. Das Verzeichnis musst du anschließend noch entpacken, die meisten Computer haben dafür schon Software installiert, falls nicht, empfehle ich dafür: [7Zip - Download](https://www.7-zip.de/).

Jetzt folgt der letzte Schritt: Öffne ein Konsolenfenster im Projektordner ("Shift+Rechtsklick" irgendwo im Ordner->PowerShell-Fenster hier öffnen) und gebe den folgenden Befehl ein:

>docker compose --profile racedisplay up --build

Das kann jetzt eine Weile dauern (5-10 Minuten), weil Docker eine ganze Menge zu tun hat. Das Schöne ist aber, dass man das nur ein mal am Anfang machen muss bzw. nur wenn man den Code ändert. Nachdem der Befehl fertig ist, sollte dort so etwas wie folgendes stehen:

>[+] Running 4/4
> - Network driftapi_default                  Created
>                                                               0.0s
> - Container driftapi-driftapi-db-1          Created
>                                                               0.1s
> - Container driftapi-racedisplay-service-1  Created
>                                                               0.2s
> - Container driftapi-driftapi-service-1     Created                                                               0.2s

Das bedeutet, dass alles geklappt hat und der Racingserver sogar schon im Hintergrund läuft. Das folgende Kapitel kannst du überspringen und direkt bei [Bedienung](#bedienung) weiter machen.

# Start & Stop
Wechsle in den Ordner des Servers (in dem auch diese Anleitung steht), öffne eine Konsole und schreibe:

>docker compose --profile racedisplay up

Darauf sollte jede Menge Text in der Konsole erscheinen, sobald aber die Zeilen mit "Created", die auch bei der Installation erscheinen, zu sehen sind, laufen die Dienste und der Server kann benutzt werden. Siehe folgendes Kapitel zur Bedienung.

Zum stoppen des Servers, schließe das Konsolenfenster oder drücke im Konsolenfenster "Strg + C" um die laufenden Prozesse zu beenden. Die Eingabe des Befehls

>docker compose --profile racedisplay down

entfernt die container komplett vom system, das ist nützlich wenn mal was nicht so läuft wie es soll.

Deinstallation: Für eine Deinstalation löscht ihr einfach den heruntergeladenen Ordner und deinstalliert die Software "Docker".

# Bedienung
Öffne einen Browser deiner Wahl (Chrome und Firefox sind getestet, Safari macht vielleicht Probleme) und gib die folgende Adresse ein:

>127.0.0.1:8080

Du solltest ins Hauptmenü des Servers kommen, von wo aus du Rennen anlegen (Create New Game) oder zuvor angelegte Rennen aufrufen (Show Game) kannst. Hinweis: Sobald ein Rennen angelegt wurde, nimmt der Server Daten von der App entgegen, unabhängig davon, ob du das Browserfenster offen lässt oder welches Rennen du gerade anzeigst. Du kannst also ruhig mehrere Rennen erstellen die gleichzeitig von Spielern genutzt werden.

Sobald du ein neues Rennen über das Menü angelegt hast, kannst du in der DR!FT-App über folgende URL beitreten:

>`http://<ip-des-servers>:8001/game`
 
wobei du `<ip-des-server>` mit der IP des Computers auf dem du den Server laufen lässt, ersetzt. Beispiel: Wenn mein PC die IP 192.168.40.23 hat, dann muss ich in der DR!FT App beim Feld URL http://192.168.40.23:8001/game eingeben. Die game-id in der app muss genau so heissen wie die vom Spiel das du erstellst und dein Nutzername sollte möglichst keine Sonderzeichen wie ' enthalten.

## Create New Game
Wähle eine Game ID ohne Leerzeichen. Tipp: Wähle kurze, einfache Bezeichner, da die Spieler diese ja auch in der App eingeben müssen. Dann klicke auf "Create" um ein Rennen anzulegen oder wähle zuvor "Optional settings" um Einstellungen für die Spieler vorzunehmen. Wenn sich ein Spieler mit dem Server synchronisiert, dann werden die hier gewählten Einstellungen als Renneinstellungen übernommen (Achtung: Die Spieler können diese anschließend immer noch ändern, diese sind nur ein "Vorschlag"). Auf der linken Seite bei "Enable..." muss bei einer Option ein Haken gesetzt werden, auf der rechten Seite wird der konkrete Wert eingestellt. Die meisten Optionen sollten Selbsterklärend sein, daher hier nur ein paar Hinweise zu den komplizierteren:

* Track name - Der Rennstrecken-Name. Wird derzeit nicht genutzt, ist aber dafür vorgesehen, beim Datenexport mit angegeben zu werden.
* Enable time limit - Wird derzeit nicht genutzt, wird später für serverseitig umgesetzte Zeitrennen verwendet werden.
* Enable Joker Lap Counter - Wenn diese Option gesetzt wird, dann wird sobald das ausgewählte Target überfahren wird, der Joker-Lap Counter hochgezählt. Achtung: Wenn dies das start/finish Target ist, dann wird sowohl eine normale Runde als auch eine Joker-Runde gezählt.
* Enable precondition - Falls ihr Rallycross oder Rally fahrt, braucht ihr die normalen Targets vermutlich für andere Zwecke. In diesem Fall könnt ihr hier einstellen, welches andere Target vor dem eigentlichen oben ausgewählten Joker-Target überfahren werden muss, damit es als Joker-Target zählt. Achtung: Zwischen der Erkennung zweier Targets muss immer etwas Zeit vergehen, sonst wird das zweite Target nicht erkannt. Das ist nötig, weil man manchmal Targets zweifach oder sogar dreifach legt damit die auf jeden Fall erkannt werden.

Nachdem man auf den Button "Create" geklickt hat, wird ein entsprechend benanntes Rennen angelegt und man wechselt in die Rennansicht.

## Rennansicht
In der Rennansicht sieht man eine Tabelle, wobei pro Spieler eine Zeile zur Verfügung steht. Sobald ein Spieler einem Spiel beitritt, also im Rennmenü auf den Rennstart klickt und dann das Armaturenbrett erscheint, aber noch bevor er der Motor startet, erscheint sein Name in dieser Liste. So könnt ihr sehen, wer schon bereit ist, das Rennen zu beginnen.

Unter der Tabelle gibt es zwei ausklappbare Menüs. Unter "Game Settings" sieht man eine Zusammenfassung der Renneinstellungen. Unter "Connection Info" gibt es Informationen dazu, wie man diesem Rennen beitreten kann. Der QR-Code enthält die darunter stehende URL zum einfacheren Beitritt. Aber Achtung: die URL stimmt leider oft nicht. In der Regel muss die IP-Adresse, also die Zahlenkombination dort durch eine andere ersetzt werden. Siehe dazu auch [Die IP unter Connection Info stimmt nicht](#die-ip-unter-connection-info-stimmt-nicht).

Ganz unten stehen noch vier Buttons:

* Download - Hier können die aktuellen Renndaten als .csv oder .json herunter geladen werden, um sie anschließend z.B. in Excel zu importieren.
* Remove Player - Löscht einen bestimmten Spielernamen aus der Tabelle (wenn mal was schief gelaufen ist)
* Reset Game - Löscht ALLE Ergebnisse aus der Liste, das Rennen bleibt aber erhalten.
* Delete Game - Löscht das komplette Rennen und alle dazugehörigen Daten vom Server und kehrt ins Hauptmenü zurück

# Fehler und Lösungen

* [Docker compose funktioniert nicht](#docker-compose-funktioniert-nicht)
* [Die IP unter Connection Info stimmt nicht](#die-ip-unter-connection-info-stimmt-nicht)
* [Die DR!FT-App findet den Server nicht](#die-drift-app-findet-den-server-nicht)
* [Die Zeiten im Racingserver stimmen nicht exakt mit denen in der App überein](#die-zeiten-im-racingserver-stimmen-nicht-exakt-mit-denen-in-der-app-überein)
* [Ein Spieler steht doppelt in der Liste](#ein-spieler-steht-doppelt-in-der-liste)


## Docker compose funktioniert nicht ##
Das kann mehrere Gründe haben, die häufigsten sind hier aufgeführt:

### Grund 1: Docker läuft nicht im Hintergrund ###
Der häufigste Grund ist der, dass der docker service nicht im Hintergrund läuft. Stell sicher, dass docker läuft. Standardmässig wird docker bei der Installation fragen, ob es automatisch bei systemstart gestartet werden soll. Wenn du dem nicht zugestimmt hast, dann starte docker desktop selbst, bevor du docker compose ausführst. Schau ansonsten auch, welche Fehlermeldungen du angezeigt bekommst, wenn du Docker Desktop ausführst.

### Grund 2: Nicht genug Speicherplatz ###
Der zweite häufige Grund ist mangelnder Speicherplatz. Stell sicher, dass auf deiner Systemfestplatte genug Platz frei ist (etwa 5GB). Wenn du den Server häufig benutzt, macht es ab und zu sinn, ältere docker dateien zu löschen. Wenn du Docker Desktop installiert hast, dann kannst du das recht einfach über die GUI erledigen. Siehe dazu [Lösung: Reset](#lösung:-reset).

### Grund 3: Irgendwas ist beim Erstellen der Dienste schief gegangen ###
Kann selten mal passieren, folge einfach den Anweisungen in  [Lösung: Reset](#lösung:-reset).

### Lösung: Reset ###
Starte eine Konsole im Projektordner und gib folgende Befehle ein, um alle laufenden Container zu beenden und von Docker gebauten Container und Daten zu löschen:
>docker compose --profile racedisplay down
>docker system prune --all --force --volumes
Dann folge den Anweisungen im Kapitel [Installation](#installation) direkt nachdem Docker installiert wurde.

## Die IP unter Connection Info stimmt nicht ##
Das Problem ist bekannt und steht auf der "Todo" Liste. Ermittel die IP des Laptops auf dem der Server läuft manuell, z.B. über den Konsolenbefehl "ipconfig" unter windows oder "ifconfig" unter linux/ios. Dann öffne die datei ".env" im Hauptverzeichnis des Projektes und änder die Zeile

>STREAMLIT_HOSTNAME=127.0.0.1

so, dass statt der 127.0.0.1 deine Host-IP steht. Bei meinem Windows PC bekomme ich über den Befehl "ipconfig" z.B. mehrere verschiedene Netzwerkadressen angezeigt, die richtige darunter ist die unter "Ethernet-Adapter Ethernet", weil mein PC über Kabel an meinem WLAN-Router hängt. Wenn du mit dem PC direkt im WLAN bist, dann halte besser nach einem WIFI adapter Ausschau, wichtig ist aber, dass der adaptername kein "vEthernet" enthält, das ist nur ein virtueller netzwerkadapter von docker.

## Die DRIFT-App findet den Server nicht ##
Zunächst solltest du sicher stellen, dass dein Smartphone auf dem die DR!FT App läuft, im gleichen WLAN ist wie der Computer auf dem der Server läuft. Zuhause reicht es meist, wenn man z.B. einen Router mit einem WLAN hat und einen PC über LAN daran angeschlossen hat. Eine Alternative dazu sind Laptops, die ein Ad-Hoc WLAN aufmachen können.

Als Zweites solltest du kontrollieren, ob du die richtige IP-Adresse verwendest (notfalls manuell ermitteln, siehe obiger Punkte). Wenn die Adresse korrekt ist, aber kein Rennen mit diesem Namen existiert, dann erscheint in der App ein rotes Kreuz. In dem Fall, einfach auf dem Server ein entsprechend benanntes Rennen erstellen.

Als Drittes kann es sein, dass deine Firewall die Verbindungen blockt. Normalerweise ist das gut, weil du nicht möchtest, dass irgendwelche Apps auf deinem PC ohne dein Wissen auf eingehende Verbindungen reagieren, aber hier wollen wir das ja. Du muss also deiner Firewall sagen, dass sie auf Port 8001 eingehende Verbindungen zulassen soll. Bei Windows 10 geht das folgendermassen: Windows Firewall -> Erweiterte Einstellungen -> Links: Eingehende Regeln -> Neue Regel... -> Regeltyp: "Port", TCP und 8001 als Port angeben und "weiter" -> Verbindung zulassen -> Profil Domäne und Privat an lassen, Öffentlich aus -> Name ist egal, z.B. "Portfreigabe für DR!FT Server" -> Fertig stellen.

## Die Zeiten im Racingserver stimmen nicht exakt mit denen in der App überein ##
Es kann vorkommen, dass die Zeiten um wenige (1-4) Millisekunden unterschiedlich sind. Dieser Fehler ist bekannt und steht auf der TODO-Liste.

## Ein Spieler steht doppelt in der Liste ##
Das kann vorkommen, wenn zwei Spieler den gleichen Namen gewählt haben oder die App zwischendurch mal vollständig aus gewesen ist, oder man auf ein anderes Smartphone gewechselt ist. Da die API aus rechtlichen Gründen nicht automatisch eure echten Sturmkind-Account namen rausgeben darf, verwenden wir für die Zuordnung ein ab und zu wechselndes Merkmal. Ich empfehle, pro Rennen das ihr fahrt entweder immer auch ein neues Rennen im Server anzulegen, oder aber zwischendurch den Reset-Knopf zu drücken. Ihr könnte aber unter der Liste auch gezielt nur bestimmte Spielernamen aus der Liste löschen.

# DRIFT Community API
Die DR!FT Community API ist der Kern der Entwicklung und die Sturmkind DR!FT App ist so programmiert, dass sie mit Servern die diese API implementieren kommunizieren kann. Kern der Überlegung ist, dass die App meist keine konkrete Antwort erwartet, sondern einfach immer nur wenn etwas Interessantes passiert (ein Rennen eingestellt, gestartet oder beendet oder ein Barcode gelesen wird) eine kurze Nachricht an die eingestellte URI verschickt. Dieses Projekt zeigt euch im Grunde genommen, wie man auf Basis der API einen Racingserver implementieren kann.

Dazu gehören im Grunde genommen drei Komponenten: Eine Datenbank (MongoDB), ein Backend (driftapi-service) und ein Frontend (racedisplay-service). Über den weiter oben genannten Startbefehl startet docker diese drei Komponenten in kleinen virtuellen Maschinen, damit keine weitere Software auf dem Host-System installiert werden muss. Dadurch sollte man dieses projekt auch auf windows, ios und linux gleichermaßen ausführen können.

Für die Datenbank braucht es keinen weiteren Ordner, aber das Backend mit der implementierung der API und der Hintergrundlogik ist im Ordner /driftapi zu finden und das Frontend im Ordner /streamlit. Beide sind in Python geschrieben.

Langfristig wäre es besser, das ganze vollständig als Online-plattform zu implementieren und aus Gründen der Performanz eine tabellenbasierte Datenbank zu verwenden.

Die technische Beschreibung der API findest du in diesem Ordner in der Datei "openapi.json" oder wenn du den server startest, in grafisch ansprechenderer Form unter der adresse 

>localhost:8001/docs

Die OpenAPI datei kannst du z.B. auf [postman](https://www.postman.com/) oder [swagger.io](swagger.io) importieren um sie anzuschauen.

## API-Calls - Ablauf ##

### /ping
Wenn der Nutzer die API im Rennmenü aktiviert, versucht die App zunächst den /ping Endpunkt zu erreichen. Klappt dass, erscheint ein Grüner Haken in der App. Als Rückgabewert akzeptiert die App ausserdem ein JSON-Dictionary, mit dem in der App die Renneinstellungen überschrieben werden:

>{
>  "status": true,
>  "start_time": "2022-05-31T18:40:45.194Z",
>  "lap_count": 0,
>  "track_condition": "drift_asphalt",
>  "track_bundle": "none",
>  "wheels": "normal",
>  "setup_mode": "RACE"
>}

Die Möglichen Rückgabewerte hier kann man auch gut im Datenmodell des Servers anschauen: [Klick hier](https://github.com/christiangeissler/driftapi/blob/main/driftapi/driftapi/model.py)

### /enter
Wenn der Spieler das Rennen aus dem Menü heraus startet und das erste Mal das Armaturenbrett sieht, wird der /enter Endpunkt aufgerufen und die vom Spieler final gewählten Renneinstellungen, aber auch die Motoreinstellungen an den Server übertragen.

### /start
Wenn der Spieler den Motor anschaltet und der Countdown grün zeigt, wird der /start Endpunkt aufgerufen und die exakte Startzeit übermittelt.

### /target
Wenn der Spieler ein Target überfährt und die Punkte feststehen, wird der /target Endpunkt aufgerufen. Die übermittelten Informationen beinhalten den Code des Targets und den exakten Zeitpunkt, wann das Target erkannt wurde. Ausserdem noch die bisher gefahrene Distanz und Zeitdauer des Laufs sowie ob es am Anfang einen Frühstart gab.

### /end
Wenn der Spieler den Motor abschaltet und der Statistikbildschirm geladen wurde, wird der /end Endpunkt aufgerufen und die abschließenden Renninformationen wie die finale Gymkhana Punktzahl, die gefahrene Zeit und Distanz übermittelt.

Wenn du darüber hinaus weitere Fragen hast, empfehle ich diese direkt im [Sturmkind Forum]([https://community.sturmkind.com](https://community.sturmkind.com/topic/3637-entwickler-informationen-zur-drft-community-api/)) in der entsprechenden Rubrik zur Community API zu stellen, damit von den Antworten dort auch andere profitieren können.

# Wie geht es weiter?
Mit der Veröffentlichung der Community API geht Sturmkind einen ersten Schritt in Richtung Multiplayerunterstützung. Aber der Weg ist noch lange nicht zuende, denn auch wenn man mit diesem Projekt hier einen ersten Racing-Server aufsetzen kann, so hat nicht jeder Nutzer Lust und Zeit, lokal einen eigenen Server zu betreiben. Wenn du selbst dich an der Weiterentwicklung oder einer Eigenentwicklung eines Servers versuchen möchtest, so bist du herzlich eingeladen, im Sturmkind Forum mit uns zu diskutieren, dein Projekt vorzustellen und dort auch Fragen zur API etc. zu stellen. Denn die Kernidee der API ist es gerade, dass wir als Community mit dieser alle Möglichen kreativen Dinge anstellen können.
