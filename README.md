# Flask To-Do App 
*Eksempel på kobling mellom Flask og MariaDB.*

## Oppgaver
1. **Få til å kjøre appen.** Følg forberedelsene nedenfor (MariaDB og Python). Du skal kunne åpne appen i nettleseren din og legge til oppgaver.
2. **Forklar hvordan koden virker.** Erstatt alle kommentarene i ```app.py``` og ```index.html``` med svar på spørsmålene. Skriv selv med egne ord, men bruk gjerne AI til å forstå.
3. **Samarbeid med læringspartner** og se om dere klarer å bruke hverandres databaser.
4. **Utvide programmet.** Se forslag til utvidelser nederst.

## Forberedelser 
### MariaDB 
```CREATE DATABASE todo;```

Lag eller velg en databasebruker du vil bruke. Bytt ut informasjonen under ```conn``` i ```app.py``` med riktig innloggingsinformasjon (IP-adresse, brukernavn, passord, og eventuelt databasenavn hvis du ikke bruker *todo*).
* Hvis du kjører Python-koden og databasen på forskjellige maskiner, må du erstatte ```localhost``` med IP-adressen til maskinen hvor databasen ligger.

### Python
Åpne terminalen der ```app.py``` ligger og kjør:
```
pip install flask
pip install mysql-connector-python
python3 app.py (på linux) | python app.py (på windows)
```
Appen skal da starte på http://localhost:5000.

## Utvidelser
Enkel
* Legg til litt CSS-design
* Sorter oppgavene alfabetisk med SQL
* Vis en melding hvis lista er tom med Jinja ( {% if not tasks %}... )
* Skjul databaseinformasjonen i en .env-fil (se egen oppgave i Teams)

Middels
* Legg til ny kolonne for “fullført”, og la brukeren krysse av
* Lag kategorier eller tags for oppgaver

Vanskelig
* Lag innlogging og registrering av brukere
* Legg til søkefelt
* Koble appen til et annet tema (filmer, spill, kurs osv.)

## Tips
Du kan gjenbruke og tilpasse denne koden i et annet prosjekt. Kanskje som årsoppgave?

Prøv å forstå hvordan Flask og databasen snakker sammen. Når du får det til, kan du lage nesten hva som helst.

## Feilsøking
### ```1273 (HY000): Unknown collation: 'utf8mb4_0900_ai_ci'```
**Hva skjer**: MySQL-connector prøver å bruke en collation (tekstsortering) som ikke finnes i MariaDB.
**Løsning**: endre get_connection slik:
```
def get_connection():
    return mysql.connector.connect(
        # Bytt ut informasjonen her med dine egne verdier:
        host='127.0.0.1',
        user='todo_user',       
        password='strongpassword',
        database='todo',
        charset='utf8mb4',
        collation='utf8mb4_general_ci'
    )
```

Dette forteller Python hvordan tekst skal lagres og sammenlignes i databasen. 

---
### ```ModuleNotFoundError: No module named 'flask'```
**Hva skjer**: Flask (eller MySQL-biblioteket) er ikke installert i miljøet ditt.
**Løsning**: installer nødvendige pakker
```
pip install flask mysql-connector-python
```

---
### Koble til database på en annen maskin

Hvis Flask-appen og databasen kjører på forskjellige maskiner, må to ting sjekkes.

1. Eksterne tilkoblinger må tillates i MariaDB. 
På Linux, åpne konfigurasjon med:

``` sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf ```
 
Finn linjen som begynner med bind-address og endre den til ```bind-address = 0.0.0.0``` for å tillate eksterne tilkoblinger.
Deretter lagre (Ctrl + O, Enter, Ctrl + X) og restart MariaDB:
   
``` sudo systemctl mariadb restart ```

2. Du må kanskje definere port i Flask-koden
```
def get_connection():
    return mysql.connector.connect(
        host='192.168.10.45', 
        port=3306,
        user='todo_user',
        password='strongpassword',
        database='todo',
        charset='utf8mb4',
        collation='utf8mb4_general_ci'
    )

```
3. Du må sørge for at du bruker en databasebruker som har alle tilganger også på andre IP-adresser, ikke bare på localhost.

4. Kanskje må du også gjøre noe med brannmuren...?