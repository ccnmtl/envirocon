"""
Signals relating to the game.
"""
from django.dispatch import Signal

world_state = Signal(providing_args=["request"])

