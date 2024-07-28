#!/usr/bin/python3
import urwid
import subprocess
import threading


palette = [
    ('banner', 'light cyan', 'black'),
    ('streak', 'yellow', 'black'),
    ('bg', 'white', 'black'),
    ('button', 'light green', 'dark blue'),
    ('button_focus', 'black', 'white'),
]

def start_main():
    subprocess.run(["python3", "main.py"])

def on_enter(button):

    threading.Thread(target=start_main).start()
    raise urwid.ExitMainLoop()


welcome_text = urwid.BigText("Welcome to E-miti", urwid.font.HalfBlock7x7Font())
welcome_text = urwid.Padding(welcome_text, 'center', width='clip')


subtitle = urwid.Text(("streak", "Negpdo-12"), align='center')


button = urwid.Button("Enter", on_press=on_enter)
button = urwid.AttrMap(button, 'button', focus_map='button_focus')
button = urwid.Padding(button, align='center', width=20)


content = urwid.Pile([
    welcome_text,
    urwid.Divider(),
    subtitle,
    urwid.Divider(),
    button
])


content = urwid.Filler(content, valign='middle')
content = urwid.LineBox(content, title="E-miti", title_align='center')


background = urwid.AttrMap(content, 'bg')


loop = urwid.MainLoop(background, palette=palette, unhandled_input=lambda key: None if key != 'q' else loop.stop())

if __name__ == "__main__":
    loop.run()
