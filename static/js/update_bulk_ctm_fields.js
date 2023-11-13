// update_bulk_ctm_fields.js

document.addEventListener('DOMContentLoaded', function() {
  const bulkCtmField = document.getElementById('bulkCtmField');
  const bulkLotField = document.getElementById('bulkLotField');
  const bulkQuantityField = document.getElementById('bulkQuantityField');
  const bulkExpirationDateField = document.getElementById('bulkExpirationDateField');
  const bulkSaveButton = document.getElementById('bulkSaveButton');
  const bulkSaveAddNewButton = document.getElementById('bulkSaveAddNewButton');
  const bulkCtmsData = JSON.parse(document.getElementById('bulkCtmsData').textContent);

  const resetQuantityAndExpiration = () => {
    bulkQuantityField.value = '';
    bulkExpirationDateField.value = '';
    bulkQuantityField.setAttribute('readonly', 'true'); // Set quantity field to readonly
    disableSaveButtons();
  };

  const disableSaveButtons = () => {
    bulkSaveButton.disabled = true;
    bulkSaveAddNewButton.disabled = true;
  };

  const enableSaveButtons = () => {
    bulkSaveButton.disabled = false;
    bulkSaveAddNewButton.disabled = false;
  };

  const resetBulkModal = () => {
    bulkCtmField.selectedIndex = 0;
    bulkLotField.innerHTML = '<option value="" disabled selected>Select Lot #</option>';
    bulkLotField.disabled = true; // Disable lot field initially
    resetQuantityAndExpiration();
  };

  const updateBulkLotNumbers = (selectedBulkCtmName) => {
    bulkLotField.innerHTML = '<option value="" disabled selected>Select Lot #</option>';
    bulkLotField.disabled = false;

    const relevantLots = bulkCtmsData.filter(item => item.ctm_name === selectedBulkCtmName);
    relevantLots.forEach(item => {
      const option = document.createElement('option');
      option.value = item.lot_number;
      option.text = item.lot_number;
      option.disabled = item.quantity === 0; // Disable if no quantity left
      bulkLotField.appendChild(option);
    });

    resetQuantityAndExpiration();
  };

  bulkCtmField.addEventListener('change', function() {
    updateBulkLotNumbers(this.value);
  });

  bulkLotField.addEventListener('change', function() {
    const selectedLot = bulkCtmsData.find(lot => lot.lot_number === this.value && lot.ctm_name === bulkCtmField.value);

    if (selectedLot) {
      bulkQuantityField.value = selectedLot.quantity;
      bulkQuantityField.removeAttribute('readonly');
      bulkExpirationDateField.value = selectedLot.expiration_date;
      enableSaveButtons();
    } else {
      resetQuantityAndExpiration();
    }
  });

  const checkDropdownSelections = () => {
    if (bulkCtmField.value && bulkLotField.value) {
      enableSaveButtons();
    } else {
      disableSaveButtons();
    }
  };

  bulkCtmField.addEventListener('change', checkDropdownSelections);
  bulkLotField.addEventListener('change', checkDropdownSelections);

  const bulkModal = document.getElementById('bulkCTMModal');
  bulkModal.addEventListener('hidden.bs.modal', resetBulkModal);

  const validateQuantity = () => {
    const enteredQuantity = parseInt(bulkQuantityField.value, 10);
    const selectedLot = bulkCtmsData.find(lot => lot.lot_number === bulkLotField.value && lot.ctm_name === bulkCtmField.value);

    if (isNaN(enteredQuantity)) {
      alert('Invalid input. Please enter a numeric value for the quantity.');
      return false;
    }

    if (enteredQuantity <= 0) {
      alert('Invalid quantity. The quantity must be greater than zero.');
      return false;
    }

    if (enteredQuantity > selectedLot.quantity) {
      alert(`Invalid quantity. The quantity exceeds the available stock. Available quantity: ${selectedLot.quantity}.`);
      return false;
    }

    return true;
  };

const updateTableAndData = (ctmName, lotNumber, usedQuantity) => {
  const selectedLot = bulkCtmsData.find(lot => lot.lot_number === lotNumber && lot.ctm_name === ctmName);
  if (selectedLot) {
    selectedLot.quantity -= usedQuantity; // Update the remaining quantity

    // Get the table body element
    const tableBody = document.querySelector('.bulk-ctm-table tbody');

    // Check if the 'No bulk CTM inventory available' message exists and remove it
    const noDataMessage = tableBody.querySelector('tr td[colspan="4"]');
    if (noDataMessage) {
      noDataMessage.parentElement.remove();
    }

    // Update or add the entry in the table
    const existingRow = document.querySelector(`.bulk-ctm-table tr[data-ctm-name="${ctmName}"][data-lot-number="${lotNumber}"]`);
    if (existingRow) {
      existingRow.cells[1].textContent = parseInt(existingRow.cells[1].textContent) + usedQuantity;
    } else {
      const row = tableBody.insertRow();
      row.setAttribute('data-ctm-name', ctmName);
      row.setAttribute('data-lot-number', lotNumber);
      row.insertCell(0).textContent = ctmName;
      row.insertCell(1).textContent = usedQuantity;
      row.insertCell(2).textContent = selectedLot.expiration_date;
      row.insertCell(3).textContent = lotNumber;
    }
  }
};

  bulkSaveButton.addEventListener('click', function(event) {
    event.preventDefault();
    if (validateQuantity()) {
      const usedQuantity = parseInt(bulkQuantityField.value, 10);
      updateTableAndData(bulkCtmField.value, bulkLotField.value, usedQuantity);
      $('#bulkCTMModal').modal('hide');
      resetBulkModal(); // Reset the modal after saving
    }
  });

  bulkSaveAddNewButton.addEventListener('click', function(event) {
    event.preventDefault();
    if (validateQuantity()) {
      const usedQuantity = parseInt(bulkQuantityField.value, 10);
      updateTableAndData(bulkCtmField.value, bulkLotField.value, usedQuantity);
      resetBulkModal(); // Reset the modal for new entry
    }
  });

  resetBulkModal(); // Initialize the modal in its default state
});
