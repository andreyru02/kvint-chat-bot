from transitions import Machine


class Matter(object):
    def __init__(self):
        self.payment_method = None
        self.pizza_size = None
        self.set_answers()

    def set_answers(self, pizza_size='', payment_method=''):
        self.pizza_size = pizza_size
        self.payment_method = payment_method

    def get_answers(self):
        return self.pizza_size, self.payment_method


lump = Matter()
states = ['start', 'pay', 'confirm', 'finish']

transitions = [
    {'trigger': 'pizza_size', 'source': 'start', 'dest': 'pay'},
    {'trigger': 'payment_method', 'source': 'pay', 'dest': 'confirm'},
    {'trigger': 'final', 'source': 'confirm', 'dest': 'finish'},
]

machine = Machine(lump, states=states, transitions=transitions, initial='start')
