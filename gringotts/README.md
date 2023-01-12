# Gringotts The Game
### Video Demo: <https://youtu.be/56d1p4GJKJc>
### Description:
** This application is a terminal window game with Gringotts banking system and small quest **
** Functionality: **
- Vault balance, deposit and withdraw operations
- Wallet balance, deposit and withdraw operations
- Character creation
- Coins exchange
- Currency exchange
- Polyjuice potion making
- Buying goods (only 1 potion)
- Vault key stealing
- Stealing from other's vaults

### Files:
#### gringotts.py
##### Functions:
###### choose_option
**  Asking user to choose from currently available game options, returns chosen.
        User should input option index according to enumerated list of options.
        If user inputs invalid value function repromts, until value is valid option index.
        Returns string.
 **
 ###### take_action
** Takes chosen option and player name, making specific changes depending on chosen option.
        Changes values in database, global game variables including list of currently available options for user.
        Basically, changes current game-state.
 **
 ###### make_decision
**  Takes list of options(strings), returns chosen one(string) or none, if user inputs invalid index.
 **
 ##### Classes:
 ###### Vault
 **Represents wizard's vault.
        Contains values of coins in vault for current user, stores them in database
        and making changes to those values via methods.
    Methods in class:
        - __init__:
            Creates instance of class, gets values from database for current user.
        - __str__:
            String representation of instance object.
        - new:
            Inserts into database values for current user.
    ...
 **
 ###### Wallet
 **Represents wizard's wallet.
        Contains values of coins and currencies in wallet for current user, stores them in database
        and making changes to those values via methods.
        ...
 **
 ###### Wizard
 **Methods of this class making changes with user's parameters in database
 ...
 **
#### gringotts.db
** .schema **
** CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE wallets (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        owner_id INTEGER,
        galleons INTEGER NOT NULL DEFAULT 20,
        sickles INTEGER NOT NULL DEFAULT 30,
        knuts INTEGER NOT NULL DEFAULT 25, usd NUMERIC DEFAULT 0.00, gbp NUMERIC DEFAULT 0.00,
        FOREIGN KEY (owner_id) REFERENCES wizards(id));
CREATE TABLE wizards (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT NOT NULL, disguise TEXT DEFAULT NULL, status TEXT DEFAULT NULL, stolen_key TEXT DEFAULT NULL, potion INTEGER DEFAULT NULL);
CREATE TABLE vaults (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        depositor_id INTEGER,
        vault_key TEXT NOT NULL,
        galleons INTEGER NOT NULL DEFAULT 0,
        sickles INTEGER NOT NULL DEFAULT 0,
        knuts INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (depositor_id) REFERENCES wizards(id));
  **

** Table wizards contains info about registered players **
** Table vaults contains info about players bank accounts **
** Table wallets contains info about players coins and currencies in wallet **
