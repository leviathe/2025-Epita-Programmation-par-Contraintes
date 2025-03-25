import eel
import pathlib

# Modules imports
import sims.generator
import sims.labyrinth_rg

folder = pathlib.Path(__file__).parent

eel.init(folder / 'web', allowed_extensions=['.js', '.html'])

eel.start('index.html', mode=None, host='localhost', port=8000)