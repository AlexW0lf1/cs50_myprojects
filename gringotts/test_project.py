import pytest
from cs50 import SQL
from project import Wizard, Vault, Wallet

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///gringotts.db")


def test_Wizard():
    name = 'Abracadabra'
    name2 = 'AAAAAA'
    Wizard.new(name)
    Wizard.new(name2)
    assert Wizard.get(name)[0]['name'] == name
    assert Wizard.get('Definetely not valid name') == []
    Wizard.make_polyjuice(name, name2)
    Wizard.drink_polyjuice(name)
    assert Wizard.check_disguise(name) != name
    Wizard.remove_disguise(name)
    assert Wizard.check_disguise(name) == name
    assert Wizard.check_key(name, name2) == False
    Wizard.steal_key(name, name2)
    assert Wizard.check_key(name, name2) == True
    Wizard.kill(name)
    Wizard.kill(name2)


def test_Vault():
    name = 'Abracadabra'
    name2 = 'AAAAAA'
    coins = {'galleons': 5, 'sickles': 10, 'knuts': 15}
    Wizard.new(name)
    Wizard.new(name2)
    vault = Vault(name)
    assert vault.galleons == 0
    assert vault.sickles == 0
    assert vault.knuts == 0
    Vault.deposit(coins, name)
    vault = Vault(name)
    assert vault.galleons == 5
    assert vault.sickles == 10
    assert vault.knuts == 15
    Vault.withdraw(coins, name)
    vault = Vault(name)
    assert vault.galleons == 0
    assert vault.sickles == 0
    assert vault.knuts == 0
    Wizard.kill(name)
    Wizard.kill(name2)


def test_Wallet():
    name = 'Abracadabra'
    name2 = 'AAAAAA'
    coins = {'galleons': 5, 'sickles': 10, 'knuts': 15}
    Wizard.new(name)
    Wizard.new(name2)
    wallet = Wallet(name)
    assert wallet.galleons == 20
    assert wallet.sickles == 30
    assert wallet.knuts == 25
    assert wallet.gbp == 0
    assert wallet.usd == 0
    Wallet.deposit(coins, name)
    wallet = Wallet(name)
    assert wallet.galleons == 25
    assert wallet.sickles == 40
    assert wallet.knuts == 40
    Wallet.withdraw(coins, name)
    wallet = Wallet(name)
    assert wallet.galleons == 20
    assert wallet.sickles == 30
    assert wallet.knuts == 25
    Wizard.kill(name)
    Wizard.kill(name2)