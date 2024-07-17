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