import sys
from cs50 import SQL
from random import choice
from pyfiglet import Figlet

# Configure figlet
figlet = Figlet(font='coinstak')


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///gringotts.db")
# Game options menu
options = {'Go to Gringotts': True, 'Check wallet': True, 'Leave Gringotts': False, 'Vault balance': False,
    'Deposit to vault': False, 'Withdraw from vault': False, 'Go to vault': False, 'Buy polyjuice potion': True,
    'Collect hair for potion': False, 'Change coins': False, 'Currency exchange': False,
    'Drink polyjuice potion': False, 'Steal key': True, 'Exit game': True}
# Player location
location = 'home'

COINS = ['galleons', 'sickles', 'knuts']
CURRENCIES = {'usd':{'galleons': 24.65, 'sickles': 1.45, 'knuts': 0.05},
    'gbp':{'galleons': 19.72, 'sickles': 1.16, 'knuts': 0.04}}
PRICES = {'polyjuice': {'galleons': 5, 'sickles': 0, 'knuts': 0}}

def main():
    name = input('Your name: ')
    # Check if wizard already in database
    wizard = Wizard.get(name)
    # If not, store him in database, create new vault and wallet
    if not wizard:
        Wizard.new(name)
    while True:
        take_action(choose_option(), name)


def choose_option():
    """Asking user to choose from currently available game options, returns chosen.
        User should input option index according to enumerated list of options.
        If user inputs invalid value function repromts, until value is valid option index.
        Returns string.
    """
    available = [option for option in options if options[option] not in [0, False, None]]
    print('\nActions available: ')
    for i, option in enumerate(available, start=1):
        print(f'{i}: {option}')
    while True:
        try:
            option_index = int(input('Action: ')) - 1
            if option_index in range(len(available)):
                print('')
                return available[option_index].lower()
            else:
                print('Not an available action!')
        except:
            print('Not an available action!')


def generate_key():
    """Generates string of 10 random digits"""
    nums = [i for i in range(10)]
    key = ''
    for _ in range(10):
        key += str(choice(nums))
    return key


def take_action(action, name):
    """Takes chosen option and player name, making specific changes depending on chosen option.
        Changes values in database, global game variables including list of currently available options for user.
        Basically, changes current game-state.
    """
    global location
    match action:
        case "go to gringotts":
            print("""
            ⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣿⣿⣷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⣿⣿⣿⠋⣉⣉⠙⣿⣿⣿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣤⣶⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣶⣤⡀⠀⠀⠀
⠀⠀⠀⣤⣤⣤⣤⣤⡄⠀⠀⠀⢀⣠⣿⣿⣤⣤⣄⡀⠀⢠⣤⣤⣤⣤⣤⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⠀⠀⠀⢀⣴⣿⡿⠛⠛⠛⠛⠛⠇⠀⠀⠀⣿⣿⣿⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⠀⠀⠀⣸⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⠀⠀⠀⣿⣿⠀⠀⠀⠀⢠⣤⣤⣤⠀⠀⠀⣿⣿⣿⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⠀⠀⠀⢹⣿⣆⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⣿⣿⣿⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⠀⠀⠀⠀⠻⣿⣷⣤⣤⣤⣤⣾⣿⠀⠀⠀⣿⣿⣿⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⠀⠀⠀⠀⠀⠈⠙⣿⣿⠛⠛⠉⠁⠀⠀⠀⣿⣿⣿⠀⠀⠀⠀
⠀⠀⠀⠛⠛⠛⠛⠛⠃⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀⠘⠛⠛⠛⠛⠛⠀⠀⠀
⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠉⠉⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀
⠀⢰⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⡆⠀
⠀⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠁⠀
            """)
            person = Wizard.check_disguise(name)
            print(f"Greetings, Mr(s). {person}. What can we do for you?\n")
            options['Go to Gringotts'] = False
            options['Buy polyjuice potion'] = False
            options['Vault balance'] = True
            options['Go to vault'] = True
            options['Steal key'] = False
            options['Leave Gringotts'] = True
            options['Change coins'] = True
            options['Currency exchange'] = True
            location = 'bank'
        case "vault balance":
            person = Wizard.check_disguise(name)
            print(Vault(person))
        case "go to vault":
            # Checking disguise
            person = Wizard.check_disguise(name)
            # Checking stolen key
            key = Wizard.check_key(name, person)
            location = 'vault'
            # If player disguised and stolen vault key
            if person != name and key:
                print("""When your cart moving through thief's downfall,
it removes Polyjuice potion effect. Then cart derails
and you are falling down""")
                spell = input('Cast a spell: ').lower()
                if spell != 'arresto momentum':
                    Wizard.kill(name)
                    print('You died!')
                    print(figlet.renderText('Game over'))
                    sys.exit()
                else:
                    print('You saved yourself!')
            elif person != name and not key:
                print(f"You don't have key from {person}'s vault")
                location = 'bank'
            if location == 'vault':
                options['Go to vault'] = False
                options['Deposit to vault'] = True
                options['Withdraw from vault'] = True
                options['Change coins'] = False
                options['Currency exchange'] = False
        case "deposit to vault":
            person = Wizard.check_disguise(name)
            try:
                coins = {'galleons': int(input('Galleons: ')), 'sickles': int(input('Sickles: ')),
                    'knuts': int(input('Knuts: '))}
                Vault.deposit(coins, person)
                Wallet.withdraw(coins, name)
            except:
                print('Invalid value')
        case "withdraw from vault":
            person = Wizard.check_disguise(name)
            try:
                coins = {'galleons': int(input('Galleons: ')), 'sickles': int(input('Sickles: ')),
                    'knuts': int(input('Knuts: '))}
                Vault.withdraw(coins, person)
                Wallet.deposit(coins, name)
            except:
                print('Invalid value')
        case "check wallet":
            print(Wallet(name))
        case "leave gringotts":
            options['Go to Gringotts'] = True
            options['Buy polyjuice potion'] = True
            options['Vault balance'] = False
            options['Go to vault'] = False
            options['Steal key'] = True
            options['Leave Gringotts'] = False
            options['Change coins'] = False
            options['Currency exchange'] = False
            options['Deposit to vault'] = False
            options['Withdraw from vault'] = False
            person = Wizard.check_disguise(name)
            # If player disguised
            if person != name and location == 'vault':
                print("""
        ⣰⠂⠀⣼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡟⢆⢠⢣⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡘⡇⠹⢦⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠹⣦⣹⢸⡖⠤⢀⠀⠘⢿⠛⢔⠢⡀⠃⠣⠀⠇⢡⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠹⠀⡷⣄⠠⡈⠑⠢⢧⠀⢢⠰⣼⢶⣷⣾⠀⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠤⢖⡆⠰⡙⢕⢬⡢⣄⠀⠑⢼⠀⠚⣿⢆⠀⠱⣸⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣤⡶⠮⢧⡀⠑⡈⢢⣕⡌⢶⠀⠀⣱⣠⠉⢺⡄⠀⢹⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⡸⠀⠈⡗⢄⡈⢆⠙⠿⣶⣿⠿⢿⣷⣴⠉⠹⢶⢾⡆⠀⠀⠀
⠀⠀⠀⢠⠶⠿⡉⠉⠉⠙⢻⣮⡙⢦⣱⡐⣌⠿⡄⢁⠄⠑⢤⣀⠐⢻⡇⠀⠀⠀
⠀⠀⠀⢀⣠⠾⠖⠛⢻⠟⠁⢘⣿⣆⠹⢷⡏⠀⠈⢻⣤⡆⠀⠑⢴⠉⢿⣄⠀⠀
⠀⠀⢠⠞⢃⢀⣠⡴⠋⠀⠈⠁⠉⢻⣷⣤⠧⡀⠀⠈⢻⠿⣿⡀⠀⢀⡀⣸⠀⠀
⠀⠀⢀⠔⠋⠁⡰⠁⠀⢀⠠⣤⣶⠞⢻⡙⠀⠙⢦⠀⠈⠓⢾⡟⡖⠊⡏⡟⠀⠀
⠀⢠⣋⢀⣠⡞⠁⠀⠔⣡⣾⠋⠉⢆⡀⢱⡀⠀⠀⠀⠀⠀⠀⢿⡄⠀⢇⠇⠀⠀
⠀⠎⣴⠛⢡⠃⠀⠀⣴⡏⠈⠢⣀⣸⣉⠦⣬⠦⣀⠀⣄⠀⠀⠈⠃⠀⠀⠙⡀⠀
⠀⡸⡁⣠⡆⠀⠀⣾⠋⠑⢄⣀⣠⡤⢕⡶⠁⠀⠀⠁⢪⠑⠤⡀⠀⢰⡐⠂⠑⢀
⠀⠏⡼⢋⠇⠀⣸⣟⣄⠀⠀⢠⡠⠓⣿⠇⠀⠀⠀⠀⠀⠑⢄⡌⠆⢰⣷⣀⡀⢸
⠀⣸⠁⢸⠀⢀⡿⡀⠀⠈⢇⡀⠗⢲⡟⠀⠀⠀⠀⠀⠀⠀⠀⠹⡜⠦⣈⠀⣸⡄
⠀⣧⠤⣼⠀⢸⠇⠉⠂⠔⠘⢄⣀⢼⠃⡇⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠚⠳⠋⠀
⠐⠇⣰⢿⠀⣾⢂⣀⣀⡸⠆⠁⠀⣹⠀⢡⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⡏⣸⠀⣟⠁⠀⠙⢄⠼⠁⠈⢺⠀⠘⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠈⡏⣸⢰⡯⠆⢤⠔⠊⢢⣀⣀⡼⡇⠀⠹⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢠⢻⢸⡇⠀⠀⠑⣤⠊⠀⠀⠈⣧⠀⠀⠙⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠸⣼⢸⠟⠑⠺⡉⠈⢑⠆⠠⠐⢻⡄⠀⠀⠈⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡟⣸⡀⠀⠀⣈⣶⡁⠀⠀⠀⢠⢻⡄⠀⠀⠀⠑⠤⣄⡀⠀⠀⠀⠀⠀⠀
⠀⠀⢰⠁⣿⡿⠟⢏⠁⠀⢈⠖⠒⠊⠉⠉⠹⣄⠀⠀⠀⠀⠀⠈⠑⠢⡀⠀⠀⠀
⠀⣀⠟⢰⡇⠀⠀⠈⢢⡴⠊⠀⠀⠀⠀⠀⣸⢙⣷⠄⢀⠀⠠⠄⠐⠒⠚⠀⠀⠀
⠘⠹⠤⠛⠛⠲⢤⠐⠊⠈⠂⢤⢀⠠⠔⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠣⢀⡀⠔⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    """)
                print('When you stepped outside vault, you encounter a dragon!')
                input('Press Enter to roll for escape')
                dice = choice(range(1,21))
                # Successfull throw
                if dice >= 18:
                    print('Congratulations! You managed to rob Gringotts and escape!')
                    Wizard.remove_disguise(name)
                else:
                    # Get thief's money to victim's vault
                    coins = vars(Wallet(name))
                    coins.pop('usd')
                    coins.pop('gbp')
                    db.execute('UPDATE vaults SET galleons = galleons + ?, sickles = sickles + ?, knuts = knuts + ?\
                        WHERE depositor_id = (SELECT id FROM wizards WHERE name = ?);', *[coins[coin] for coin in coins], person)
                    print('You died in dragon fire')
                    Wizard.kill(name)
                    print(figlet.renderText('Game over'))
                    sys.exit()
            location = 'home'

        case "change coins":
            Wallet.change(name)
        case "currency exchange":
            Wallet.exchange(name)
        case "steal key":
            print('From what wizard you want to steal?')
            dec = make_decision(Wizard.all(name))
            if not dec:
                print('Invalid option')
            else:
                input('Press Enter to roll the dice')
                dice = choice(range(1,21))
                if dice > 6:
                    Wizard.steal_key(name, dec)
                    options['Steal key'] = False
                    print(f"You successfully stolen {dec}'s vault key!")
                else:
                    print(f"You were caught while attempting to steal {dec}'s vault key")
                    print("You will be sent to Azkaban")
                    Wizard.kill(name)
                    print(figlet.renderText('Game over'))
                    sys.exit()
        case "buy polyjuice potion":
            print('Polyjuice potion costs 5 galleons. Are you sure?')
            dec = make_decision(['yes', 'no'])
            if not dec:
                print('Invalid option')
            elif dec == 'yes':
                Wallet.withdraw(PRICES['polyjuice'], name)
                Wizard.add_potion(name)
        case "collect hair for potion":
            print('Choose wizard to steal hair')
            dec = make_decision(Wizard.all(name))
            if not dec:
                print('Invalid option')
            else:
                Wizard.make_polyjuice(name, dec)
                print('Potion ready!')
                print("""
                    ⠀⠀⠀⠀⢀⡴⠢⣀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠒⠔⠋⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠤⠴⠒⠖⠖⠶⠢⠤⣀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠠⠖⢆⡀⠀⠀⣠⠔⣇⠲⣀⢀⠂⣀⠒⣊⢴⣹⠠⣄⠀⠀⠀⡠⢄
⠀⠀⠈⠂⠋⠀⠀⢸⠀⠀⠽⣷⣮⣷⢿⣮⣷⣽⡾⠏⠀⠀⡆⠀⠀⠁⠈
⠀⠀⠀⠀⠀⠀⠀⠸⡀⠀⣸⡧⡀⡤⣀⠠⣀⠠⣼⣟⢀⢠⠇⠀⠀⠀⠀
⡤⡀⠀⠀⠀⠀⠀⠀⠨⡇⢹⡕⠶⠶⠴⠶⠴⠶⣮⡏⢸⠁⠀⠀⠀⠀⠀
⠑⠁⠀⠀⠀⠀⢀⡠⠞⠁⠀⠙⠳⠾⠶⠷⠾⠞⠋⠀⠈⠳⣄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢰⠋⠀⣀⣤⣤⣤⣶⣶⣶⣶⣶⣦⣤⣤⣤⣀⠈⠓⡄⠀⠀
⠀⠀⠀⠀⠀⢸⠀⠘⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠂⡅⠀⠀
⠀⠀⠀⠀⠀⢸⠀⠀⠀⢀⣾⣿⣷⣶⣿⣿⣿⣿⣷⣾⣶⡾⢷⡆⡄⠀⠀
⠀⠀⠀⠀⠀⢸⠀⠀⢀⣾⣿⣿⣿⣯⣿⣿⣿⠟⠉⠙⢿⣿⣿⡇⠇⠀⠀
⠀⠀⠀⠀⠀⢸⠀⠀⢸⣿⣿⣯⣿⣿⣿⣻⣧⡠⢤⢤⣬⣿⣿⡇⡃⠀⠀
⠀⠀⠀⠀⠀⢸⠀⠀⢾⣯⣽⡿⣽⣿⣟⣿⢿⣦⣥⣼⡿⣿⣹⡇⡃⠀⠀
⠀⠀⠀⠀⠀⢸⠀⠀⢯⡿⡏⠁⠀⢹⣟⡾⡿⣽⣻⣽⣻⢿⡽⡇⡅⠀⠀
⠀⠀⠀⠀⠀⢸⠀⠀⡟⡟⣷⣤⣤⣿⢫⣷⠛⣧⡟⣶⣿⣯⡟⡇⡆⠀⠀
⠀⠀⠀⠀⠀⢸⠀⠀⣽⡷⣍⢯⣝⢮⡽⢬⡛⣶⢹⣭⢆⡾⣹⠇⡆⠀⠀
⠀⠀⠀⠀⠀⢸⠀⠀⢾⡘⢿⠚⡌⢇⢏⢣⢃⠗⡛⡜⢎⡹⢏⡇⠆⠀⠀
⠀⠀⠀⠀⠀⢾⡀⠀⣞⢡⢎⠩⡘⠌⡌⢢⠉⡌⡙⠬⡆⠩⠌⣆⡃⠀⠀
⠀⠀⠀⠀⠀⠈⠋⠤⣈⢀⡂⠡⠌⠰⢈⠂⠌⡐⠁⢂⡐⣡⠼⠚⠁⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠑⠒⠒⠒⠒⠒⠒⠛⠉⠉⠀⠀⠀⠀⠀⠀
                """)
        case "drink polyjuice potion":
            Wizard.drink_polyjuice(name)
            print(f"Your body started to change and now you look like {Wizard.check_disguise(name)}")
        case "exit game":
            sys.exit()
    # After user choice was processed
    # Check if allowed to collect hair or drink potion
    d = db.execute('SELECT disguise, status, potion FROM wizards WHERE name = ?;', name)[0]
    if d['disguise'] and not d['status'] and location == 'home':
        options['Drink polyjuice potion'] = True
    else:
        options['Drink polyjuice potion'] = False
    if not d['potion'] and location == 'home':
        options['Buy polyjuice potion'] = True
    else:
        options['Buy polyjuice potion'] = False
    if d['potion'] and not d['disguise'] and location == 'home':
        options['Collect hair for potion'] = True
    else:
        options['Collect hair for potion'] = False
    # Check if exit allowed
    if location == 'home':
        options['Exit game'] = True
    else:
        options['Exit game'] = False

def make_decision(options):
    """Takes list of options(strings), returns chosen one(string) or none, if user inputs invalid index."""
    for i, decision in enumerate(options, start=1):
        print(f"{i}: {decision}")
    try:
        dec = options[int(input('Option: '))-1]
    except:
        return
    return dec


class Vault:
    """Represents wizard's vault.
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
    """

    def __init__(self, name):
        balance = db.execute('SELECT galleons, sickles, knuts FROM vaults, wizards\
            WHERE vaults.depositor_id = wizards.id AND name = ?;', name)[0]
        self.galleons = balance['galleons']
        self.sickles = balance['sickles']
        self.knuts = balance['knuts']


    def __str__(self):
        return f"In vault you have {self.galleons} galleons,\
 {self.sickles} sickles, {self.knuts} knuts"


    def deposit(coins, name):
        wallet = vars(Wallet(name))
        for coin in coins:
            if wallet[coin] < coins[coin]:
                print(f'Wrong amount of {coin}')
                return
        db.execute('UPDATE vaults SET galleons = galleons + ?, sickles = sickles + ?, knuts = knuts + ?\
        WHERE depositor_id = (SELECT id FROM wizards WHERE name = ?);', *[coins[coin] for coin in coins], name)
        print('Successfull deposit!')


    def withdraw(coins, name):
        vault = vars(Vault(name))
        for coin in coins:
            if vault[coin] < coins[coin]:
                print(f'Wrong amount of {coin}s')
                return
        db.execute('UPDATE vaults SET galleons = galleons - ?, sickles = sickles - ?, knuts = knuts - ?\
            WHERE depositor_id = (SELECT id FROM wizards WHERE name = ?);', *[coins[coin] for coin in coins], name)
        print('Successfull withdraw!')


    def new(id):
        db.execute('INSERT INTO vaults (depositor_id, vault_key) VALUES (?, ?);', id, generate_key())


class Wallet:
    """Represents wizard's wallet.
        Contains values of coins and currencies in wallet for current user, stores them in database
        and making changes to those values via methods.
    """

    def __init__(self, name):
        balance = db.execute('SELECT galleons, sickles, knuts, usd, gbp FROM wallets, wizards\
            WHERE wallets.owner_id = wizards.id AND name = ?;', name)[0]
        self.galleons = balance['galleons']
        self.sickles = balance['sickles']
        self.knuts = balance['knuts']
        self.usd = balance['usd']
        self.gbp = balance['gbp']


    def __str__(self):
        return f"In wallet you have {self.galleons} galleons,\
 {self.sickles} sickles, {self.knuts} knuts. Also {self.usd:,.2f} USD, {self.gbp:,.2f} GBP"

    def deposit(coins, name):
        db.execute('UPDATE wallets SET galleons = galleons + ?, sickles = sickles + ?, knuts = knuts + ?\
        WHERE owner_id = (SELECT id FROM wizards WHERE name = ?);', *[coins[coin] for coin in coins], name)


    def withdraw(coins, name):
        db.execute('UPDATE wallets SET galleons = galleons - ?, sickles = sickles - ?, knuts = knuts - ?\
            WHERE owner_id = (SELECT id FROM wizards WHERE name = ?);', *[coins[coin] for coin in coins], name)


    def change(name):
        print('You can only change coins from your wallet')
        print('1 Galleon = 17 Sickles. 1 Sickle = 29 Knuts.')
        coins = {'galleons': int(input('Galleons: ')), 'sickles': int(input('Sickles: ')),
            'knuts': int(input('Knuts: '))}
        wallet = vars(Wallet(name))
        for coin in coins:
            if wallet[coin] < coins[coin]:
                print(f'Wrong amount of {coin}')
                return
        print('Choose coins to recieve')
        for i, coin in enumerate(COINS, start=1):
            print(f"{i}: {coin}")
        try:
            cur = COINS[int(input('Recieve: '))-1]
        except:
            print('Invalid value')
            return
        # Withdraw coins for changing
        Wallet.withdraw(coins, name)
        # Dict for change
        back = {}
        match cur:
            case 'galleons':
                back[cur] = coins[cur] + (coins['sickles'] + coins['knuts']//29)//17
                back['sickles'] = (coins['sickles'] + coins['knuts'] // 29) % 17
                back['knuts'] = coins['knuts'] % 29
            case 'sickles':
                back['galleons'] = 0
                back[cur] = coins[cur] + coins['galleons']*17 + coins['knuts']//29
                back['knuts'] = coins['knuts'] % 29
            case 'knuts':
                back['galleons'] = 0
                back['sickles'] = 0
                back[cur] = coins[cur] + coins['galleons'] * 29 * 17 + coins['sickles'] * 29
        # Deposit wallet with changed coins
        Wallet.deposit(back, name)
        # Filtering zero values for output
        result = {coin: back[coin] for coin in back if back[coin] != 0}
        print('You recieved: ')
        for coin in result:
            print(f'{coin.capitalize()}: {result[coin]}')


    def exchange(name):
        print('1 USD = 20 Knuts. 1 GBP = 25 Knuts. Comission = 1 %, but not less than 20 Knuts')
        for i, decision in enumerate(['buy', 'sell'], start=1):
            print(f"{i}: {decision}")
        try:
            dec = ['buy', 'sell'][int(input('Option: '))-1]
        except:
            print('Invalid value')
            return
        if dec == 'buy':
            print('Choose currency to buy')
            for i, coin in enumerate([*CURRENCIES], start=1):
                print(f"{i}: {coin}")
            try:
                cur = [*CURRENCIES][int(input('Option: '))-1]
            except:
                print('Invalid value')
                return
            print('You can only exchange coins from your wallet')
            coins = {'galleons': int(input('Galleons: ')), 'sickles': int(input('Sickles: ')),
                'knuts': int(input('Knuts: '))}
            wallet = vars(Wallet(name))
            for coin in coins:
                if wallet[coin] < coins[coin]:
                    print(f'Wrong amount of {coin}')
                    return
            # Withdraw coins for changing
            Wallet.withdraw(coins, name)
            # Dict for exchanged currency
            back = {'usd': 0, 'gbp': 0}
            # Exchanging coins
            for coin in CURRENCIES[cur]:
                back[cur] += CURRENCIES[cur][coin] * coins[coin]
            # Take 1% comission, but at least 1 usd/gbp
            value = back[cur]
            if (value / 100) >= 1:
                value *= 0.99
            else:
                value -= 1
            # Limiting to two decimal points
            back[cur] = int(value*100)/100
            # Deposit wallet with changed currency
            Wallet.buy_cur(back, name)
            # Filtering zero values for output
            result = {currency: back[currency] for currency in back if back[currency] != 0}
            print('You recieved: ')
            for currency in result:
                print(f'{currency}: {result[currency]}')
        # Selling currency
        else:
            print('Choose currency to sell')
            for i, coin in enumerate([*CURRENCIES], start=1):
                print(f"{i}: {coin}")
            try:
                cur = [*CURRENCIES][int(input('Currency: '))-1]
            except:
                print('Invalid value')
                return
            sell = {'usd': 0, 'gbp': 0}
            sell[cur] = float(input('Amount: '))
            wallet = vars(Wallet(name))
            if wallet[cur] < sell[cur]:
                print(f'Wrong amount of {cur.upper()}')
                return
            # Sell currency
            Wallet.sell_cur(sell, name)
            knuts = sell[cur] / CURRENCIES[cur]['knuts']
            # Take comission, 1%, at least 20 knuts
            if knuts / 100 >= 20:
                knuts = int(knuts*0.99)
            else:
                knuts = knuts - 20
            galleons = knuts // (29*17)
            knuts = knuts % (29*17)
            sickles = knuts // 29
            knuts = knuts % 29
            Wallet.deposit({'galleons': galleons, 'sickles': sickles, 'knuts': knuts}, name)
            print(f'You recieved: {galleons} Galleons, {sickles} Sickles, {knuts} Knuts')

    def buy_cur(coins, name):
        db.execute('UPDATE wallets SET usd = usd + ?, gbp = gbp + ?\
        WHERE owner_id = (SELECT id FROM wizards WHERE name = ?);', *[coins[coin] for coin in coins], name)


    def sell_cur(coins, name):
        db.execute('UPDATE wallets SET usd = usd - ?, gbp = gbp - ?\
            WHERE owner_id = (SELECT id FROM wizards WHERE name = ?);', *[coins[coin] for coin in coins], name)


    def new(id):
        db.execute('INSERT INTO wallets (owner_id) VALUES (?);', id)


class Wizard:
    """Methods of this class making changes with user's parameters in database"""
    def new(name):
        db.execute('INSERT INTO wizards (name) VALUES (?);', name)
        id = db.execute('SELECT id FROM wizards WHERE name = ?;', name)[0]['id']
        Vault.new(id)
        Wallet.new(id)


    def get(name):
        wizard = db.execute('SELECT name FROM wizards WHERE name = ?;', name)
        return wizard


    def all(name):
        wizards = db.execute('SELECT name FROM wizards WHERE name != ?', name)
        names = [wizard['name'] for wizard in wizards]
        return names


    def kill(name):
        id = db.execute('SELECT id FROM wizards WHERE name = ?;', name)[0]['id']
        db.execute('DELETE FROM vaults WHERE depositor_id = ?;', id)
        db.execute('DELETE FROM wallets WHERE owner_id = ?;', id)
        db.execute('DELETE FROM wizards WHERE name = ?;', name)


    def steal_key(name, victim):
        db.execute('UPDATE wizards SET stolen_key = (SELECT vault_key\
            FROM vaults, wizards WHERE vaults.depositor_id = wizards.id AND name = ?)\
            WHERE name = ?;', victim, name)

    def add_potion(name):
        db.execute('UPDATE wizards SET potion = 1 WHERE name = ?;', name)

    def make_polyjuice(name, disguise):
        db.execute('UPDATE wizards SET disguise = ? WHERE name = ?;', disguise, name)

    def drink_polyjuice(name):
        db.execute("UPDATE wizards SET status = 'disguised', potion = NULL WHERE name = ?;", name)

    def check_disguise(name):
        disguise = db.execute("SELECT disguise, status FROM wizards WHERE name = ?;", name)[0]
        if disguise['status']:
            return disguise['disguise']
        else:
            return name

    def remove_disguise(name):
        db.execute('UPDATE wizards SET disguise = NULL, status = NULL WHERE name = ?;', name)

    def check_key(name, person):
        key = db.execute("SELECT vault_key FROM vaults, wizards\
            WHERE vaults.depositor_id = wizards.id\
            AND name = ?;", person)[0]['vault_key']
        stolen_key = db.execute("SELECT stolen_key FROM wizards WHERE name = ?;", name)[0]['stolen_key']
        if key == stolen_key:
            return True
        else:
            return False

if __name__ == '__main__':
    main()