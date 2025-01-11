import { useState } from 'react';

export default function MyApp() {
    const [toggle, setToggle] = useState(true);
    const [ls,setLs]=useState("apple")
    const numbers = [1, 2, 3, 4, 5];
    const listItems = numbers.map((number) =>
        <li key={number}>{number}</li>
    );
    function handleSubmit(e) {
        e.preventDefault();
        // if (e.target.as.value=="ON"){
        //     setToggle("OFF");
        // }
        // else{
        //     setToggle("ON")
        // }
        setToggle(!toggle);
        // const res = e.target.mySelect.value;
        console.log(res);
        console.log('You clicked submit.');
    }
    function sel(e)
    {
        setLs(e.target.value);
    }
    return (
        <form>
            Select your favorite fruit:
            <select id="mySelect" value={ls} onChange={sel}> 
                <option value="apple">Apple</option>
                <option value="orange">Orange</option>
                <option value="pineapple">Pineapple</option>
                <option value="banana">Banana</option>
            </select>
            <button type="submit" id="as" onClick={handleSubmit}>ON</button>
            {
                toggle && <ol>{listItems}</ol>
            }
            <p>{ls}</p>
        </form>
    );
}
