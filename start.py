from client import Client
try:
    Client.start("kod.d")
except KeyboardInterrupt:
    pass