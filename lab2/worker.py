from random import randrange

from services.common.settings import *
from services.collections.hash import Hash
from services.collections.list import List
from services.collections.pub_sub import PubSub
from services.collections.set import Set
from services.collections.zset import ZSet


class Worker:
    def __init__(self):
        self.__message_queue = List("message_queue")
        self.__message_in_queue_status = Set(message_in_queue_status)
        self.__messages_processing_status = Set(message_processing_status)
        self.__messages_send_status = Set(message_send_status)
        self.__messages_delivered_status = Set(message_delivered_status)
        self.__messages_blocked_status = Set(message_blocked_status)
        self.__journal = PubSub("activity_journal")
        self.__active_users = ZSet("most_active_users")
        self.__spamers = ZSet("spamers")

        self.__sent_message_journal_prefix = "sent_message:"
        self.__incoming_message_prefix = "incoming_message:"

    def run(self):
        while True:
            message_id = self.__message_queue.remove_blocking()
            self.__message_in_queue_status.move_to("message_processing_status", message_id)
            message = Hash(message_id)
            sender, message_body, receiver = self.get_message_data(message)

            if self.is_message_valid(message_body):
                self.__messages_processing_status.move_to("message_send_status", message_id)
                List(self.__incoming_message_prefix + receiver).add(message_id)
                PubSub(self.__sent_message_journal_prefix + receiver).publish(receiver)
                self.__messages_send_status.move_to("message_delivered_status", message_id)
                self.__active_users.add(sender, 1)
            else:
                self.__messages_processing_status.move_to("message_blocked_status", message_id)
                self.__spamers.add(sender, 1)
                self.__journal.publish("Client `%s` tried to send SPAM `%s` to user `%s`" %
                                       (sender, message_body, receiver))

    @staticmethod
    def get_message_data(message: Hash):
        sender = message.get('from')
        message_body = message.get('body')
        receiver = message.get('to')
        return sender, message_body, receiver

    @staticmethod
    def is_message_valid(message: str):
        return randrange(100) > 10


if __name__ == '__main__':
    worker = Worker()
    worker.run()
