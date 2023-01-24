import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///wizards.db")

# Roles list
ROLES = ['player', 'gm']
# Houses list
HOUSES = ['Gryffindor', 'Ravenclaw', 'Hufflepuff', 'Slytherin']
#Styles list
STYLES = ['Willpower', 'Technique', 'Intellect']
# Disciplines list
DISCIPLINES = ['Charms', 'Jinxes-Hexes-and-Curses', 'Transfiguration', 'Healing', 'Divination', 'Magizoology']
# Backgrounds list
BACKGROUNDS = ['Artist', 'Bookworm', 'Dreamer', 'Groundskeeper', 'Potioneer', 'Protector', 'Quidditch-fan', 'Socialite', 'Troublemaker']

# Count modifier
def modifier(i):
    return int((i - 10)/2 - (i-10)/2%1)
# Scores list
SCORES = {i: modifier(i) for i in range(1, 31)}
# [{i:mod[i]} for i in range(1,31)]
#Ability points and cost (max summary cost = 27)
def cost(i):
    if i <= 13:
        return (i-8)
    return ((i-13)*2 + 5)
POINTS = {i: cost(i) for i in range(8, 16)}
# Abilities list
ABILITIES = ['Strength', 'Dexterity', 'Intellect', 'Wisdom', 'Charisma', 'Constitution']
# Hit dice, hit points
HITS = {'willpower': {'hit dice': 'd10', 'hp_1': 10, 'hp_after': 6},
    'technique': {'hit dice': 'd6', 'hp_1': 6, 'hp_after': 4},
    'intellect': {'hit dice': 'd8', 'hp_1': 8, 'hp_after': 5}}

# Skills
SKILLS = {'willpower': ['Athletics', 'Deception', 'Intimidation', 'Magical Theory',
    'Persuasion', 'Sleight of Hand', 'Survival'],
    'technique': ['Acrobatics', 'Herbology', 'Insight', 'Perception', 'Potion Making',
    'Sleight of Hand', 'Stealth'],
    'intellect': ['Acrobatics', 'Herbology', 'Insight', 'Investigation', 'Magical Creatures',
    'Magical Theory', 'Medicine', 'Muggle Studies', 'Survival']}

# Get messages
def get_invites():
    try:
        user_id = session["user_id"]
    except:
        return
    messages = db.execute("SELECT COUNT(message) AS count FROM messages, users WHERE messages.reciever_id = users.id AND users.id = ?;", user_id)
    count = messages[0]["count"]
    print(count)
    return count


# Check if session is running
def check_session():
    try:
        if session["session_id"]:
            rows = db.execute("SELECT name FROM sessions WHERE id = ?", session["session_id"])
            session_name = rows[0]["name"]
            return session_name
    except:
        return None


@app.route("/")
def index():
    """Homepage"""

    return render_template("index.html", count=get_invites(), s_name=check_session())

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check all fields
        if not username:
            return apology("must provide username")
        elif not password:
            return apology("must provide password")
        elif not confirmation:
            return apology("Passwords must match")
        elif confirmation != password:
            return apology("Passwords must match")

        # Query database for username in case already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username not exists
        if len(rows) != 0:
            return apology("username already exists")
        # Check password
        if len(password) < 4:
            return apology("weak password")
        # Add new user to database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))

        # Auto log in
        session.clear()
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    # Access via GET
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/sessions/", methods=["GET", "POST"])
@login_required
def sessions():
    user_id = session["user_id"]

    if request.method == "POST":
        decision = request.form.get("decision")
        session_name = request.form.get("session_name")

        # If gm wants to start session check if at least 2 players joined session
        if decision == "start":
            try:
                if session["session_id"]:
                    return apology("You already started a session. Stop it to start a new one")
            except:
                pass
            count = db.execute("SELECT player_id, character_name FROM players, sessions WHERE players.session_id = sessions.id AND name = ?", session_name)
            if len(count) < 2:
                return apology("You need to have at least two players to start")
            # Check if all players created their characters
            for p in count:
                if p['character_name'] == 'New player':
                    return apology('One or more of your players havent created character')

            # Select message recievers
            recievers = db.execute("SELECT player_id, session_id FROM players, sessions WHERE players.session_id = sessions.id AND name = ?;", session_name)
            # Store session_id in user's flask session
            session["session_id"] = recievers[0]["session_id"]
            session["role"] = "gm"
            # Generate message
            message = 'Session ' + session_name + ' has started! You can now connect to session.'
            for row in recievers:
                p_id = row["player_id"]
                s_id = row["session_id"]
                # Send messages to players to inform that session started
                db.execute("INSERT INTO messages (reciever_id, sender_id, session_id, message, type, date) VALUES ( ?, ?, ?, ?, 'start', ?);", p_id, user_id, s_id, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            # Delete stop messages
            db.execute("DELETE FROM messages WHERE type = 'stop' AND session_id = ?", session.get('session_id'))
            # Redirect to session page
            print(session)
            print(session_name)
            return redirect(url_for(".session_play", session_name=session_name))

        # If GM wants to end session
        if decision == "end":
            # Select message recievers
            recievers = db.execute("SELECT player_id, session_id FROM players, sessions WHERE players.session_id = sessions.id AND name = ?;", session_name)
            # Generate message
            message = 'Session ' + session_name + ' was closed by GM!'
            for row in recievers:
                p_id = row["player_id"]
                # Send messages to players to inform that session ended
                db.execute("INSERT INTO messages (reciever_id, sender_id, message, type, date) VALUES ( ?, ?, ?, 'end', ?);", p_id, user_id, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            # DELETE messages connected to session (except of type end) if any
            try:
                db.execute("DELETE FROM messages WHERE session_id = ?;", recievers[0]["session_id"])
            except:
                pass
            # Delete players from session if any
            try:
                db.execute("DELETE FROM players WHERE session_id = ?;", recievers[0]["session_id"])
            except:
                pass
            # Delete session
            db.execute("DELETE FROM sessions WHERE name = ?", session_name)
            try:
                session.pop("session_id")
                session.pop("role")
            except:
                pass
            return redirect("/sessions/")

        #If player wants to create character
        if decision == 'create':
            return redirect(url_for(".create_character", session_name=session_name, user_id=user_id))

    # Sessions where user participating as GM
    gm_sessions = db.execute("SELECT id, name AS [Session name], description AS Description, started AS Started FROM sessions WHERE gm_id = ?;", user_id)
    for row in gm_sessions:
        count = db.execute("SELECT COUNT(player_id) AS p FROM players WHERE session_id = ?", row["id"])
        row["Joined"] = str(count[0]["p"])
        del row["id"]
    # Sessions where user participating as player
    player_sessions = db.execute("SELECT name AS [Session name], started AS Started, character_name AS Name, character_level AS Level FROM sessions, players, users WHERE sessions.id = players.session_id AND players.player_id = users.id AND users.id = ?;", user_id)
    for row in player_sessions:
        count = db.execute("SELECT COUNT(player_id) AS p FROM players, sessions WHERE players.session_id = sessions.id AND name = ?", row["Session name"])
        row["Joined"] = str(count[0]["p"])

    no_res = None
    if len(gm_sessions) == 0 and len(player_sessions) == 0:
        no_res = "You are not participating in any session yet. Join any existing session, or create your own!"

    return render_template("sessions.html", gm_sessions=gm_sessions, player_sessions=player_sessions, no_res=no_res, count=get_invites(), s_name=check_session())


@app.route("/sessions/new", methods=["GET", "POST"])
@login_required
def new_session():
    user_id = session["user_id"]
    session_names = db.execute("SELECT name FROM sessions")

    if request.method == "POST":
        name = request.form.get('session_name')
        if not name:
            return apology("Provide session name")
        if len(name) > 25:
            name = name[0:24]
        description = request.form.get('description')
        if not description:
            description = 'No description'
        if len(description) > 200:
            description = description[0:199]

        # Need to check here for valid usernames
        # Get usernames from invites
        invites = request.form.get('invites')
        invites = invites.split(',')
        invites = [invite.strip() for invite in invites]
        print(invites)

        for row in session_names:
            if row['name'] == name:
                return apology("Session with that name already exists")
        # Need to check here for max num of sessions as GM
        # Create new session
        db.execute("INSERT INTO sessions (name, gm_id, started, description) VALUES (?, ?, ?, ?);", name, user_id, datetime.now().strftime("%Y-%m-%d"), description)
        # Get session id
        rows = db.execute("SELECT id FROM sessions WHERE name = ?", name)
        session_id = rows[0]["id"]
        #Select invite recievers
        recievers = db.execute("SELECT id FROM users WHERE username IN (?)", invites)
        # Send invites
        for row in recievers:
            reciever_id = row['id']
            # Get sender username
            rows = db.execute("SELECT username FROM users WHERE id = ?", user_id)
            username = rows[0]['username']
            # Create messages in database
            message = 'You were invited by ' + username + ' to join ' + name + ' session!'
            print(message)
            db.execute("INSERT INTO messages (reciever_id, sender_id, session_id, message, type, date) VALUES ( ?, ?, ?, ?, 'invite', ?);", reciever_id, user_id, session_id, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        return redirect("/sessions/")

    return render_template("new_session.html", session_names=session_names)


@app.route("/sessions/session/<session_name>", methods=["GET", "POST"])
@login_required
def session_play(session_name):
    """Session page"""
    user_id = session["user_id"]
    print(session_name)
    # Access via POST
    if request.method == "POST":
        player_id = request.form.get('player_id')
        decision = request.form.get('decision')
        # If GM wants to stop session
        if decision == 'stop':
            rows_p = db.execute("SELECT player_id FROM players WHERE session_id = ?", session['session_id'])
            # Send stop message
            for p in rows_p:
                db.execute("INSERT INTO messages (sender_id, reciever_id, session_id, type) VALUES (?, ?, ?, 'stop')", user_id, p['player_id'], session['session_id'])

            # Delete start messages
            db.execute("DELETE FROM messages WHERE session_id = ? AND type = 'start'", session['session_id'])
            # Remove session parameters from flask session
            session.pop('role')
            session.pop('session_id')
            return redirect("/")

        # If player leaves stopped session
        if decision == 'leave':
            # Delete stop message
            db.execute("DELETE FROM messages WHERE type = 'stop' and reciever_id = ? and session_id = ?", user_id, session.get('session_id'))
            # Remove session parameters from flask session
            session.pop('role')
            session.pop('session_id')
            return redirect("/")

        level = request.form.get('level')
        # If GM leveled up character
        if level == 'level':
            # Level up character and update hp
            rows_lv = db.execute("SELECT character_level, style, Constitution FROM players WHERE player_id = ? AND session_id = (SELECT id FROM sessions WHERE name = ?)", player_id, session_name)
            lv = rows_lv[0]['character_level']
            st = rows_lv[0]['style']
            con = rows_lv[0]['Constitution']
            # Set current hp to new max value (lv instead (lv-1) because we haven't updated level yet)
            cur_hp = HITS[st]['hp_1'] + SCORES[con] + lv*(HITS[st]['hp_after'] + SCORES[con])
            db.execute("UPDATE players SET character_level = character_level + 1, cur_hp = ? WHERE player_id = ? AND session_id = (SELECT id FROM sessions WHERE name = ?)", cur_hp, player_id, session_name)

        dmg_hl = request.form.get('dmg_hl')
        # If damage/heal form was activated
        if dmg_hl:
            num = request.form.get('num')
            rows = db.execute("SELECT cur_hp FROM players, sessions WHERE player_id = ? AND players.session_id = sessions.id AND name = ?", player_id, session_name)
            cur_hp = rows[0]['cur_hp']
            print(cur_hp)
            # Check if character got damage or heal
            if dmg_hl == 'd':
                cur_hp = cur_hp - int(num)
                print(cur_hp)
            elif dmg_hl == 'h':
                cur_hp = cur_hp + int(num)
            else:
                return redirect(url_for(".session_play", session_name=session_name))
            # Set current hp
            db.execute("UPDATE players SET cur_hp = ? WHERE player_id = ? AND session_id = (SELECT id FROM sessions WHERE name = ?)", cur_hp, player_id, session_name)

        return redirect(url_for(".session_play", session_name=session_name))

    # Access via GET
    # Check if user allowed to session
    s_rows = db.execute("SELECT id FROM sessions WHERE name = ?", session_name)
    session_id = session.get('session_id')
    if session_id != s_rows[0]['id']:
        return redirect("/")
    # Get role
    role = session.get('role')

    # Get players data
    players = db.execute("SELECT player_id, character_name AS Name, character_level AS Level, house AS House, style AS [Casting Style], discipline AS Discipline, background AS Background FROM players, sessions WHERE players.session_id = sessions.id AND name = ?", session_name)
    stats = db.execute("SELECT player_id, Strength, Dexterity, Intellect, Wisdom, Charisma, Constitution, cur_hp FROM players, sessions WHERE players.session_id = sessions.id AND name = ?", session_name)
    # Get GM data
    gm_rows = db.execute("SELECT username FROM users, sessions WHERE users.id = sessions.gm_id AND name = ?", session_name)
    gm = gm_rows[0]['username']
    # Get stop message if sent
    stop = 0
    try:
        stop_message = db.execute("SELECT type FROM messages WHERE type = 'stop' AND reciever_id = ? AND session_id = ?", user_id, session['session_id'])
        if len(stop_message) != 0:
            stop = 1
    except:
        pass
    return render_template("session_play.html", players=players, stats=stats, gm=gm, session_name=session_name, user_id=user_id, scores=SCORES, role=role, hits=HITS, stop=stop)


@app.route("/sessions/session/<session_name>/character/<user_id>", methods=["GET", "POST"])
@login_required
def create_character(session_name, user_id):
    """Character creation page"""
    user_id = session['user_id']
    if request.method == "POST":
        # Get and check user input
        character_name = request.form.get('character_name')
        if not character_name:
            return apology('Provide character name')
        house = request.form.get('house')
        if house not in [item.lower() for item in HOUSES]:
            return apology('Unexisting house')
        style = request.form.get('style')
        if style not in [item.lower() for item in STYLES]:
            return apology('Unexisting casting style')
        discipline = request.form.get('discipline')
        if discipline not in [item.lower() for item in DISCIPLINES]:
            return apology('Unexisting school of magic')
        background = request.form.get('background')
        if background not in [item.lower() for item in BACKGROUNDS]:
            return apology('Unexisting background')
        session_name = request.form.get('session_name')
        # Get stats from form, add house bonuses
        try:
            stats = {stat: (int(request.form.get(stat[0:3])) + int(request.form.get('add_'+ stat[0:3]))) for stat in ABILITIES}
        except:
            return apology('Ability values must be integers')
        print(stats)
        # Add +1 to chosen ability score
        addition = request.form.get('add_score')
        if not addition:
            return apology('Select ability to upgrade')
        stats[addition] += 1
        s = ''
        # Check values and make string for adding to sql query
        for stat in stats:
            if stats[stat] < 8 or stats[stat] > 17:
                return apology('Wrong ability value')
            s += stat + ' = ' + str(stats[stat]) + ', '
        print(s)
        # Set hitpoints
        for key in HITS:
            if style == key:
                #upd v_1
                cur_hp = HITS[key]['hp_1'] + SCORES[stats['Constitution']]
        # Get session_id
        rows = db.execute("SELECT id FROM sessions WHERE name = ?", session_name)
        session_id = rows[0]['id']

        # Store character data in database
        query = 'UPDATE players SET ' + s + 'character_name = ?, house = ?, style = ?, discipline = ?, background = ?, cur_hp = ? WHERE player_id = ? AND session_id = ?'
        db.execute(query, character_name, house, style, discipline, background, cur_hp, user_id, session_id)
        return redirect("/sessions/")

    level = db.execute("SELECT character_level FROM players, sessions WHERE players.session_id = sessions.id AND player_id = ? AND name = ?", user_id, session_name)
    if level[0]['character_level'] != 1:
        return apology('You can edit only first-level character')
    return render_template("create_character.html", user_id=user_id, session_name=session_name, houses=HOUSES, styles=STYLES, disciplines=DISCIPLINES, backgrounds=BACKGROUNDS, abilities=ABILITIES)


@app.route("/messages", methods=["GET", "POST"])
@login_required
def messages():
    user_id = session["user_id"]

    if request.method == "POST":
        decision = request.form.get('decision')
        # Invites (join or reject)
        if decision == 'join':
            session_name = request.form.get('session_name')
            rows = db.execute("SELECT id FROM sessions WHERE name = ?", session_name)
            session_id = rows[0]['id']
            # Check if already joined
            player = db.execute("SELECT player_id FROM players WHERE session_id = ? AND player_id = ?;", session_id, user_id)
            if player:
                # Delete message
                db.execute("DELETE FROM messages WHERE reciever_id = ? AND session_id = ? AND type = 'invite';", user_id, session_id)
                return apology("You already joined this session")
            # Need to check here for max num of players and max num of sessions as player
            # Add new player to session
            db.execute("INSERT INTO players (player_id, session_id, character_name) VALUES (?, ?, 'New player');", user_id, session_id)
            # Remove invite
            db.execute("DELETE FROM messages WHERE reciever_id = ? AND session_id = ?;", user_id, session_id)
            return redirect("/sessions/")
        elif decision == 'reject':
            session_name = request.form.get('session_name')
            rows = db.execute("SELECT id FROM sessions WHERE name = ?", session_name)
            session_id = rows[0]['id']
            # Remove invite
            db.execute("DELETE FROM messages WHERE reciever_id = ? AND session_id = ? AND type = 'invite';", user_id, session_id)
            return redirect("/")
        # Notification about ended session
        elif decision == 'ok':
            # Actually deletes all messages about ended sessions(because session already deleted and we have no info about session id)
            # Might change code later
            db.execute("DELETE FROM messages WHERE reciever_id = ? AND type = 'end';", user_id)
            return redirect("/messages")
        elif decision == 'connect':
            session_name = request.form.get('session_name')
            rows = db.execute("SELECT id FROM sessions WHERE name = ?", session_name)
            session_id = rows[0]['id']
            # Store session_id in user's flask session
            try:
                if session["session_id"] != session_id:
                    return apology("You are already playing in another session")
            except:
                pass
            session["session_id"] = session_id
            session["role"] = "player"
            print(session_name)
            return redirect(url_for(".session_play", session_name=session_name))
        elif decision == 'yes' or decision == 'no':
            session_name = request.form.get('session_name')
            rows = db.execute("SELECT id FROM sessions WHERE name = ?", session_name)
            session_id = rows[0]['id']
            p_id = request.form.get('sender')
            if decision == 'yes':
                # Check if user already joined
                player = db.execute("SELECT player_id FROM players WHERE session_id = ? AND player_id = ?;", session_id, p_id)
                if player:
                    # Delete message
                    db.execute("DELETE FROM messages WHERE reciever_id = ? AND sender_id = ? AND session_id = ? AND type = 'ask';", user_id, p_id, session_id)
                    return apology("User already joined session")
                # Add player
                db.execute("INSERT INTO players (player_id, session_id, character_name) VALUES (?, ?, 'New player');", p_id, session_id)
                # Need to add approval message later

            # Delete message
            db.execute("DELETE FROM messages WHERE reciever_id = ? AND sender_id = ? AND session_id = ? AND type = 'ask';", user_id, p_id, session_id)
            return redirect("/messages")

        # Decision somehow different
        else:
            return apology("Incorrect input")

    invites = db.execute("SELECT message AS Invite, name, description, type FROM messages, users, sessions WHERE messages.reciever_id = users.id AND users.id = ? AND messages.session_id = sessions.id AND type = 'invite';", user_id)
    start_messages =  db.execute("SELECT message AS Notification, name, description, type FROM messages, sessions WHERE reciever_id = ? AND messages.session_id = sessions.id AND type = 'start';", user_id)
    end_messages = db.execute("SELECT message AS Notification, type FROM messages WHERE reciever_id = ? AND type = 'end';", user_id)
    requests = db.execute("SELECT sender_id, message AS Request, name, type FROM messages, sessions WHERE reciever_id = ? AND messages.session_id = sessions.id AND type = 'ask';", user_id)
    return render_template("messages.html", invites=invites, start_messages=start_messages, end_messages=end_messages, requests=requests)


@app.route("/join", methods=["GET", "POST"])
@login_required
def join():
    user_id = session["user_id"]
    # Access via POST
    if request.method == "POST":
        decision = request.form.get('decision')
        print(decision)
        if decision != 'ask':
            return apology("Wrong input")
        session_name = request.form.get('session_name')
        # Find session and GM ids
        ids = db.execute("SELECT id, gm_id FROM sessions WHERE name = ?;", session_name)
        # Get username
        username = db.execute("SELECT username FROM users WHERE id = ?", user_id)
        # Format message
        message = username[0]["username"] + ' wants to join your ' + session_name + ' session. Do you agree?'
        print(message)
        # Send request to GM
        db.execute("INSERT INTO messages (sender_id, reciever_id, session_id, message, type, date) VALUES (?, ?, ?, ?, 'ask', ?);", user_id, ids[0]["gm_id"], ids[0]["id"], message, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return redirect("/join")

    # Access via GET
    # Select all sessions, except those where user already gm or player
    other_sessions = db.execute("SELECT id, name AS [Session name], description AS Description, started AS Started, gm_id FROM sessions WHERE gm_id != ? AND id NOT IN (SELECT session_id FROM players WHERE player_id = ?)  ORDER BY started DESC;", user_id, user_id)
    for row in other_sessions:
        gm = db.execute("SELECT username FROM users WHERE id = ?", row["gm_id"])
        row["GM"] = gm[0]["username"]
        del row["gm_id"]
        count = db.execute("SELECT COUNT(player_id) AS p FROM players WHERE session_id = ?", row["id"])
        row["Joined"] = str(count[0]["p"])
        del row["id"]

    no_res = None
    if len(other_sessions) == 0:
        no_res = "No sessions to join yet"

    return render_template("join.html", other_sessions=other_sessions, no_res=no_res)

@app.route("/rulebook")
def rulebook():
    return render_template("rulebook.html")