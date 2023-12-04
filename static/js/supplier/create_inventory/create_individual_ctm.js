// static/js/supplier/create_inventory/create_individual_ctm.js
document.addEventListener('DOMContentLoaded', function() {
    // --------------- Session Management ---------------
    // Generates and stores a unique session ID
    const pageSessionId = uuid.v4(); // Using uuid library to generate a valid UUID
    sessionStorage.setItem('pageSessionId', pageSessionId);

    function generateUniqueSessionId() {
        // Creates a unique identifier based on current time and random numbers
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    // --------------- References to the modal and form elements ---------------
    // Grabbing HTML elements by their IDs for manipulation
    const individualCtmModal = document.getElementById('addIndividualCTM');
    const ctmNameField = document.getElementById('individualCtmNameField');
    const kitSerialNumberField = document.getElementById('individualCtmKitSerialNumberField');
    const lotNumberField = document.getElementById('individualCtmLotNumberField');
    const expirationDateField = document.getElementById('individualCtmExpirationDateField');
    const quantityField = document.getElementById('individualCtmQuantityField');
    const saveButton = document.getElementById('saveIndividualCTMButton');

    // Setting the quantity field as non-editable
    quantityField.readOnly = true;
    quantityField.style.backgroundColor = "lightgrey";

    // --------------- Utility Functions ---------------
    // Function to check if a string is a number
    const isNumber = (value) => /^\d+$/.test(value);

    // Functions to validate individual fields
    const validateKitSerialNumberFormat = () => {
        const kitSerialValue = kitSerialNumberField.value.trim();
        return kitSerialValue.length > 0 && /^\d{5,10}$/.test(kitSerialValue);
    };

    const validateExpirationDate = () => {
        const expirationDate = new Date(expirationDateField.value);
        const currentDate = new Date();
        currentDate.setHours(0, 0, 0, 0);
        return expirationDateField.value && expirationDate > currentDate;
    };

    const validateCtmNameFormat = () => {
        const ctmNameValue = ctmNameField.value.trim();
        return ctmNameValue.length <= 100 && /^[a-zA-Z0-9\s]+$/.test(ctmNameValue);
    };

    const validateLotNumberFormat = () => {
        const lotNumberValue = lotNumberField.value.trim();
        return lotNumberValue.length > 0 && /^[A-Za-z0-9-]{3,20}$/.test(lotNumberValue);
    };

    // Function to check if all required fields are filled
    const areRequiredFieldsFilled = () => {
        return validateCtmNameFormat() &&
               validateKitSerialNumberFormat() &&
               validateLotNumberFormat() &&
               validateExpirationDate();
    };

    // --------------- Backend Communication Functions ---------------
    // Function to send CTM entry data to the backend
    const addCtmEntryToBackend = () => {
        const ctmData = {
            page_session_id: sessionStorage.getItem('pageSessionId'),
            ctm_name: ctmNameField.value.trim(),
            kit_serial_number: kitSerialNumberField.value.trim(),
            quantity: 1, // Quantity is always 1 for individual CTM
            expiration_date: expirationDateField.value,
            lot_number: lotNumberField.value.trim()
        };

        fetch('/supplier/process_ctm_entries/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ individualCtm: [ctmData] })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                addToIndividualCtmInventoryTable(ctmData);
                resetModalFields();
                $(individualCtmModal).modal('hide');
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while saving the CTM entry.');
        });
    };

    // JavaScript to send cleanup request with CSRF token
    document.addEventListener('visibilitychange', function() {
        if (document.visibilityState === 'hidden') {
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const sessionId = sessionStorage.getItem('pageSessionId');
            const data = new FormData();
            data.append('csrfmiddlewaretoken', csrfToken);
            data.append('session_id', sessionId);

            navigator.sendBeacon('/supplier/cleanup_sessions/', data);
        }
    });


    // --------------- Event Listeners and Handlers ---------------
    // Function to update the state of the Save button based on field inputs
    const updateFormState = () => {
        saveButton.disabled = !areRequiredFieldsFilled();
        if (areRequiredFieldsFilled()) {
            quantityField.value = 1; // Auto-set quantity to 1
        } else {
            quantityField.value = ''; // Clear quantity if fields are not valid
        }
    };

    // Adding input event listeners to form fields for dynamic form state updates
    [ctmNameField, kitSerialNumberField, lotNumberField, expirationDateField].forEach(field => {
        field.addEventListener('input', updateFormState);
    });

    // Event listener for the Save button
    saveButton.addEventListener('click', function(event) {
        event.preventDefault();
        if (!isNumber(kitSerialNumberField.value.trim())) {
            alert('Kit/Serial Number must be a numeric value.');
            return;
        }
        if (areRequiredFieldsFilled() && isKitSerialNumberUnique()) {
            addCtmEntryToBackend(); // Call backend communication function instead of directly adding to table
            // addToIndividualCtmInventoryTable();
            // resetModalFields();
            // $(individualCtmModal).modal('hide');
        } else {
            alert('Please ensure all fields are correctly filled and the Kit/Serial Number is unique.');
        }
    });

    // --------------- Table Manipulation Functions ---------------
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

    // --------------- Modal State Management Functions ---------------
    // Function to reset the modal fields when opened
    const resetModalFields = () => {
        ctmNameField.value = '';
        kitSerialNumberField.value = '';
        lotNumberField.value = '';
        expirationDateField.value = '';
        quantityField.value = '';
        updateFormState(); // Update form state after resetting fields
    };

    // Event listener to reset modal fields when it is opened
    individualCtmModal.addEventListener('show.bs.modal', resetModalFields);

    // Function to retrieve CSRF token from HTML
    const getCsrfToken = () => {
        const csrfTokenInput = document.getElementById('csrfToken');
        return csrfTokenInput ? csrfTokenInput.value : '';
    };

    // Function to check if Kit/Serial Number is unique (requires backend endpoint)
    const isKitSerialNumberUnique = () => {
        // Placeholder for backend check functionality
        return true;
    };
});


