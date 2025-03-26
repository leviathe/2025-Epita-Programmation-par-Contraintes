const loadCanvasButton = document.getElementById('load_canvas')
const pixiContainer = document.getElementById('pixi_container')
const rgSelect = document.getElementById('rg-select')
let app = new PIXI.Application()

eel.expose(LoadCanvas)
eel.expose(registerRoadGenerationAlgorithms)
CANVAS_LOADED = false

// Enum for Tile type
let Tile = {
    0: 'NONE',
    1: 'ROAD'
}

// Enum for Tile texture
let TileTexture = {
    0: ['none0', 'none1', 'none2', 'none3', 'none4'],
    1: ['road']
}

async function LoadTextures() {
    for (const [key,value] of Object.entries(TileTexture)) {
        let tl = []
        for (const t of value) { tl.push(await PIXI.Assets.load(`/images/${t}.png`)); }
        TileTexture[key] = tl
    }
}

function GetTexture(type) {
    return TileTexture[type][Math.floor(Math.random() * TileTexture[type].length)];
}

async function DestroyCanvas() {
    if (!CANVAS_LOADED)
        return

    app.destroy(true, { children: true, texture: true, baseTexture: true });
    app = new PIXI.Application()

    pixiContainer.classList.remove('show')
    pixiContainer.classList.add('hide')

    CANVAS_LOADED = false
}

const delay = (ms) => new Promise(res => setTimeout(res, ms));

async function LoadCanvas(grid) {
    await app.init({
        width: grid[0].length * 16,
        height: grid.length * 16,
        backgroundColor: 0xbbbbbb
    });

    CANVAS_LOADED = true

    pixiContainer.classList.remove('hide')
    pixiContainer.classList.add('show')

    app.view.id = "pixi_canvas"
    
    pixiContainer.appendChild(app.view);

    function shuffle(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]]
        }
    }

    const sprites = []

    // Loading sprites
    for (let y = 0; y < grid.length; y++) {
        for (let x = 0; x < grid[y].length; x++) {
            const sprite = new PIXI.Sprite(GetTexture(grid[y][x]));
            
            sprite.x = x * 16;
            sprite.y = y * 16;
            sprite.width = 16;
            sprite.height = 16;
            
            sprites.push(sprite)
        }
    }

    shuffle(sprites)
    let i = 0;

    for (const sprite of sprites) {
        app.stage.addChild(sprite)
    
        if (i % 5 == 0)
            await delay(1)

        i += 1;
    }
}

loadCanvasButton.onclick = async () => {
    if (CANVAS_LOADED)
        await DestroyCanvas()

    let grid = await eel.generate()()

    console.log('result', grid)

    await LoadCanvas(grid)
}

rgSelect.onchange = async () => {
    eel.select_rg(this.value)
}

function registerRoadGenerationAlgorithms(algorithms) {
    if (algorithms.length === 0)
        return
    
    for (let algo of algorithms) {
        let o = document.createElement('option')
        o.value = algo
        o.text = algo

        rgSelect.appendChild(o)
    }

    eel.select_rg(algorithms[0])
}

LoadTextures()