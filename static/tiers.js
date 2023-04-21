'use strict';

function addTier(evt){
    evt.preventDefault();

    fetch('/add-tier')
        .then((response) => response.json())
        .then((responseData) => {
            document.querySelector('#').insertAdjacentHTML()
        }); 
}

document.querySelector('#new-tier').addEventListener()