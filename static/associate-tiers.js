'use strict';

const updateButtons = document.querySelectorAll('.upd-tier')
for (const button of updateButtons){
    button.addEventListener('click', () =>{
        const newTier = prompt('What tier would you like to add to this occasion?');
        const formInputs = {
            tier_id: newTier,
            occasion_id: button.id, 
        };
        fetch('/update-tier', {
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
}
