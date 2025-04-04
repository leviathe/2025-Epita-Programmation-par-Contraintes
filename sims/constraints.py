import math

from sims.utils import StringEnum
import sims.options as o

CONSTRAINTS = {}

class Constraint():
    def __init__(self, opt : o.Opt, title : str):
        self.opt = opt
        self.option = o.CheckboxOption(opt, title, o.OptCat.SOLVER_AND_CONSTRAINTS)

        o.register_option(self.option)

    def enabled(self):
        return o.get(self.opt)

def constraint_enabled(opt : o.Opt):
    if not opt in CONSTRAINTS:
        raise Exception('Invalid constraint given to is_constraint_enabled.')
    
    return CONSTRAINTS[opt].enabled()

def register_constraint(constraint : Constraint):
    CONSTRAINTS[constraint.option.id] = constraint

def register_constraints():
    consts = [
        Constraint(o.Opt.BUILDINGS_NEXT_TO_AT_LEAST_A_ROAD, 'Buildings next to a road'),
    ]

    for c in consts: register_constraint(c)

# Utils functions related to parameters

def get_required_number_of_houses():
    return math.ceil(o.get(o.Opt.POPULATION) / o.get(o.Opt.HOUSE_CAPACITY))