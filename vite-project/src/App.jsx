import { useState } from 'react'

const apiKey = "7d8833b1736e90a49d361b2b3270dadc";

function App() {
    const [icon, setIcon] = useState("https://openweathermap.org/img/wn/10d@2x.png")
    const [temp,settemp]=useState("20")
    const[humidity,setHumidity]=useState("20")
    const [speed,setSpeed]=useState("30")
    const [city, setCity] = useState("")
    function handleSubmit(event) {
        event.preventDefault();
        const cityName = event.target.city.value;
        setCity(cityName);
        if (!cityName) {
            alert("Please Enter city Name!!")
            return
        }
        console.log('City:', cityName);
        fetch("https://api.openweathermap.org/data/2.5/weather?q="+cityName+"&units=metric&appid=7d8833b1736e90a49d361b2b3270dadc")
            .then(responce => {
                if (!responce.ok) {
                    throw new Error()
                }
                return responce.json()
            })
            .then(data => {
                setIcon("https://openweathermap.org/img/wn/" + data.weather[0].icon + "@2x.png");
                settemp(data.main.temp)
                console.log("temp",data.main.temp);
                setHumidity(data.main.humidity)
                console.log("humidity",data.main.humidity);
                setSpeed(data.wind.speed)
                console.log("Wind",data.wind.speed);
                setCity(data.name);
                console.log(data.name);
            })
            .catch(error => {
                alert("Unable to fetch the wheather forecast")
            })
    }
    return (
        <div className="container my-5">
            <div className="mx-auto rounded border text-center text-white p-4"
                style={{
                    backgroundColor: "#3B5FAB", width: "400px"
                }}>
                <h2 className="fw-bold mb-5">wheather Forecast</h2>
                <div className="container-fluid">
                    <form className="d-flex" role="search" onSubmit={handleSubmit}>
                        <input className="form-control me-2" type="search" placeholder="city" name="city" />
                        <button type="submit" className="btn btn-outline-dark">Search</button>
                    </form>
                    {city && <p>Searching for city: {city}</p>}
                </div>
                <img src={icon} alt="wheather" />
                <h1 className='display-4 fw-medium'>{temp}°C</h1>
                <h1 className="mb-5">{city}</h1>
                <div className="row mb-3">
                    <div className="col">
                        <i className="bi bi-droplet-half"></i>
                        Humidity<br />{humidity}%
                    </div>
                    <div className="col">
                        <i className="bi bi-wind"></i>Wind Speed<br />{speed}kmph

                    </div>
                </div>
            </div>
        </div>
    )
}

export default App
