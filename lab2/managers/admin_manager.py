from consolemenu import *
from services.client import Client


class AdminManager:
    def __init__(self, journal_pub_sub):
        self.client = Client()
        self.journal_pub_sub = journal_pub_sub

    def show_menu(self):
        admin_menu = SelectionMenu(["Show online users",
                                    "Show active users",
                                    "Show spamers",
                                    "Show journal"], "Admin Menu")
        admin_menu.show()

        opt = admin_menu.selected_option
        count = int(input("Enter number of records to display: "))
        if opt == 0:
            self.show_online_users(count)
        elif opt == 1:
            self.show_active_users(count)
        elif opt == 2:
            self.show_spamers(count)
        elif opt == 3:
            self.show_journal(count)

    def show_online_users(self, count):
        online_users = self.client.get_all_online_users()
        print("\n".join(online_users[:count]))
        input("Input to close > ")

    def show_active_users(self, count):
        active_users = self.client.get_active_users(count)
        print("\n".join(active_users))
        input("Input to close > ")

    def show_spamers(self, count):
        spamers = self.client.get_spamers(count)
        print("\n".join(spamers))
        input("Input to close > ")

    def show_journal(self, count):
        message_tmp = self.journal_pub_sub.get_message()
        messages_tmp = []
        while message_tmp and len(messages_tmp) < count:
            messages_tmp.append(message_tmp)
            message_tmp = self.journal_pub_sub.get_message()

        messages = []
        for m in messages_tmp:
            if isinstance(m['data'], bytes):
                messages.append(m['data'].decode("utf-8"))

        print("\n".join(messages))
        input("Input to close > ")
