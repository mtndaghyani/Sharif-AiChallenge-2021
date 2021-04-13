from Model import *
import random
import json
from typing import *

from classes.kargar_agent import KargarAgent

kargar_agent = KargarAgent()


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
        """self.message = "hello python"
        self.value = random.randint(1,10)
        self.direction = random.choice(list(Direction)).value"""
        kargar_agent.initialize(self.game)
        if self.game.ant.antType == 1:
            print("Ant type: Kargar")
            self.direction = kargar_agent.get_answer().value
            print(self.direction)
        else:
            print("Ant type: Sarbaz")
            self.direction = Direction.UP.value
        return self.message, self.value, self.direction
