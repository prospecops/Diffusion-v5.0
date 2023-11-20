// static/js/supplier/create_inventory/create_bulk_ctm.js

document.addEventListener('DOMContentLoaded', function() {
    const bulkCtmModal = document.getElementById('addBulkCTM');
    const ctmNameField = document.getElementById('bulkCtmNameField');
    const lotNumberField = document.getElementById('bulkCtmLotNumberField');
    const expirationDateField = document.getElementById('bulkCtmExpirationDateField');
    const quantityField = document.getElementById('bulkCtmQuantityField');
    const saveButton = document.getElementById('saveBulkCTMButton');

    // Function to check if all required fields are filled
    const areRequiredFieldsFilled = () => {
        const isExpirationValid = expirationDateField.value && new Date(expirationDateField.value) > new Date();
        const isQuantityNumeric = /^\d+$/.test(quantityField.value.trim());
        return ctmNameField.value.trim() && lotNumberField.value.trim() && isExpirationValid && isQuantityNumeric;
    };

    // Update the state of the Save button based on field inputs
    const updateFormState = () => {
        saveButton.disabled = !areRequiredFieldsFilled();
    };

    // Add event listeners to input fields to dynamically update form state
    [ctmNameField, lotNumberField, expirationDateField, quantityField].forEach(field => {
        field.addEventListener('input', updateFormState);
    });

    // Function to add or update the bulk CTM entry in the table
    const updateBulkCtmTable = () => {
        const tableBody = document.querySelector('.bulk-ctm-table tbody');
        let rowExists = false;

        // Remove 'No data' message if it exists
        const noDataMessage = tableBody.querySelector('tr td[colspan]');
        if (noDataMessage) {
            noDataMessage.parentElement.remove();
        }

        // Update or add new row
        for (const row of tableBody.rows) {
            if (row.cells[0].textContent === ctmNameField.value &&
                row.cells[2].textContent === expirationDateField.value &&
                row.cells[3].textContent === lotNumberField.value) {
                    const newQuantity = parseInt(row.cells[1].textContent) + parseInt(quantityField.value);
                    row.cells[1].textContent = newQuantity;
                    rowExists = true;
                    break;
            }
        }

        if (!rowExists) {
            const newRow = tableBody.insertRow();
            newRow.innerHTML = `
                <td>${ctmNameField.value}</td>
                <td>${quantityField.value}</td>
                <td>${expirationDateField.value}</td>
                <td>${lotNumberField.value}</td>
            `;
        }
    };

    // Event listener for the Save button
    saveButton.addEventListener('click', function(event) {
        event.preventDefault();
        if (areRequiredFieldsFilled()) {
            updateBulkCtmTable();
            $(bulkCtmModal).modal('hide');
            ctmNameField.value = '';
            lotNumberField.value = '';
            expirationDateField.value = '';
            quantityField.value = '';
        } else {
            alert('Please ensure all fields are correctly filled.');
        }
    });

    // Reset fields when the modal is opened
    bulkCtmModal.addEventListener('show.bs.modal', function() {
        ctmNameField.value = '';
        lotNumberField.value = '';
        expirationDateField.value = '';
        quantityField.value = '';
        updateFormState();
    });
});

