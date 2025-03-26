let optionsContainer = document.getElementById('options_container')
let categoryTemplate = document.getElementsByClassName('options-category')[0]
let rangeOptionTemplate = document.getElementsByClassName('option-range-container')[0]
let checkboxOptionTemplate = document.getElementsByClassName('option-checkbox-container')[0]
let selectOptionTemplate = document.getElementsByClassName('option-select-container')[0]

eel.expose(registerOptions)

function registerOptions(options) {
    for (let opt of options) {
        console.log(opt)
        let category = document.getElementById(`category-${opt.category}`)

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
            }

            oRange.onchange = rangeUpdate

            o.classList.remove('template')
            category.appendChild(o)

            rangeUpdate()
        }
        else if (opt.type == 'checkbox') {
            let o = checkboxOptionTemplate.cloneNode(true)
            let oCheck = o.querySelector('.option-checkbox')
            let oName = o.querySelector('.option-checkbox-name')
            oName.innerText = `${opt.name}`

            function checkUpdate() { eel.option_update(opt.id, oCheck.checked) }
            oCheck.onchange = checkUpdate

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

            oSelect.value = opt.options[0]

            function selectUpdate() { eel.option_update(opt.id, oSelect.value) }
            oSelect.onchange = selectUpdate

            o.classList.remove('template')
            category.appendChild(o)

            selectUpdate()
        }

        category.classList.remove('template')
    }
}