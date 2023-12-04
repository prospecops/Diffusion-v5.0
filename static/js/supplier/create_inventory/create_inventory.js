// static/js/supplier/create_inventory/create_inventory.js

document.addEventListener('DOMContentLoaded', function() {
    const confirmCreateInventoryButton = document.getElementById('confirmCreateInventoryButton');

    function getCsrfToken() {
        const csrfTokenElement = document.getElementById('csrfToken');
        return csrfTokenElement ? csrfTokenElement.value : '';
    }

    function getIndividualCtmData() {
        const data = [];
        const rows = document.querySelectorAll('.individual-ctm-table tbody tr');
        rows.forEach(row => {
            if (row.cells.length > 1) {  // Ensure it's not a 'No data' row
                data.push({
                    ctm_name: row.cells[0].textContent.trim(),
                    kit_serial_number: row.cells[1].textContent.trim(),
                    quantity: row.cells[2].textContent.trim(),
                    expiration_date: row.cells[3].textContent.trim(),
                    lot_number: row.cells[4].textContent.trim()
                });
            }
        });
        console.log('Individual CTM Data:', data);  // Log the collected data
        return data;
    }

    confirmCreateInventoryButton.addEventListener('click', function() {
        console.log('Create Inventory button clicked.');  // Log button click

        const individualCtmData = getIndividualCtmData();

        console.log('Sending AJAX request with data:', individualCtmData);  // Log the data being sent

        fetch('/supplier/process_ctm_entries/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
                'X-Requested-With': 'XMLHttpRequest'  // Add this line
            },
            body: JSON.stringify({ individualCtm: individualCtmData })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Response received:', data);  // Log the response from the server
            // ... rest of your success/error handling code ...
        })
        .catch(error => {
            console.error('Error in AJAX request:', error);  // Log any errors
        });
    });
});

