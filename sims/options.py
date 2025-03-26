import eel
import sims.generator as generator
from enum import Enum

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

class StringEnum(str, Enum):
    def __str__(self):
        return self.value
    
class Opt(StringEnum):
    GRID_WIDTH = 'grid_width'
    GRID_HEIGHT = 'grid_height'
    ROAD_GENERATION_ALGORITHM = 'road_generation_algorithm'
    GENERATE_RIVERS = 'generate_rivers'

class OptCat(StringEnum):
    GRID = 'GRID',
    WORLD_GENERATION = 'WORLD GENERATION'

def register_options():
    opts = [
        RangeOption(Opt.GRID_WIDTH, 'Grid Width', OptCat.GRID, 10, 100, 10),
        RangeOption(Opt.GRID_HEIGHT, 'Grid Height', OptCat.GRID, 10, 100, 10),
        SelectOption(Opt.ROAD_GENERATION_ALGORITHM, 'Road Generation Algorithm', OptCat.WORLD_GENERATION, list(generator.ROAD_GENERATION_ALGORITHMS.keys())),
        CheckboxOption(Opt.GENERATE_RIVERS, 'Generate Rivers', OptCat.WORLD_GENERATION)
    ]

    for o in opts: register_option(o)

def send_options_to_front():
    eel.registerOptions([o.serialize() for o in OPTIONS.values()])

def get(opt : Opt):
    return OPTIONS[opt].value