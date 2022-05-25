# Dr!ft Community API Racing Server #
 
* [Was ist das hier?](#einleitung)
* [Wie installier ich das?](#installation)
* [Wie starte und beende ich das?](#start)
* [Wie bediene ich das?](#bedienung)
* [Typische Fehler und wie man sie hoffentlich behebt](#fehler-und-lösungen)
* [Dr!ft Community API](#drift-community-api)


# Einleitung
Dieser Dr!ft Racingserver verfolgt zwei Ziele: Zum einen als Prototyp um die Dr!ft Community API zu entwickeln und zu testen, zum anderen um euch einen Ausblick darauf zu geben, was damit alles möglich ist. Der Dr!ft Racingserver kann lokal auf einem Laptop aufgesetzt werden und stellt euch dort dann eine Webseite bereit, auf der ihr Rennen anlegen, den Rennfortschritt der Teilnehmer anschauen und die Ergebnisse im Anschluss als .csv Datei für den Import in Excel & co herunter laden könnt.

Achtung: Dieser Server ist nicht dazu geeignet, ihn offen ins Internet zu stellen. Die generierte Webseite hat z.B. keinerlei Sicherheitsmaßnahmen wie eine Benutzerverwaltung oder Passwortschutz, d.h. jeder der die Adresse der Webseite kennt kann dort Rennen anlegen, löschen etc.. Benutzt ihn also besser nur lokal und mit Leuten, die da keinen Mist mit machen. Wir werden in Zukunft sicherlich noch bessere Racingserver sehen, die dann im Internet laufen und auf denen jeder ohne Installation bequem selbst seine Rennen auf machen kann, aber das wird noch eine Weile dauern. Dieser Racingserver dient erst mal der schnellen Entwicklung einer soliden Basis. Wenn du mehr zur Entwicklung etc. wissen willst, schau mal ins Kapitel  [Dr!ft Community API](#drift-community-api)

# Installation
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

# Start
Wechsle in den Ordner des Servers (in dem auch diese Anleitung steht), öffne eine Konsole und schreibe:

>docker compose --profile racedisplay up

Danach kannst du den Server über die Webseite "localhost:8080" erreichen, einfach in die Browser-Adresszeile schreiben.

# Bedienung

# Fehler und Lösungen

* [Docker compose funktioniert nicht](#docker-compose-funktioniert-nicht)
* [Die IP unter Connection Info stimmt nicht](#die-ip-unter-connection-info-stimmt-nicht)
* [Die Drift-App findet den Server nicht](#die-drift-app-findet-den-server-nicht)
* [Die Zeiten im Racingserver stimmen nicht exakt mit denen in der App überein](#die-zeiten-im-racingserver-stimmen-nicht-exakt-mit-denen-in-der-app-überein)
* [Ein Spieler steht doppelt in der Liste](#ein-spieler-steht-doppelt-in-der-liste)


## Docker compose funktioniert nicht ##
Das kann mehrere Gründe haben, die häufigsten sind hier aufgeführt:

### Grund 1: Docker läuft nicht im Hintergrund ###
Der häufigste Grund ist der, dass der docker service nicht im Hintergrund läuft. Stell sicher, dass docker läuft. Standardmässig wird docker bei der Installation fragen, ob es automatisch bei systemstart gestartet werden soll. Wenn du dem nicht zugestimmt hast, dann starte docker selbst bevor du docker compose ausführst.

### Grund 2: Nicht genug Speicherplatz ###
Der zweite häufige Grund ist mangelnder Speicherplatz. Stell sicher, dass auf deiner Systemfestplatte genug Platz frei ist (etwa 5GB). Wenn du den Server häufig benutzt, macht es ab und zu sinn, ältere docker dateien zu löschen. Wenn du Docker Desktop installiert hast, dann kannst du das recht einfach über die GUI erledigen. Siehe dazu [Lösung: Reset](#lösung:-reset).

### Grund 3: Irgendwas ist beim erstellen der Dienste schief gegangen ###
Kann selten mal passieren, folge einfach den Anweisungen in  [Lösung: Reset](#lösung:-reset).

### Lösung: Reset ###
Stell sicher, dass keine Container laufen. In der Docker Desktop GUI, klick auf den oberen Button in der linken Seitenleiste ("Containers/Apps"). Beende alle Container die dort zu sehen sind und lösche diese. Danach klick auf "Images" in der linken Seitenleiste. Lösche auch hier alle. Danach dasselbe mit den "Volumes" darunter. Dann folge den Anweisungen im Kapitel [Installation](#installation) direkt nachdem Docker installiert wurde.

## Die IP unter Connection Info stimmt nicht ##
Das Problem ist bekannt und steht auf der "Todo" Liste. Ermittel die IP des Laptops auf dem der Server läuft manuell, z.B. über den Konsolenbefehl "ipconfig" unter windows oder "ifconfig" unter linux/ios.

## Die Drift-App findet den Server nicht ##
Schau ob du die richtige IP-Adresse verwendest (notfalls manuell ermitteln, siehe obiger Punkte). Wenn die Adresse korrekt ist, aber kein Rennen mit diesem Namen existiert, dann erscheint in der App ein rotes Kreuz. In dem Fall, einfach auf dem Server ein entsprechend benanntes Rennen erstellen.

## Die Zeiten im Racingserver stimmen nicht exakt mit denen in der App überein ##
Es kann vorkommen, dass die Zeiten um wenige Millisekunden unterschiedlich sind, bisher sind mir Unterschiede um die +- 0.004 Sekunden aufgefallen. Dieser Fehler ist bekannt und steht schon auf der "Todo" Liste.

## Ein Spieler steht doppelt in der Liste ##
Das kann vorkommen, wenn zwei Spieler den gleichen Namen gewählt haben oder die App zwischendurch mal vollständig aus gewesen ist, oder man auf ein anderes Smartphone gewechselt ist. Da die API aus rechtlichen Gründen nicht automatisch eure echten Sturmkind-Account namen rausgeben darf, verwenden wir für die Zuordnung ein ab und zu wechselndes Merkmal. Ich empfehle, pro Rennen das ihr fahrt entweder immer auch ein neues Rennen im Server anzulegen, oder aber zwischendurch den Reset-Knopf zu drücken. Ihr könnte aber unter der Liste auch gezielt nur bestimmte Spielernamen aus der Liste löschen.

# Drift Community API
