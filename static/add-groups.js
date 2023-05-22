'use strict';

document.querySelector('#new-tier').addEventListener('submit', (evt) => {
    evt.preventDefault();
    const formInputs = {
        "tier-name": document.querySelector('#tier-name').value,
        "tier-desc": document.querySelector('#tier-desc').value,
        "tier-days-ahead": document.querySelector('#tier-days-ahead').value,
        "tier-reminder-type": document.querySelector('input[name="tier-reminder-type"]:checked').value
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
                document.querySelector('#no-groups').setAttribute("hidden", true)
                const tier_id = responseData["tier-id"]
                document.querySelector('#tiers-table').insertAdjacentHTML('beforeend',`<tr id=tier_row_${tier_id}>
                <td><button type="button" id="del_button_${tier_id}" class="del-tier"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16">
                <path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5ZM11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H2.506a.58.58 0 0 0-.01 0H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1h-.995a.59.59 0 0 0-.01 0H11Zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5h9.916Zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47ZM8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5Z"/>
              </svg></i></button></td><td>${responseData["tier-name"]}</td>
                    <td>${responseData["tier-desc"]}</td>
                    <td>${responseData["tier-days-ahead"]}</td>
                    <td>${responseData["tier-reminder-type"]}</td>
                    </tr>`);
                document.querySelector('#new-tier').reset()
                updateEventListeners(tier_id);
            }
        }); 
});

function updateEventListeners(tier_id){
    const newButton = document.querySelector(`#del_button_${tier_id}`)
    newButton.addEventListener('click', function(evt){
        deleteCheck(evt,tier_id)
    });
}

const deleteButtons = document.querySelectorAll('.del-tier')
for (const delButton of deleteButtons){
    delButton.addEventListener('click', function(evt){
        deleteCheck(evt,delButton.id.substring(11))
    });
}

function deleteCheck(evt, tier_id){
    console.log(`tier_id is ${tier_id}`)
    fetch(`/tier-in-use?tier_id=${tier_id}`)
        .then((response) => response.json())
        .then((responseData) => {
            console.log(responseData)
            if (responseData["in_use"]){
                const confirmationModal = new bootstrap.Modal(document.getElementById('inUseConfirmation'))
                document.querySelector('#confirm').addEventListener('click',() => deleteTier(tier_id))
                confirmationModal.show()
            }
            else{
                deleteTier(tier_id)
            }
        }); 
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
                document.querySelector(`#tier_row_${tier_id}`).style.display= 'none'
                if (!responseData["tiers"]){
                    document.querySelector('#no-groups').removeAttribute("hidden")
                }
            }
     }); 
};