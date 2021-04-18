from consolemenu import *
from consolemenu.items import *
from services.collections.pub_sub import PubSub
from managers.admin_manager import AdminManager
from managers.message_manager import MessageManager
from managers.user_manager import UserManager


class App:
    def __init__(self):
        inbox_menu_item = FunctionItem("Inbox", self.inbox_screen)
        send_message_menu_item = FunctionItem("Send Message", self.send_screen)
        statuses_menu_item = FunctionItem("Statuses", self.statuses_screen)
        self.admin_menu_item = FunctionItem("Admin panel", self.admin_panel)

        self.main_menu = ConsoleMenu("Redis Messaging")
        self.main_menu.append_item(inbox_menu_item)
        self.main_menu.append_item(send_message_menu_item)
        self.main_menu.append_item(statuses_menu_item)

        self.user_manager = UserManager()
        self.message_manager = None
        self.current_username = None

        self.journal_pub_sub = PubSub('activity_journal')

    def start(self):
        while not self.user_manager.username:
            self.user_manager.show_auth()

        self.current_username = self.user_manager.username
        is_admin = "admin" if self.user_manager.client.is_admin(self.current_username) else "just user"
        self.main_menu.epilogue_text = f"logged in as {self.current_username} ({is_admin})"

        if is_admin == "admin":
            self.main_menu.append_item(self.admin_menu_item)

        self.message_manager = MessageManager(self.current_username)
        self.journal_pub_sub.subscribe()

        self.main_menu.show()

    def inbox_screen(self):
        self.message_manager.show_inbox()

    def send_screen(self):
        self.message_manager.show_send()

    def statuses_screen(self):
        self.message_manager.show_statuses()

    def admin_panel(self):
        admin_manager = AdminManager(self.journal_pub_sub)
        admin_manager.show_menu()


if __name__ == '__main__':
    myApp = App()
    myApp.start()
