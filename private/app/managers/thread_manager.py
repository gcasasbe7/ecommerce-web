import threading
from ..managers.order_manager import OrderManager

# Manager class to run Email actions in a dedicated background thread
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

# Manager class to run an Order verification in a dedicated background thread
class CheckOrderThread(threading.Thread):

    def __init__(self, basket, user):
        self.basket = basket
        self.user = user
        threading.Thread.__init__(self)
        self._return = None

    def run(self):
        self._return = OrderManager.check_order(basket=self.basket, user=self.user)

    def join(self):
        threading.Thread.join(self)
        return self._return