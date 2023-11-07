// update_ctm_fields.js

// Event handling after DOM content is fully loaded
document.addEventListener('DOMContentLoaded', function() {
  // Define references to the dropdowns and input fields
  const ctmField = document.getElementById('ctmField');
  const kitSerialField = document.getElementById('kitSerialField');
  const lotField = document.getElementById('lotField');
  const quantityField = document.getElementById('quantityField');
  const expirationDateField = document.getElementById('expirationDateField');

  // Fetch the ctmsWithKitsData from the script tag
  const ctmsWithKitsData = JSON.parse(document.getElementById('ctmsWithKitsData').textContent);

  // Function to reset Kit/Serial Numbers
  const resetKitSerialNumbers = () => {
    kitSerialField.innerHTML = '<option value="" selected>Select Kit/Serial Number</option>'; // Reset to default option
  };

  // Function to clear Kit details fields
  const clearKitDetails = () => {
    lotField.value = '';
    quantityField.value = '';
    expirationDateField.value = '';
  };

  // Function to update the kit serial numbers based on selected CTM
  const updateKitSerialNumbers = (selectedCtmName) => {
    resetKitSerialNumbers(); // Clear previous options and set default
    ctmsWithKitsData.forEach(item => {
      if (item.ctm_name === selectedCtmName) {
        const option = new Option(item.kit_serial_number, item.kit_serial_number);
        kitSerialField.add(option);
      }
    });
  };

  // Function to update the kit details based on selected Kit Serial Number
  const updateKitDetails = (selectedSerialNumber) => {
    const selectedKit = ctmsWithKitsData.find(kit => kit.kit_serial_number === selectedSerialNumber);
    if (selectedKit) {
      lotField.value = selectedKit.lot_number;
      quantityField.value = selectedKit.quantity;
      expirationDateField.value = selectedKit.expiration_date;
    }
  };

  // Event listener for CTM field change
  ctmField.addEventListener('change', function() {
    if (this.value) {
      updateKitSerialNumbers(this.value);
    } else {
      resetKitSerialNumbers();
    }
    clearKitDetails(); // Clear the details fields whenever CTM changes
  });

  // Event listener for kit serial field change
  kitSerialField.addEventListener('change', function() {
    if (this.value) {
      updateKitDetails(this.value);
    } else {
      clearKitDetails();
    }
  });

  // Call reset functions on initial load to ensure proper state
  resetKitSerialNumbers();
  clearKitDetails();
});


