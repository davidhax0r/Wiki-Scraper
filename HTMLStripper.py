# Developed by: Nauman Ahmad
# Twitter: twitter.com/itsnauman
# Email: nauman-ahmad@outlook.com

#Import HTML Parser module
from HTMLParser import HTMLParser

#MLStripper inherts from the HTMLParser base class
class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)
