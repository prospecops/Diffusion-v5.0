// static/js/supplier/create_inventory/create_individual_ctm.js
document.addEventListener('DOMContentLoaded', function() {
    // References to the modal and form elements
    const individualCtmModal = document.getElementById('addIndividualCTM');
    const ctmNameField = document.getElementById('individualCtmNameField');
    const kitSerialNumberField = document.getElementById('individualCtmKitSerialNumberField');
    const lotNumberField = document.getElementById('individualCtmLotNumberField');
    const expirationDateField = document.getElementById('individualCtmExpirationDateField');
    const quantityField = document.getElementById('individualCtmQuantityField');
    const saveButton = document.getElementById('saveIndividualCTMButton');

    // Initialize the quantity field as non-editable
    quantityField.readOnly = true;
    quantityField.style.backgroundColor = "lightgrey";

    // Function to check if a string is a number
    const isNumber = (value) => /^\d+$/.test(value);

    // Function to check if all required fields (excluding quantity) are filled
    const areRequiredFieldsFilled = () => {
        const isExpirationValid = expirationDateField.value && new Date(expirationDateField.value) > new Date();
        const isSerialNumberNumeric = isNumber(kitSerialNumberField.value.trim());
        return ctmNameField.value.trim() && isSerialNumberNumeric &&
               lotNumberField.value.trim() && isExpirationValid;
    };

    // Update the state of the Save button based on field inputs
    const updateFormState = () => {
        saveButton.disabled = !areRequiredFieldsFilled();
        if (areRequiredFieldsFilled()) {
            quantityField.value = 1; // Auto-set quantity to 1
        } else {
            quantityField.value = ''; // Clear quantity if fields are not valid
        }
    };

    // Add event listeners to input fields to dynamically update form state
    [ctmNameField, kitSerialNumberField, lotNumberField, expirationDateField].forEach(field => {
        field.addEventListener('input', updateFormState);
    });

    // Function to check if the Kit/Serial Number is unique or if the table is initially empty
    const isKitSerialNumberUnique = () => {
        const rows = document.querySelectorAll('.individual-ctm-table tbody tr');
        const noDataMessage = document.querySelector('.individual-ctm-table tbody tr td[colspan="5"]');

        if (rows.length === 1 && noDataMessage) {
            return true; // If only 'No data' message, consider unique
        }

        for (const row of rows) {
            if (row.cells && row.cells[1] && row.cells[1].textContent === kitSerialNumberField.value.trim()) {
                return false; // Serial number is not unique
            }
        }
        return true; // Serial number is unique
    };

    // Function to add a new CTM entry to the table
    const addToIndividualCtmInventoryTable = () => {
        const tableBody = document.querySelector('.individual-ctm-table tbody');
        const newRow = document.createElement('tr');

        newRow.innerHTML = `
            <td>${ctmNameField.value}</td>
            <td>${kitSerialNumberField.value}</td>
            <td>1</td>
            <td>${expirationDateField.value}</td>
            <td>${lotNumberField.value}</td>
        `;

        const noDataMessage = tableBody.querySelector('tr td[colspan="5"]');
        if (noDataMessage) {
            noDataMessage.parentElement.remove(); // Remove 'No data' message
        }

        tableBody.appendChild(newRow); // Add new row to the table
    };

    // Function to reset the modal fields
    const resetModalFields = () => {
        ctmNameField.value = '';
        kitSerialNumberField.value = '';
        lotNumberField.value = '';
        expirationDateField.value = '';
        quantityField.value = '';
        updateFormState();
    };

    // Event listener for the Save button
    saveButton.addEventListener('click', function(event) {
        event.preventDefault();
        if (!isNumber(kitSerialNumberField.value.trim())) {
            alert('Kit/Serial Number must be a numeric value.');
            return;
        }
        if (areRequiredFieldsFilled() && isKitSerialNumberUnique()) {
            addToIndividualCtmInventoryTable();
            resetModalFields();
            $(individualCtmModal).modal('hide');
        } else {
            alert('Please ensure all fields are correctly filled and the Kit/Serial Number is unique.');
        }
    });

    // Reset fields when the modal is opened
    individualCtmModal.addEventListener('show.bs.modal', resetModalFields);

    // Initialize the form state
    resetModalFields();
});

