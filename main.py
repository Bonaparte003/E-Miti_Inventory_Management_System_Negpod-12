import urwid

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