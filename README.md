# WANDS & WIZARDS SESSIONS v.0
#### Video Demo: <https://youtu.be/77x3hLF_m_w>
#### Description:
** This application is a tool for running W&W sessions online **
** Functionality: **
- Create sessions
- Join sessions
- Character creation
- Start/End sessions as GM
- Run session for players
- Message system (invites, notifications, requests)

#### Rules:
** Rules of this game created by [Murphen44](https://www.gmbinder.com/profile/murphen44) and can be found at the /rulebook route in this application.

#### Files:
##### app.py
** Main file, does all server logic, managing different application routes.**
###### "/"
** Homepage with information of current app version, introduction and explanation how to create, join and run sessions and play this game **
###### "/sessions/"
** At this route we can look at our existing sessions (via GET), and they are separated depending on role you took in the session. **
** GM role means that user created a session and will lead it for players and do the storytelling **
** Player role means that user was invited by GM, or requested to join the session. **
** Players need to create characters once they joined session and after that they will have character sheets with their features, ability scores etc. **
** GM manages sessions, can start, stop or end one. On the session page GM is able to affect players by events **
###### "/sessions/new"
** Form for creating new session, includes fields for session name, description and invitation (gm can immediately send invites to users by it) **

###### "/sessions/session/<session_name>"
** Route where session is running. **
** Content for GM: **
** Cards with players features, forms for doing events to players **
** Content for player: **
** Character sheet for logged player with full character info; cards with features for other party members **
** Most of the gameplay features of W&W are not implemented in this version, but core mechanics are there: character features, hp, ability scores **

##### helpers.py
###### login_required
** Helps to check if user logged in **
###### apology
** Returns error message and status code 400 **

##### myscript.js
** Client side, checks for correct input in registration form **
** Also at character creation page sends get request to the rulebook and fetches html code from it.
Then it finds elements with id's we looking for to asynchronously load them to page. **

##### session.js
** For GM: when GM submits one of the forms, sends POST request, prevents page reloading and makes changes on page **
** For player: when document loaded, sends get request to server every 3 seconds. If anything changed for players on server, updates data
asynchronously and add messages to session log **

##### wizards.db
** .schema **
** CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        username TEXT NOT NULL,
        hash TEXT NOT NULL,
        score INTEGER NOT NULL DEFAULT 0);
CREATE TABLE sqlite_sequence(name,seq);
CREATE UNIQUE INDEX username ON users (username);
CREATE TABLE sessions (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name VARCHAR(25) NOT NULL,
        gm_id INTEGER,
        started DATE,
        description VARCHAR(200) DEFAULT 'No description',
        FOREIGN KEY (gm_id) REFERENCES users(id));
CREATE TABLE players (player_id INTEGER,
        session_id INTEGER,
        character_name TEXT NOT NULL,
        character_level INTEGER DEFAULT 1, house VARCHAR(15), style VARCHAR(15), discipline VARCHAR(25), background VARCHAR(20), Strength SMALLINT, Dexterity SMALLINT, Intellect SMALLINT, Wisdom SMALLINT, Charisma SMALLINT, Constitution SMALLINT, cur_hp SMALLINT,
        FOREIGN KEY (player_id) REFERENCES users(id),
        FOREIGN KEY (session_id) REFERENCES sessions(id));
CREATE TABLE messages (reciever_id INTEGER,
        sender_id INTEGER,
        session_id INTEGER,
        message TEXT,
        type VARCHAR(10),
        date DATETIME,
        FOREIGN KEY (reciever_id) REFERENCES users(id),
        FOREIGN KEY (sender_id) REFERENCES users(id)
        FOREIGN KEY (session_id) REFERENCES sessions(id));  **

** Table users contains info about registered users **
** Table sessions contains info about sessions started and referencing user who started session **
** Table players contains info about player characters, referencing users and sessions by id's **
** Table messages stores all messages which were sent, until some command removes them (for example when user react to message by clicking one of the options) **
