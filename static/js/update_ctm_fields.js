// update_ctm_fields.js

// Retrieve the serialized data
var ctmsWithKitsData = JSON.parse(document.getElementById('ctmsWithKitsData').textContent);

// Event handling after DOM content is fully loaded
document.addEventListener('DOMContentLoaded', function() {
  var ctmField = document.getElementById('ctmField');
  var kitSerialField = document.getElementById('kitSerialField');

  // Function to update kit serial numbers based on the selected CTM name
  function updateKitSerialNumbers(selectedCtmName) {
    kitSerialField.innerHTML = ''; // Clear previous options

    // Get unique CTM names and append options
    var ctmNamesSet = new Set(ctmsWithKitsData.map(item => item.ctm_name));
    ctmNamesSet.forEach(function(name) {
      if (name === selectedCtmName) {
        // Filter and append options related to the selected CTM
        ctmsWithKitsData.forEach(function(ctm) {
          if (ctm.ctm_name === name) {
            var option = new Option(ctm.kit_serial_number, ctm.kit_serial_number);
            kitSerialField.add(option);
          }
        });
      }
    });
  }

  // Update kit serial numbers when a CTM name is selected
  ctmField.addEventListener('change', function() {
    updateKitSerialNumbers(this.value);
    // Reset other fields
    document.getElementById('lotField').value = '';
    document.getElementById('quantityField').value = '';
    document.getElementById('expirationDateField').value = '';
  });

  // Initial population of kit serial numbers
  if(ctmField.selectedIndex >= 0) {
    updateKitSerialNumbers(ctmField.options[ctmField.selectedIndex].value);
  }

  kitSerialField.addEventListener('change', updateFieldsBasedOnSelection);
});

// Function to update the fields based on the selected Kit/Serial Number
function updateFieldsBasedOnSelection() {
  var selectedSerialNumber = kitSerialField.value;
  var ctm = ctmsWithKitsData.find(function(item) {
    return item.kit_serial_number === selectedSerialNumber;
  });

  if (ctm) {
    document.getElementById('lotField').value = ctm.lot_number || '';
    document.getElementById('quantityField').value = ctm.quantity || '';
    document.getElementById('expirationDateField').value = ctm.expiration_date || '';
  }
}


