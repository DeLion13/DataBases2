from consolemenu import *
from services.common.settings import statuses
from services.message import Message


class MessageManager:
    def __init__(self, username):
        self.message = Message()
        self.username = username

    def show_inbox(self):
        messages = self.message.read_messages(self.username)
        messages_view = SelectionMenu(messages, "Inbox")
        messages_view.show()

    def show_send(self):
        receiver = input("Send to: ")
        text = input("Enter message text: ")
        self.message.send_message(text, self.username, receiver)

    def show_statuses(self):
        statuses_display = statuses.copy()
        for i in range(len(statuses)):
            count = self.message.count_messages_in_status(self.username, statuses[i])
            statuses_display[i] += f" | count: {count}"

        statuses_display.append("Refresh")

        statuses_view = SelectionMenu(statuses_display, "Messages in statuses")
        statuses_view.show()

        if statuses_view.selected_option == 6:  # Refresh
            self.show_statuses()
