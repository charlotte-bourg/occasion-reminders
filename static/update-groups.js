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