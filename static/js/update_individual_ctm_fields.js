// update_ctm_fields.js

// Event handling after DOM content is fully loaded
document.addEventListener('DOMContentLoaded', function() {
  // Define references to the dropdowns and input fields
  const ctmField = document.getElementById('ctmField');
  const kitSerialField = document.getElementById('kitSerialField');
  const individualLotField = document.getElementById('individualLotField'); // Updated ID
  const quantityField = document.getElementById('quantityField');
  const expirationDateField = document.getElementById('expirationDateField');

  // Reset function to clear selections and details
  const resetFields = () => {
    // Clear the current selections
    ctmField.selectedIndex = 0;
    kitSerialField.innerHTML = '<option disabled selected>Select Kit / Serial #</option>';

    // Clear the kit details
    individualLotField.value = ''; // Updated ID
    quantityField.value = '';
    expirationDateField.value = '';

    // Disable the kitSerialField until a CTM is selected
    kitSerialField.disabled = true;
  };

  // Fetch the ctmsWithKitsData from the script tag
  const ctmsWithKitsData = JSON.parse(document.getElementById('ctmsWithKitsData').textContent);

  const updateKitSerialNumbers = (selectedCtmName) => {
    kitSerialField.innerHTML = '<option disabled selected>Select Kit / Serial #</option>'; // Reset the options
    kitSerialField.disabled = false; // Enable the dropdown
    ctmsWithKitsData.forEach(item => {
      if (item.ctm_name === selectedCtmName) {
        const option = new Option(item.kit_serial_number, item.kit_serial_number);
        kitSerialField.add(option);
      }
    });

    // Clear the kit details since the previous selection is no longer valid
    individualLotField.value = ''; // Updated ID
    quantityField.value = '';
    expirationDateField.value = '';
  };

  // Event listener to reset the modal when it's opened
  document.getElementById('individualCTMModal').addEventListener('show.bs.modal', resetFields);

  // Update kit serial numbers when a CTM name is selected
  ctmField.addEventListener('change', function() {
    updateKitSerialNumbers(this.value);
  });

  // Update kit details when a kit serial number is selected
  kitSerialField.addEventListener('change', function() {
    if(this.value) {
      const selectedKit = ctmsWithKitsData.find(kit => kit.kit_serial_number === this.value);
      if (selectedKit) {
        individualLotField.value = selectedKit.lot_number; // Updated ID
        quantityField.value = selectedKit.quantity;
        expirationDateField.value = selectedKit.expiration_date;
      }
    } else {
      // If no kit is selected, clear the details
      individualLotField.value = ''; // Updated ID
      quantityField.value = '';
      expirationDateField.value = '';
    }
  });

  // Call resetFields on page load to ensure everything is in its default state
  resetFields();
});

