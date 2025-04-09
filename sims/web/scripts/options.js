let optionsContainer = document.getElementById('options_container')
let categoryTemplate = document.getElementsByClassName('options-category')[0]
let rangeOptionTemplate = document.getElementsByClassName('option-range-container')[0]
let checkboxOptionTemplate = document.getElementsByClassName('option-checkbox-container')[0]
let selectOptionTemplate = document.getElementsByClassName('option-select-container')[0]

eel.expose(registerOptions)

function registerOptions(options) {
    for (let opt of options) {
        let category = document.getElementById(`category-${opt.category}`)

        let defaultValue = localStorage.getItem(opt.name)
        
        if (defaultValue === null)
            defaultValue = opt.default 

        if (category === null)
        {
            category = categoryTemplate.cloneNode(true)
            category.id = `category-${opt.category}`

            let catName = category.querySelector('.category-title')
            catName.innerText = opt.category

            optionsContainer.appendChild(category)
        }

        if (opt.type === 'range') {
            let o = rangeOptionTemplate.cloneNode(true)
            let oRange = o.querySelector('.option-range')
            let oName = o.querySelector('.option-range-name')
            oName.innerText = `${opt.name} : ${oRange.value}`

            oRange.min = opt.min_range
            oRange.max = opt.max_range
            oRange.step = opt.step

            function rangeUpdate() {
                oName.innerText = `${opt.name} : ${oRange.value}`
                eel.option_update(opt.id, parseInt(oRange.value))
                localStorage.setItem(opt.name, oRange.value)
            }

            oRange.onchange = rangeUpdate

            if (defaultValue !== null) oRange.value = defaultValue

            o.classList.remove('template')
            category.appendChild(o)

            rangeUpdate()
        }
        else if (opt.type == 'checkbox') {
            let o = checkboxOptionTemplate.cloneNode(true)
            let oCheck = o.querySelector('.option-checkbox')
            let oName = o.querySelector('.option-checkbox-name')
            oName.innerText = `${opt.name}`

            function checkUpdate() {
                eel.option_update(opt.id, oCheck.checked)
                localStorage.setItem(opt.name, oCheck.checked)
            }
            oCheck.onchange = checkUpdate

            if (defaultValue !== null) oCheck.checked = defaultValue === "true" ? true : defaultValue === true

            o.classList.remove('template')
            category.appendChild(o)

            checkUpdate()
        }
        else if (opt.type == 'select') {
            let o = selectOptionTemplate.cloneNode(true)
            let oSelect = o.querySelector('.option-select')
            let oName = o.querySelector('.option-select-name')
            oName.innerText = `${opt.name}`

            for (let select_o of opt.options) {
                let dom_o = document.createElement('option')
                dom_o.value = select_o
                dom_o.text = select_o

                oSelect.appendChild(dom_o)
            }

            function selectUpdate() {
                eel.option_update(opt.id, oSelect.value)
                localStorage.setItem(opt.name, oSelect.value)
            }
            oSelect.onchange = selectUpdate

            oSelect.value = opt.options[0]

            if (defaultValue !== null) oSelect.value = defaultValue

            o.classList.remove('template')
            category.appendChild(o)

            selectUpdate()
        }

        category.classList.remove('template')
    }
}