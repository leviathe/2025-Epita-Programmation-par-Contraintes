import eel
import pathlib

folder = pathlib.Path(__file__).parent
eel.init(folder / 'web', allowed_extensions=['.js', '.html'])

# Modules imports
import sims.labyrinth_rg
import sims.generator as generator

generator.sync_rg_to_front()

print('Starting server...')
eel.start('index.html', mode=None, host='localhost', port=8000)