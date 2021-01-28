import numpy as np

'''moduł zawierający klasy potential i variable'''

class potential:
    def __init__(self,variables = np.array([]),table = np.array([])):
        self.variables = variables
        self.table = table


class variable:
    def __init__(self, name=[], domain = []):
        self.name = name
        self.domain = domain