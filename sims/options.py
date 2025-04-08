import eel
import sims.generator as generator

from sims.utils import StringEnum

OPTIONS = {}

class Option():
    def __init__(self, id, name, category, type):
        self.id, self.name, self.category, self.type, self.value = id, name, category, type, None

    def serialize(self):
        return { 'id': self.id, 'name': self.name, 'category': self.category, 'type': self.type }

class RangeOption(Option):
    def __init__(self, id, name, category, min_range, max_range, step):
        super().__init__(id, name, category, 'range')
        self.min_range, self.max_range, self.step = min_range, max_range, step

    def serialize(self):
        return super().serialize() | { 'min_range': self.min_range, 'max_range': self.max_range, 'step': self.step }

class SelectOption(Option):
    def __init__(self, id, name, category, options : list[str]):
        super().__init__(id, name, category, 'select')
        self.options = options

    def serialize(self):
        return super().serialize() | { 'options': self.options }

class CheckboxOption(Option):
    def __init__(self, id, name, category):       
        super().__init__(id, name, category, 'checkbox')

@eel.expose
def option_update(id, value):
    OPTIONS[id].value = value
    print(f'Updated option {id} to ({type(value)}) {value}.')

def register_option(option : Option):
    if option.id in OPTIONS:
        raise Exception(f'Option already exists: {option.id}.')
    
    OPTIONS[option.id] = option
    
class Opt(StringEnum):
    #Grid
    
    GRID_WIDTH = 'grid_width'
    GRID_HEIGHT = 'grid_height'
    
    # World Generation
    ROAD_GENERATION_ALGORITHM = 'road_generation_algorithm'
    GENERATE_RIVERS = 'generate_rivers'    

    # City parameters
    POPULATION = 'population'
    HOUSE_CAPACITY = 'house_capacity'
    HOSPITAL_CAPACITY = 'hopital_capacity'

    # Solver and Constraints
    SOLVER = 'solver'

    BUILDINGS_NEXT_TO_AT_LEAST_A_ROAD = 'buildings_next_to_at_least_a_road'
    HOSPITALS_NEAR_PATIENTS = 'hospitals_near_patients'
    

class OptCat(StringEnum):
    GRID = 'GRID',
    WORLD_GENERATION = 'WORLD GENERATION'
    SOLVER_AND_CONSTRAINTS = 'SOLVER AND CONSTRAINTS'
    CITY_PARAMETERS = 'CITY PARAMETERS'

def register_options():
    opts = [
        # Grid
        RangeOption(Opt.GRID_WIDTH, 'Grid Width', OptCat.GRID, 10, 100, 10),
        RangeOption(Opt.GRID_HEIGHT, 'Grid Height', OptCat.GRID, 10, 100, 10),
        
        # World Generation 
        SelectOption(Opt.ROAD_GENERATION_ALGORITHM, 'Road Generation Algorithm', OptCat.WORLD_GENERATION, list(generator.ROAD_GENERATION_ALGORITHMS.keys())),
        CheckboxOption(Opt.GENERATE_RIVERS, 'Generate Rivers', OptCat.WORLD_GENERATION),

        # City Parameters
        RangeOption(Opt.POPULATION, 'Population', OptCat.CITY_PARAMETERS, 10, 1000, 10),
        RangeOption(Opt.HOUSE_CAPACITY, 'House Capacity', OptCat.CITY_PARAMETERS, 1, 10, 1),
        RangeOption(Opt.HOSPITAL_CAPACITY, 'Hospital Capacity', OptCat.CITY_PARAMETERS, 1, 100, 5),

        # Solver and Constraints
        SelectOption(Opt.SOLVER, 'Solver', OptCat.SOLVER_AND_CONSTRAINTS, ['NONE'] + list(generator.SOLVER_ALGORITHMS.keys())),
    ]

    for o in opts: register_option(o)

def send_options_to_front():
    eel.registerOptions([o.serialize() for o in OPTIONS.values()])

def get(opt : Opt):
    return OPTIONS[opt].value