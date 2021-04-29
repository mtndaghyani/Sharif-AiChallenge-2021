from Model import *
import random
import json
from typing import *

from classes.kargar_agent import KargarAgent
from classes.sarbaz_agent import SarbazAgent

kargar_agent = KargarAgent()
sarbaz_agent = SarbazAgent()


class AI:
    def __init__(self):
        # Current Game State
        self.game: Game = None

        # Answer
        self.message: str = None
        self.direction: int = None
        self.value: int = None

    """
    Return a tuple with this form:
        (message: str, message_value: int, message_dirction: int)
    check example
    """

    def turn(self) -> (str, int, int):
        kargar_agent.initialize(self.game)
        sarbaz_agent.initialize(self.game)
        if self.game.ant.antType == 1:
            print("Ant type: Kargar")
            self.direction = kargar_agent.get_answer().value
            self.message = kargar_agent.get_message()
            print("Direction=" + str(self.direction) + " / " + "Message=" + self.message)
        else:
            print("Ant type: Sarbaz")
            self.direction = sarbaz_agent.get_answer().value
            self.message = kargar_agent.get_message()
            print("Direction=" + str(self.direction) + " / " + "Message=" + self.message)
        return self.message, 2, self.direction
