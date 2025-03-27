import eel
import pathlib

folder = pathlib.Path(__file__).parent
eel.init(folder / 'web', allowed_extensions=['.js', '.html'])

# Modules imports
import sims.labyrinth_rg
import sims.z3_solver
import sims.generator as generator
import sims.options as options
import sims.constraints as constraints

options.register_options()
constraints.register_constraints()

@eel.expose
def front_load():
    print('Loading front.')
    options.send_options_to_front()

print('Starting server...')
eel.start('index.html', mode=None, host='localhost', port=8000)