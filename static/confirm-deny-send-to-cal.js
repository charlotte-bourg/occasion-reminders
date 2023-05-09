'use strict';

document.querySelector('#approve').addEventListener('click', () =>{
    fetch('/add-events', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then((response) => response.json())
        .then((responseData) => {
            if (responseData["success"]){
                document.querySelector(`span.tier_name_${button.id}`).innerHTML = responseData["tier_name"];
            }
    }); 
});

