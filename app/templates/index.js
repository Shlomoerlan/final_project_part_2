const setInputsDisabledByRoutes = (value) => {
    const routes = {
        enosh: ['area'],
        matanel: ['area', 'area-input'],
        itshak: [''],
        alef: ['area-input']
    }
    const allInputs = ['area', 'area-input'].map(id => document.getElementById(id))
    
    allInputs.forEach((node) => {
        node.disabled = !routes[value].includes(node.id)
    })   
}

(() => {
    const routeValue = document.getElementById("routes").value
    setInputsDisabledByRoutes(routeValue)
    document.getElementById("routes").addEventListener('change', ({ target: { value}}) => {
        setInputsDisabledByRoutes(value)
    })
})()



const fetchData = async (additionalUrl = "", port = 5000) => {
    const BASE_URL = `http://localhost:${port}/${additionalUrl}`
    const response = await fetch(BASE_URL)
    return await response.json()
}

const extractFormValues = () =>  [...document.getElementsByClassName("form-value")]
    .filter(n => !n.disabled)
    .map(n => n.value)

const sendRequest = async () => {
    const { map } = await fetchData("api/attack-types/top-5")
    document.getElementById("map").innerHTML = map
}