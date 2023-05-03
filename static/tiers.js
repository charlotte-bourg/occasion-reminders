'use strict';

document.querySelector('#new-tier').addEventListener('submit', (evt) => {
    evt.preventDefault();

    const formInputs = {
        "tier-name": document.querySelector('#tier-name').value,
        "tier-desc": document.querySelector('#tier-desc').value,
        "tier-days-ahead":document.querySelector('#tier-days-ahead').value,
        "tier-reminder-type": document.querySelector('#tier-reminder-type').value
    };
    fetch('/add-tier', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then((response) => response.json())
        .then((responseData) => {
            if (responseData["success"]){
                document.querySelector('#tiers-table').insertAdjacentHTML('beforeend',`<tr>
                    <td>${responseData["tier-name"]}</td>
                    <td>${responseData["tier-desc"]}</td>
                    <td>${responseData["tier-days-ahead"]}</td>
                    <td>${responseData["tier-reminder-type"]}</td>
                    </tr>`);
            }
        }); // consider changes for consistent sorting?
});

document.querySelector('.upd-tier').addEventListener('submit', (evt) =>{
    evt.preventDefault()
    const checkedBoxes = document.querySelectorAll('input[type="checkbox"]:checked')
    var occasion_ids = []
    for (const box of checkedBoxes){
        occasion_ids.push(box.id)
    }
    const formInputs = {    
        tier_id: document.querySelector('#tier-dropdown').value,
        occasion_ids: occasion_ids
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
                 for (const occasion_id of occasion_ids){
                    document.querySelector(`span.tier_name_${occasion_id}`).innerHTML = responseData["tier_name"];
                 }
             }
     }); 
});
const deleteButtons = document.querySelectorAll('.del-tier')
for (const delButton of deleteButtons){
    delButton.addEventListener('click', () => {
        const tier_id = delButton.id
        console.log(`tier_id is ${tier_id}`)
        fetch(`/tier-in-use?tier_id=${tier_id}`)
            .then((response) => response.json())
            .then((responseData) => {
                console.log(responseData)
                if (responseData["in_use"]){
                    const confirmed = confirm("This group is in use! Are you sure you'd like to delete it?");
                    if (confirmed){deleteTier(tier_id)}
                }
                else{
                    deleteTier(tier_id)
                }
            }); 
    })
}

function deleteTier(tier_id){
    console.log(tier_id)
    fetch('/delete-tier', {
         method: 'POST',
         body: JSON.stringify({"tier_id": tier_id}),
         headers: {
             'Content-Type': 'application/json'
         },
     })
         .then((response) => response.json())
         .then((responseData) => {
            if (responseData["success"]){
                console.log("the affected occasions are as follows")
                for (const occasion_id of responseData["occasion_ids"]){
                    console.log(occasion_id)
                    document.querySelector(`span.tier_name_${occasion_id}`).innerHTML = "";
                }
                document.querySelector(`#tier_row_${tier_id}`).style.display= 'none'
            }
     }); 
};