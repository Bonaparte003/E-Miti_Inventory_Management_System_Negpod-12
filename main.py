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


load_dotenv()


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

class InventorySystemUI:
    def __init__(self, user_mgmt: UserManagement, inventory_mgmt: InventoryManagement):
        self.user_mgmt = user_mgmt
        self.inventory_mgmt = inventory_mgmt
        self.main = urwid.Padding(urwid.SolidFill(), left=2, right=2)
        self.top = urwid.Overlay(
            self.main, urwid.SolidFill("\N{MEDIUM SHADE}"),
            align="center", width=("relative", 80),
            valign="middle", height=("relative", 80),
            min_width=20, min_height=9
        )
        self.username = None
        self.user_id = None
        self.action_view = None

    def main_menu(self, button=None):
        title = urwid.BigText("E-miti Inventory System", urwid.font.HalfBlock7x7Font())
        title = urwid.Padding(title, 'center', width='clip')
        
        subtitle = urwid.Text(("streak", "Negpdo-12"), align='center')
        
        buttons = []
        for choice in choices:
            button = urwid.Button(choice)
            urwid.connect_signal(button, 'click', self.item_chosen, user_arg=choice)
            button = urwid.AttrMap(button, 'button', focus_map='button_focus')
            buttons.append(urwid.Padding(button, align='center', width=20))

        content = urwid.Pile([
            title,
            urwid.Divider(),
            subtitle,
            urwid.Divider(),
            *buttons
        ])

        content = urwid.Filler(content, valign='middle')
        content = urwid.LineBox(content, title="E-miti", title_align='center')
        self.main.original_widget = urwid.AttrMap(content, 'bg')

    def item_chosen(self, button, choice):
        if choice == "Register":
            self.main.original_widget = self.register_form()
        elif choice == "Login":
            self.main.original_widget = self.login_form()
        elif choice == "Exit":
            self.exit_program(button)

    def register_form(self):
        body = [urwid.Text("Register"), urwid.Divider()]
        username_edit = urwid.Edit("Username: ")
        password_edit = urwid.Edit("Password: ", mask="*")

        role_group = []
        roles = ["Pharmacist", "Hospital"]
        role_options = [urwid.RadioButton(role_group, role) for role in roles]
        
        register_button = urwid.Button("Register")
        urwid.connect_signal(register_button, "click", self.register_action, (username_edit, password_edit, role_group))

        body.extend([
            username_edit,
            password_edit,
            urwid.Text("Role:"),
            *role_options,
            urwid.AttrMap(register_button, None, focus_map="reversed"),
        ])
        
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def register_action(self, button, edits):
        username = edits[0].edit_text
        password = edits[1].edit_text
        role_group = edits[2]
        selected_role = next((rb.label for rb in role_group if rb.state), None)
        if not selected_role:
            response = urwid.Text(("error", "Please select a role\n"))
        elif self.user_mgmt.register_user(username, password, selected_role.lower()):
            response = urwid.Text(("success", "Registration successful\n"))
        else:
            response = urwid.Text(("error", "Username already taken\n"))
        done = urwid.Button("Ok")
        urwid.connect_signal(done, "click", lambda button: self.main_menu())
        self.main.original_widget = urwid.Filler(urwid.Pile([response, urwid.AttrMap(done, None, focus_map="reversed")]))
    
    def login_form(self):
        body = [urwid.Text("Login"), urwid.Divider()]
        username_edit = urwid.Edit("Username: ")
        password_edit = urwid.Edit("Password: ", mask="*")
        login_button = urwid.Button("Login")
        urwid.connect_signal(login_button, "click", self.login_action, (username_edit, password_edit))
        body.extend([username_edit, password_edit, urwid.AttrMap(login_button, None, focus_map="reversed")])
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def login_action(self, button, edits):
        username = edits[0].edit_text
        password = edits[1].edit_text
        authenticated, user_id, role = self.user_mgmt.authenticate_user(username, password)
        if authenticated:
            self.username = username
            self.user_id = user_id
            self.inventory_menu()
        else:
            response = urwid.Text(("error", "Login failed\n"))
            done = urwid.Button("Ok")
            urwid.connect_signal(done, "click", self.main_menu)
            self.main.original_widget = urwid.Filler(urwid.Pile([response, urwid.AttrMap(done, None, focus_map="reversed")]))

    def inventory_menu(self):
        inventory = self.inventory_mgmt.get_inventory(self.user_id)

        header = urwid.Columns([
            urwid.Text("ID"),
            urwid.Text("Name"),
            urwid.Text("Expiry Date"),
            urwid.Text("Price"),
            urwid.Text("Quantity"),
            urwid.Text("Code")
        ])

        items = []
        for item in inventory:
            # Format the expiry_date as a string
            expiry_date_str = item['expiry_date'].strftime('%Y-%m-%d %H:%M:%S')
            item_widget = urwid.Columns([
                urwid.Text(str(item['id'])),
                urwid.Text(item['name']),
                urwid.Text(expiry_date_str),  # Use the formatted string here
                urwid.Text(str(item['price'])),
                urwid.Text(str(item['quantity'])),
                urwid.Text(str(item['code']))
            ])
            if item['expiry_date'] < datetime.now():
                items.append(urwid.AttrMap(item_widget, 'expired'))
            elif item.get('flag', False):
                items.append(urwid.AttrMap(item_widget, 'flagged'))
            else:
                items.append(item_widget)

        inventory_list = urwid.ListBox(urwid.SimpleFocusListWalker([header] + items))
        inventory_box = urwid.LineBox(inventory_list, title="Inventory")

        menu_items = [urwid.Button(choice, on_press=self.menu_choice) for choice in inventory_choices]
        menu_list = urwid.ListBox(urwid.SimpleFocusListWalker(menu_items))
        menu_box = urwid.LineBox(menu_list, title="Menu")

        self.action_view = urwid.Text("")
        action_box = urwid.LineBox(self.action_view, title="Action")

        right_column = urwid.Pile([
            ('weight', 1, menu_box),
            ('weight', 2, action_box)
        ])

        columns = urwid.Columns([
            ('weight', 2, inventory_box),
            ('weight', 1, right_column),
        ])

        self.main.original_widget = columns 

    def menu_choice(self, button):
        choice = button.label
        if choice == "Add Item":
            self.show_add_item()
        elif choice == "Update Item":
            self.show_update_item()
        elif choice == "Delete Item":
            self.show_delete_item()
        elif choice == "Search Item":
            self.show_search_item()
        elif choice == "Flag Item":
            self.show_flag_item()
        elif choice == "Logout":
            self.main_menu()

    def show_add_item(self):
        content = [
            urwid.Edit("Name: "),
            urwid.Edit("Quantity: "),
            urwid.Edit("Price: "),
            urwid.Edit("Code: "),
            urwid.Edit("Expiry Date: "),
            urwid.CheckBox("Flag"),
            urwid.Button("Add", on_press=self.add_item)
        ]
        self.action_view = urwid.ListBox(urwid.SimpleFocusListWalker(content))
        self.update_action_box()

    def add_item(self, button):
        form = self.action_view
        name = form.body[0].edit_text
        quantity = form.body[1].edit_text
        price = form.body[2].edit_text
        code = form.body[3].edit_text
        expiry_date = form.body[4].edit_text
        flag = form.body[5].state

        if not name or not quantity or not price or not code or not expiry_date:
            self.show_message("All fields are required.")
            return

        try:
            quantity = int(quantity)
            price = float(price)
            if self.inventory_mgmt.add_item(self.user_id, name, quantity, price, code, expiry_date, flag):
                self.show_message("Item added successfully")
                self.inventory_menu()  # Refresh inventory
            else:
                self.show_message("Failed to add item")
        except ValueError:
            self.show_message("Invalid input. Quantity must be an integer and price must be a float")

    def show_update_item(self):
        content = [
            urwid.Edit("Item ID: "),
            urwid.Edit("New Name: "),
            urwid.Edit("New Quantity: "),
            urwid.Edit("New Price: "),
            urwid.Edit("New Code: "),
            urwid.Edit("New Expiry Date: "),
            urwid.Button("Update", on_press=self.update_item)
        ]
        self.action_view = urwid.ListBox(urwid.SimpleFocusListWalker(content))
        self.update_action_box()

    def update_item(self, button):
        form = self.action_view
        item_id = form.body[0].edit_text
        name = form.body[1].edit_text
        quantity = form.body[2].edit_text
        price = form.body[3].edit_text
        code = form.body[4].edit_text
        expiry_date = form.body[5].edit_text

        if not item_id or not name or not quantity or not price or not code or not expiry_date:
            self.show_message("All fields are required.")
            return

        try:
            item_id = int(item_id)
            quantity = int(quantity)
            price = float(price)
            if self.inventory_mgmt.update_item(item_id, name, quantity, price, code, expiry_date):
                self.show_message("Item updated successfully")
                self.inventory_menu()  # Refresh inventory
            else:
                self.show_message("Item not found")
        except ValueError:
            self.show_message("Invalid input. Item ID, Quantity must be integers and price must be a float")

    def show_delete_item(self):
        content = [
            urwid.Edit("Item ID: "),
            urwid.Button("Delete", on_press=self.delete_item)
        ]
        self.action_view = urwid.ListBox(urwid.SimpleFocusListWalker(content))
        self.update_action_box()

    def delete_item(self, button):
        form = self.action_view
        item_id = form.body[0].edit_text

        if not item_id:
            self.show_message("Item ID is required.")
            return

        try:
            item_id = int(item_id)
            if self.inventory_mgmt.delete_item(item_id):
                self.show_message("Item deleted successfully")
                self.inventory_menu()  # Refresh inventory
            else:
                self.show_message("Item not found")
        except ValueError:
            self.show_message("Invalid input. Item ID must be an integer")

    def show_search_item(self):
        content = [
            urwid.Edit("Item Name: "),
            urwid.Button("Search", on_press=self.search_item)
        ]
        self.action_view = urwid.ListBox(urwid.SimpleFocusListWalker(content))
        self.update_action_box()

    def search_item(self, button):
        form = self.action_view
        name = form.body[0].edit_text

        if not name:
            self.show_message("Item name is required.")
            return

        top_users = self.inventory_mgmt.get_top_users_for_item(name)
        if top_users:
            result = f"Research Result For {name}\n\n"
            for user in top_users:
                result += f"Username: {user['username']}, Count: {user['total_quantity']}\n"
            self.show_search_result(result)
        else:
            self.show_message("Item not found")

    def show_search_result(self, result):
        self.action_view = urwid.Text(result)
        self.update_action_box()

    def show_flag_item(self):
        content = [
            urwid.Edit("Item ID: "),
            urwid.Button("Flag", on_press=self.flag_item)
        ]
        self.action_view = urwid.ListBox(urwid.SimpleFocusListWalker(content))
        self.update_action_box()

    def flag_item(self, button):
        form = self.action_view
        item_id = form.body[0].edit_text

        if not item_id:
            self.show_message("Item ID is required.")
            return

        try:
            item_id = int(item_id)
            if self.inventory_mgmt.flag_item(item_id):
                self.show_message("Item flagged successfully")
                self.inventory_menu()  # Refresh inventory
            else:
                self.show_message("Item not found")
        except ValueError:
            self.show_message("Invalid input. Item ID must be an integer")

    def show_message(self, message):
        self.action_view = urwid.Text(message)
        self.update_action_box()

    def update_action_box(self):
        action_box = urwid.LineBox(self.action_view, title="Action")
        right_column = self.main.original_widget.contents[1][0]
        right_column.contents[1] = (action_box, right_column.options('weight', 2))

    def exit_program(self, button):
        raise urwid.ExitMainLoop()

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    # Get MySQL connection parameters from environment variables
    db_host = os.getenv("DB_HOST")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    user_db = UserDatabase(host=db_host, user=db_user, password=db_password, database=db_name)
    inventory_db = InventoryDatabase(host=db_host, user=db_user, password=db_password, database=db_name)
    user_mgmt = UserManagement(user_db)
    inventory_mgmt = InventoryManagement(inventory_db)
    system = InventorySystemUI(user_mgmt, inventory_mgmt)
    system.main_menu()
    urwid.MainLoop(system.top, palette).run()
