from consolemenu import *
from services.client import Client


class UserManager:
    def __init__(self):
        self.client = Client()
        self.username = ""

    def show_auth(self):
        self.username = input("Enter username: ")

        if self.client.is_registered(self.username):
            self.client.login(self.username)
        else:
            is_admin_menu = SelectionMenu(["yes", "no"], "Register as admin?")
            is_admin_menu.show()
            is_admin = True if is_admin_menu.selected_option == 0 else False

            self.client.register(self.username, is_admin)
            self.client.login(self.username)
