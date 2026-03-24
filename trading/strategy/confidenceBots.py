from compression.zstd import Strategy
from trading import models

class ConfidenceBotsStrategy():


    def __init__(self, confidence, order):
        self.confidence = confidence
        self.my_order = order

    def check_recent_trend(self):

