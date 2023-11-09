// update_bulk_ctm_fields.js
document.addEventListener('DOMContentLoaded', function() {
  const bulkCtmField = document.getElementById('bulkCtmField');
  const bulkLotField = document.getElementById('bulkLotField');
  const bulkQuantityField = document.getElementById('bulkQuantityField');
  const bulkExpirationDateField = document.getElementById('bulkExpirationDateField');
  const bulkSaveButton = document.getElementById('bulkSaveButton');
  const bulkCtmsData = JSON.parse(document.getElementById('bulkCtmsData').textContent);

  const updateBulkLotNumbers = (selectedBulkCtmName) => {
    bulkLotField.innerHTML = '<option value="" disabled selected>Select Lot #</option>';
    bulkLotField.disabled = false;

    const relevantLots = bulkCtmsData.filter(item => item.ctm_name === selectedBulkCtmName);
    relevantLots.forEach(item => {
      const option = document.createElement('option');
      option.value = item.lot_number;
      option.text = item.lot_number;
      bulkLotField.appendChild(option);
    });
  };

  bulkCtmField.addEventListener('change', function() {
    updateBulkLotNumbers(this.value);
    bulkQuantityField.value = '';
    bulkExpirationDateField.value = '';
    bulkQuantityField.setAttribute('readonly', 'true');
    bulkExpirationDateField.setAttribute('readonly', 'true');
  });

  bulkLotField.addEventListener('change', function() {
    const selectedLot = bulkCtmsData.find(lot => lot.lot_number === this.value && lot.ctm_name === bulkCtmField.value);

    if (selectedLot) {
      bulkQuantityField.value = selectedLot.quantity;
      bulkQuantityField.removeAttribute('readonly');
      bulkQuantityField.max = selectedLot.quantity;
      bulkExpirationDateField.value = selectedLot.expiration_date;
      bulkExpirationDateField.removeAttribute('readonly');
    }
  });

  // Save button click event listener
  bulkSaveButton.addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const quantityValue = parseInt(bulkQuantityField.value, 10);
    const maxQuantity = parseInt(bulkQuantityField.max, 10);

    // Check for a valid number
    if (isNaN(quantityValue) || quantityValue < 0) {
      alert('Please enter a valid whole number equal to or greater than 0.');
      bulkQuantityField.value = bulkQuantityField.max;
      return;
    }

    // Check if the quantity does not exceed the maximum
    if (quantityValue > maxQuantity) {
      alert('The quantity entered exceeds the available stock.');
      bulkQuantityField.value = bulkQuantityField.max;
      return;
    }

    const isValidLot = bulkLotField.value !== "";
    const isValidCtm = bulkCtmField.value !== "";

    if (isValidLot && isValidCtm) {
      // If validation passes, submit the form or perform the save action
      console.log('Form is valid. Implement the submission logic here.');
      // Example: submitForm();
    } else {
      // If validation fails, the form will not be submitted
      console.log('Form is invalid. Check all fields.');
      // Show error messages as needed
    }
  });

  // Add an event listener for closing the modal
  const bulkModal = document.getElementById('bulkCTMModal'); // Replace 'bulkModal' with the actual ID of your modal
  bulkModal.addEventListener('hidden.bs.modal', resetBulkModal);

  function resetBulkModal() {
    bulkCtmField.selectedIndex = 0;
    bulkLotField.innerHTML = '<option value="" disabled selected>Select Lot #</option>';
    bulkLotField.disabled = true;
    bulkQuantityField.value = '';
    bulkQuantityField.setAttribute('readonly', 'true');
    bulkExpirationDateField.value = '';
    bulkExpirationDateField.setAttribute('readonly', 'true');
  }

  // Call resetBulkModal if needed, for example, after successful form submission
  // resetBulkModal();
});


