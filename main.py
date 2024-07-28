#!/usr/bin/python3
import warnings
import urwid
from user_management import UserManagement
from user_database import UserDatabase
from inventory_management import InventoryManagement
from inventory_database import InventoryDatabase
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Filter warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

palette = [
    ('banner', 'light cyan', 'black'),
    ('streak', 'yellow', 'black'),
    ('bg', 'white', 'black'),
    ('button', 'white', 'black'),
    ('button_focus', 'black', 'white'),
    ('header', 'light cyan', 'black'),
    ('body', 'light gray', 'black'),
    ('footer', 'black', 'light cyan'),
    ('key', 'light cyan', 'black', 'bold'),
    ('reversed', 'standout', ''),
    ('success', 'dark green', 'black'),
    ('error', 'dark red', 'black'),
    ('expired', 'dark red', 'black'),
    ('flagged', 'yellow', 'black'),
]

choices = ["Register", "Login", "Exit"]
inventory_choices = ["Add Item", "Update Item", "Delete Item", "Search Item", "Flag Item", "Logout"]