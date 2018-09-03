#
from modules.base import SaoDangFb

class task(SaoDangFb):
    def ActIndex(self):
        result = self.action(c='activity',m='index')
