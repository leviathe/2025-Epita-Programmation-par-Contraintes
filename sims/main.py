import eel
import pathlib

folder = pathlib.Path(__file__).parent
eel.init(folder / 'web', allowed_extensions=['.js', '.html'])

# Modules imports
import sims.labyrinth_rg
import sims.generator as generator
import sims.options as options

options.register_options()

@eel.expose
def front_load():
    print('Loading front.')
    options.send_options_to_front()

print('Starting server...')
eel.start('index.html', mode=None, host='localhost', port=8000)