import sys
import signal
from random import randrange
from time import sleep
from services.client import Client
from services.common.redis_client import RedisClient
from services.message import Message

users = []


def handle_interrupt_event(_sig, _frame):
    client_controller = Client()
    for x in users:
        client_controller.logout(x)
    sys.exit(0)


def send_messages(count_users: int):
    user_prefix = "user_id"
    client_controller = Client()
    message_controller = Message()
    for idx in range(count_users):
        users.append(user_prefix + str(idx))
        client_controller.register(users[idx])
        client_controller.login(users[idx])
    i = 0
    while True:
        from_username = user_prefix + str(randrange(len(users)))
        to_username = from_username
        while to_username != from_username:
            to_username = user_prefix + str(randrange(len(users)))
        message = "test message, id:" + str(i)
        i += 1
        message_controller.send_message(message, from_username, to_username)
        sleep(2)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_interrupt_event)
    signal.signal(signal.SIGTERM, handle_interrupt_event)
    RedisClient.get_connection().flushall()
    send_messages(50)
