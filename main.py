#!/usr/bin/python3
import urwid
import typing

# Define the palette for the UI colors
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
inventory_choices = ["Add Item", "Update Item", "Delete Item", "Logout"]

class InventorySystem:
    def __init__(self):
        self.main = urwid.Padding(urwid.SolidFill(), left=2, right=2)
        self.top = urwid.Overlay(
            self.main, urwid.SolidFill("\N{MEDIUM SHADE}"),
            align="center", width=("relative", 80),
            valign="middle", height=("relative", 80),
            min_width=20, min_height=9
        )

    def main_menu(self):
        title = urwid.BigText("E-miti Inventory System", urwid.font.HalfBlock7x7Font())
        title = urwid.Padding(title, 'center', width='clip')
        
        subtitle = urwid.Text(("streak", "Negpdo-12"), align='center')
        
        buttons = []
        for choice in choices:
            button = urwid.Button(choice)
            urwid.connect_signal(button, 'click', self.item_chosen, choice)
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

    # Registration - Didier 
    def register_form(self):
        body = [urwid.Text("Register"), urwid.Divider()]
        username_edit = urwid.Edit("Username: ")
        password_edit = urwid.Edit("Password: ", mask="*")

        role_group = []
        roles = ["Admin", "Pharmacist", "Inventory Manager", "Hospital"]
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
        elif register_user(username, password, selected_role.lower()):
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
        if authenticate_user(username, password):
            self.inventory_menu(username)
        else:
            response = urwid.Text(("error", "Login failed\n"))
            done = urwid.Button("Ok")
            urwid.connect_signal(done, "click", self.main_menu)
            self.main.original_widget = urwid.Filler(urwid.Pile([response, urwid.AttrMap(done, None, focus_map="reversed")]))
    def inventory_menu(self, username):
        tasks_content = [
            ("header", " ID   NAME           EXPIRY_DATE   PRICE     QUANTITY           CODE      "),
        ]
        inventory = get_inventory(username)

        # Find the maximum width for each column
        max_widths = [len(col) for col in tasks_content[0][1].split()]

        for item_list in inventory.values():
            for item in item_list:
                # Update max widths based on current item
                max_widths[0] = max(max_widths[0], len(str(item['id'])) + len("ID"))
                max_widths[1] = max(max_widths[1], len(item['name']) + len("NAME"))
                max_widths[2] = max(max_widths[2], len(item['expiry_date']) + len("EXPIRY_DATE"))
                max_widths[3] = max(max_widths[3], len(str(item['price'])) + len("PRICE"))
                max_widths[4] = max(max_widths[4], len(str(item['quantity'])) + len("QUANTITY"))
                max_widths[5] = max(max_widths[5], len(str(item['Code'])) + len("CODE"))

        # Adjust tasks_content with dynamically calculated column widths
        tasks_content[0] = ("header", f" ID{' '(max_widths[0]-2)} NAME{' '(max_widths[1]-4)} EXPIRY_DATE{' '(max_widths[2]-11)} PRICE{' '(max_widths[3]-6)} QUANTITY{' '(max_widths[4]-8)} CODE{' '(max_widths[5]-4)}")

        for item_list in inventory.values():
            for item in item_list:
                if item['expiry_date'] < datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
                    tasks_content.append(("expired", f" {item['id']}{' '(max_widths[0]-len(str(item['id'])))} {item['name']}{' '(max_widths[1]-len(item['name']))} {item['expiry_date']}{' '(max_widths[2]-len(item['expiry_date']))} {item['price']}{' '(max_widths[3]-len(str(item['price'])))} {item['quantity']}{' '(max_widths[4]-len(str(item['quantity'])))} {item['Code']}{' '(max_widths[5]-len(str(item['Code'])))}"))
                else:
                    tasks_content.append(("body", f" {item['id']}{' '(max_widths[0]-len(str(item['id'])))} {item['name']}{' '(max_widths[1]-len(item['name']))} {item['expiry_date']}{' '(max_widths[2]-len(item['expiry_date']))} {item['price']}{' '(max_widths[3]-len(str(item['price'])))} {item['quantity']}{' '(max_widths[4]-len(str(item['quantity'])))} {item['Code']}{' '(max_widths[5]-len(str(item['Code'])))}"))

        # Create widgets with adjusted content
        tasks_list = urwid.SimpleListWalker([urwid.AttrMap(urwid.Text(item[1]), item[0]) for item in tasks_content])

        # Create buttons for the menu options on the right side
        menu_items = [
            urwid.Text(f"=========== Welcome back, {username} ==========="),
            urwid.Text(""),
            urwid.Button("Add Item", on_press=lambda button: self.handle_menu_action(username, "add")),
            urwid.Button("Update Item", on_press=lambda button: self.handle_menu_action(username, "update")),
            urwid.Button("Delete Item", on_press=lambda button: self.handle_menu_action(username, "delete")),
            urwid.Button("Logout", on_press=lambda button: self.main_menu())
        ]

        # Style the buttons
        menu_items = [urwid.AttrMap(item, "button", focus_map="button_focus") for item in menu_items]

        # Wrap the menu items in a ListBox
        menu_items_listbox = urwid.ListBox(urwid.SimpleFocusListWalker(menu_items))

        # Add padding around the menu items
        menu_items_with_padding = urwid.Padding(menu_items_listbox, left=2, right=2)

        # Create the columns
        columns = urwid.Columns([
            urwid.LineBox(urwid.ListBox(tasks_list), title="Inventory List"),
            urwid.LineBox(menu_items_with_padding, title="Menu"),
        ])

        # Update the main widget with the columns
        self.main.original_widget = columns