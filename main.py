import threading
from bot import start_bot as start_bot1
from rug import start_bot as start_bot2

threading.Thread(target=start_bot1).start()
threading.Thread(target=start_bot2).start()