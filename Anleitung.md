[Was ist das hier?](#einleitung) 
[Wie installier ich das?](#installation)
[Wie starte und beende ich das?](#start)
[Wie bediene ich das?](#bedienung)
[Typische Fehler und wie man sie hoffentlich behebt](#fehler-und-lösungen)
[Dr!ft Community API](#drift-community-api)


#Einleitung
Dieser Dr!ft Racingserver verfolgt zwei Ziele: Zum einen als Prototyp um die Dr!ft Community API zu entwickeln und zu testen, zum anderen um euch einen Ausblick darauf zu geben, was damit alles möglich ist. Der Dr!ft Racingserver kann lokal auf einem Laptop aufgesetzt werden und stellt euch dort dann eine Webseite bereit, auf der ihr Rennen anlegen, den Rennfortschritt der Teilnehmer anschauen und die Ergebnisse im Anschluss als .csv Datei für den Import in Excel & co herunter laden könnt.

Achtung: Dieser Server ist nicht dazu geeignet, ihn offen ins Internet zu stellen. Die generierte Webseite hat z.B. keinerlei Sicherheitsmaßnahmen wie eine Benutzerverwaltung oder Passwortschutz, d.h. jeder der die Adresse der Webseite kennt kann dort Rennen anlegen, löschen etc.. Benutzt ihn also besser nur lokal und mit Leuten, die da keinen Mist mit machen. Wir werden in Zukunft sicherlich noch bessere Racingserver sehen, die dann im Internet laufen und auf denen jeder ohne Installation bequem selbst seine Rennen auf machen kann, aber das wird noch eine Weile dauern. Dieser Racingserver dient erst mal der schnellen Entwicklung einer soliden Basis. Wenn du mehr zur Entwicklung etc. wissen willst, schau mal ins Kapitel  [Dr!ft Community API](#drift-community-api)

#Installation
Zunächst musst du auf deinem PC die Software "Docker" installieren. Diese gibt es für Windows, iOS und Linux und eine bequeme Desktop-Version bekommst du hier:

https://www.docker.com/products/docker-desktop

Installier die Software, dann öffne ein Konsolenfenster im gleichen Ordner wo auch diese Anleitung hier liegt. Unter Windows geht das über "Shift+Rechtsklick"->"PowerShell Fenster hier öffnen". Als Test ob die Installation geklappt hat, kanns du mal

>docker run hello-world

eintippen. Wenn das läuft, kannst du den Racingserver installieren indem du in die gleiche Konsole den folgenden Befehl eintippst (oder den Befehl kopierst und in der Konsole einen Rechtsklick machst, das fügt den Text da ein):

>docker compose --profile racedisplay up --build

Das kann jetzt eine Weile dauern, weil Docker eine ganze Menge zu tun hat. Das Schöne ist aber, dass man das nur ein mal am Anfang machen muss bzw. nur wenn man den Code ändert. Nachdem der Befehl fertig ist, sollte dort so etwas wie folgendes stehen:

>[+] Running 4/4
> - Network driftapi_default                  Created
>                                                               0.0s
> - Container driftapi-driftapi-db-1          Created
>                                                               0.1s
> - Container driftapi-racedisplay-service-1  Created
>                                                               0.2s
> - Container driftapi-driftapi-service-1     Created                                                               0.2s

Das bedeutet, dass alles geklappt hat und der Racingserver sogar schon im Hintergrund läuft. Beenden könnt ihr den Server indem ihr in der Konsole "Str+C" drückt.

#Start

#Bedienung

#Fehler und Lösungen

#Drift Community API
