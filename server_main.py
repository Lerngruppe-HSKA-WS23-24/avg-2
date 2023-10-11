import time


from server.MessageManager import *

m = MessageManager()

while True:
    m.await_new_messages()
    time.sleep(5)

print("Server: finished")
