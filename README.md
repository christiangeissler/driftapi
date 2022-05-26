# Dr!ft Community API Racing Server #
[English Manual](README_EN.md)
 
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

Darauf sollte jede Menge Text in der Konsole erscheinen, sobald aber die Zeilen mit "Created" die auch bei der Installation erscheinen zu sehen sind, laufen die Dienste und der Server kann benutzt werden. Sie folgendes Kapitel zur Bedienung.

# Stop
Schließe das Konsolenfenster oder drücke im Konsolenfenster "Strg + C" um die laufenden Prozesse zu beenden. Die Eingabe des Befehls

>docker compose --profile racedisplay down

entfernt die container vom system und ist für ein sauberes Beenden empfohlen.

# Bedienung
Öffne einen Browser deiner Wahl und gib die folgende Adresse ein:

>localhost:8080

Du solltest ins Hauptmenü des Servers kommen, von wo aus du Rennen anlegen (Create New Game) oder zuvor angelegte Rennen aufrufen (Show Game) kannst. Hinweis: Sobald ein Rennen angelegt wurde, nimmt der Server Daten von der App entgegen, unabhängig davon, ob du das Browserfenster offen lässt oder welches Rennen du gerade anzeigst. Du kannst also ruhig mehrere Rennen erstellen die gleichzeitig von Spielern genutzt werden.

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
Das Problem ist bekannt und steht auf der "Todo" Liste. Ermittel die IP des Laptops auf dem der Server läuft manuell, z.B. über den Konsolenbefehl "ipconfig" unter windows oder "ifconfig" unter linux/ios. Dann öffne die datei ".env" im Hauptverzeichnis des Projektes und änder die Zeile

>STREAMLIT_HOSTNAME=127.0.0.1

so, dass statt der 127.0.0.1 deine Host-IP steht. Bei meinem Windows PC bekomme ich über den Befehl "ipconfig" z.B. mehrere verschiedene Netzwerkadressen angezeigt, die richtige darunter ist die unter "Ethernet-Adapter Ethernet", weil mein PC über Kabel an meinem WLAN-Router hängt. Wenn du mit dem PC direkt im WLAN bist, dann halte besser nach einem WIFI adapter Ausschau, wichtig ist aber, dass der adaptername kein "vEthernet" enthält, das ist nur ein virtueller netzwerkadapter von docker.

## Die Drift-App findet den Server nicht ##
Schau ob du die richtige IP-Adresse verwendest (notfalls manuell ermitteln, siehe obiger Punkte). Wenn die Adresse korrekt ist, aber kein Rennen mit diesem Namen existiert, dann erscheint in der App ein rotes Kreuz. In dem Fall, einfach auf dem Server ein entsprechend benanntes Rennen erstellen.

## Die Zeiten im Racingserver stimmen nicht exakt mit denen in der App überein ##
Es kann vorkommen, dass die Zeiten um wenige Millisekunden unterschiedlich sind, bisher sind mir Unterschiede um die +- 0.004 Sekunden aufgefallen. Dieser Fehler ist bekannt und steht schon auf der "Todo" Liste.

## Ein Spieler steht doppelt in der Liste ##
Das kann vorkommen, wenn zwei Spieler den gleichen Namen gewählt haben oder die App zwischendurch mal vollständig aus gewesen ist, oder man auf ein anderes Smartphone gewechselt ist. Da die API aus rechtlichen Gründen nicht automatisch eure echten Sturmkind-Account namen rausgeben darf, verwenden wir für die Zuordnung ein ab und zu wechselndes Merkmal. Ich empfehle, pro Rennen das ihr fahrt entweder immer auch ein neues Rennen im Server anzulegen, oder aber zwischendurch den Reset-Knopf zu drücken. Ihr könnte aber unter der Liste auch gezielt nur bestimmte Spielernamen aus der Liste löschen.

# Drift Community API
Die Dr!ft Community API ist der Kern der Entwicklung und die Sturmkind Dr!ft App ist so programmiert, dass sie mit Servern die diese API implementieren kommunizieren kann. Kern der Überlegung ist, dass die App meist keine konkrete Antwort erwartet, sondern einfach immer nur wenn etwas Interessantes passiert (ein Rennen eingestellt, gestartet oder beendet oder ein Barcode gelesen wird) eine kurze Nachricht an die eingestellte URI verschickt. Dieses Projekt zeigt euch im Grunde genommen, wie man auf Basis der API einen Racingserver implementieren kann.

Dazu gehören im Grunde genommen drei Komponenten: Eine Datenbank (MongoDB), ein Backend (driftapi-service) und ein Frontend (racedisplay-service). Über den weiter oben genannten Startbefehl startet docker diese drei Komponenten in kleinen virtuellen Maschinen, damit keine weitere Software auf dem Host-System installiert werden muss. Dadurch sollte man dieses projekt auch auf windows, ios und linux gleichermaßen ausführen können.

Für die Datenbank braucht es keinen weiteren Ordner, aber das Backend mit der implementierung der API und der Hintergrundlogik ist im Ordner /driftapi zu finden und das Frontend im Ordner /streamlit. Beide sind in Python geschrieben.

Langfristig wäre es besser, das ganze vollständig als Online-plattform zu implementieren und aus Gründen der Performanz eine tabellenbasierte Datenbank zu verwenden.

Die technische Beschreibung der API findest du in diesem Ordner in der Datei "openapi.json" oder wenn du den server startest, in grafisch ansprechenderer Form unter der adresse 

>localhost:8080/docs

Die OpenAPI datei kannst du z.B. auf [postman](https://www.postman.com/) oder [swagger.io](swagger.io) importieren um sie anzuschauen.

Wenn du darüber hinaus weitere Fragen hast, empfehle ich diese direkt im [Sturmkind Forum](https://community.sturmkind.com) in der entsprechenden Rubrik zur Community API zu stellen, damit von den Antworten dort auch andere profitieren können.

# Wie geht es weiter?
Mit der Veröffentlichung der Community API geht Sturmkind einen ersten Schritt in Richtung Multiplayerunterstützung. Aber der Weg ist noch lange nicht zuende, denn auch wenn man mit diesem Projekt hier einen ersten Racing-Server aufsetzen kann, so hat nicht jeder Nutzer Lust und Zeit, lokal einen eigenen Server zu betreiben. Wenn du selbst dich an der Weiterentwicklung oder einer Eigenentwicklung eines Servers versuchen möchtest, so bist du herzlich eingeladen, im Sturmkind Forum mit uns zu diskutieren, dein Projekt vorzustellen und dort auch Fragen zur API etc. zu stellen. Denn die Kernidee der API ist es gerade, dass wir als Community mit dieser alle Möglichen kreativen Dinge anstellen können.
