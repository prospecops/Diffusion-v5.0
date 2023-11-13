// update_individual_ctm_fields.js

document.addEventListener('DOMContentLoaded', function() {
  // Get references to the form elements.
  const ctmField = document.getElementById('ctmField');
  const kitSerialField = document.getElementById('kitSerialField');
  const individualLotField = document.getElementById('individualLotField');
  const quantityField = document.getElementById('quantityField');
  const expirationDateField = document.getElementById('expirationDateField');
  const saveButton = document.getElementById('saveButton');
  const saveAndAddNewButton = document.getElementById('saveAddNewButton');

  // Function to reset the related fields and disable save buttons.
  const clearRelatedFieldsAndDisableButtons = () => {
    kitSerialField.innerHTML = '<option value="" disabled selected>Select Kit/Serial #</option>';
    individualLotField.value = '';
    quantityField.value = '';
    expirationDateField.value = '';
    saveButton.disabled = true;
    saveAndAddNewButton.disabled = true;
    kitSerialField.disabled = true; // Disable this dropdown initially.
  };

  // Fetch the CTM data from the script tag.
  const ctmsWithKitsData = JSON.parse(document.getElementById('ctmsWithKitsData').textContent);

  // Function to update Kit/Serial Number options based on the selected CTM.
  const updateKitSerialNumbers = (selectedCtmName) => {
    clearRelatedFieldsAndDisableButtons(); // Clear related fields upon CTM change.
    kitSerialField.disabled = false; // Enable the dropdown.

    ctmsWithKitsData.forEach(item => {
      if (item.ctm_name === selectedCtmName) {
        const option = new Option(item.kit_serial_number, item.kit_serial_number);
        if (item.selected) {
          option.disabled = true;
        }
        kitSerialField.add(option);
      }
    });

    checkAndDisableCtmOption(selectedCtmName);
  };

  // Function to disable CTM option if all its kits are selected
  const checkAndDisableCtmOption = (ctmName) => {
    const allSelected = ctmsWithKitsData.every(item => item.ctm_name !== ctmName || item.selected);
    if (allSelected) {
      const ctmOption = ctmField.querySelector(`option[value="${ctmName}"]`);
      if (ctmOption) {
        ctmOption.disabled = true;
      }
    }
  };

  // Add event listener to the CTM dropdown to disable the 'Select CTM' option once dropdown is opened
  ctmField.addEventListener('mousedown', function() {
    this.querySelector('option[value=""]').disabled = true;
  });

  // Add event listeners to CTM and Kit/Serial Number dropdowns.
  ctmField.addEventListener('change', function() {
    updateKitSerialNumbers(this.value);
  });

  kitSerialField.addEventListener('change', function() {
    if (this.value) {
      const selectedKit = ctmsWithKitsData.find(kit => kit.kit_serial_number === this.value);
      if (selectedKit) {
        // If a valid kit is selected, populate the related fields and enable save buttons.
        individualLotField.value = selectedKit.lot_number;
        quantityField.value = selectedKit.quantity;
        expirationDateField.value = selectedKit.expiration_date;
        saveButton.disabled = false;
        saveAndAddNewButton.disabled = false;
      }
    } else {
      // If the kit selection is reset, clear the related fields and disable save buttons.
      clearRelatedFieldsAndDisableButtons();
    }
  });

  // Function to add new CTM data to the table
  const addCtmToTable = (ctmData) => {
    const tableBody = document.querySelector('.individual-ctm-table tbody');

    // Check if the 'no data' message exists and remove it
    const noDataMessage = tableBody.querySelector('tr td[colspan="5"]');
    if (noDataMessage) {
      noDataMessage.parentElement.remove();
    }

    // Create a new row for the CTM data
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${ctmData.ctm_name}</td>
      <td>${ctmData.kit_serial_number}</td>
      <td>${ctmData.quantity}</td>
      <td>${ctmData.expiration_date}</td>
      <td>${ctmData.lot_number}</td>
    `;
    tableBody.appendChild(row);
  };

  // Event listener for the Save button
  saveButton.addEventListener('click', function(event) {
    event.preventDefault();
    const ctmData = {
      ctm_name: ctmField.value,
      kit_serial_number: kitSerialField.value,
      quantity: quantityField.value,
      expiration_date: expirationDateField.value,
      lot_number: individualLotField.value
    };

    addCtmToTable(ctmData);

    // Mark the selected kit as selected in the ctmsWithKitsData
    const selectedKit = ctmsWithKitsData.find(kit => kit.kit_serial_number === ctmData.kit_serial_number);
    if (selectedKit) {
      selectedKit.selected = true;
    }

    // Update CTM dropdown options after saving
    checkAndDisableCtmOption(ctmData.ctm_name);

    $('#individualCTMModal').modal('hide');
    clearRelatedFieldsAndDisableButtons();
  });

  // Reset the form when the modal is opened.
  document.getElementById('individualCTMModal').addEventListener('show.bs.modal', function() {
    clearRelatedFieldsAndDisableButtons();
    ctmField.value = "";
    ctmField.querySelectorAll('option').forEach(option => option.disabled = false); // Re-enable all CTM options
  });

  // Call the function to set the initial state of the modal on page load.
  clearRelatedFieldsAndDisableButtons();
});
