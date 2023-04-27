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