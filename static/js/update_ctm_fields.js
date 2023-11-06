// update_ctm_fields.js
// No need to parse from the DOM, assuming ctmsWithKitsData is defined globally in your Django template

// Function to update kit serial numbers based on the selected CTM name
function updateKitSerialNumbers(selectedCtmName) {
  const kitSerialField = document.getElementById('kitSerialField');
  kitSerialField.innerHTML = ''; // Clear previous options

  // Find the selected CTM and its kits
  const ctmKits = ctmsWithKitsData.find(ctm => ctm.ctm_name === selectedCtmName);

  if (ctmKits && ctmKits.kit_serial_numbers) {
    // Append options related to the selected CTM
    ctmKits.kit_serial_numbers.forEach(serialNumber => {
      const option = new Option(serialNumber, serialNumber);
      kitSerialField.add(option);
    });
  }
}

// Event handling after DOM content is fully loaded
document.addEventListener('DOMContentLoaded', function() {
  const ctmField = document.getElementById('ctmField');

  // Update kit serial numbers when a CTM name is selected
  ctmField.addEventListener('change', function() {
    updateKitSerialNumbers(this.value);
  });

  // Initial population of kit serial numbers if there's a preselected CTM
  if(ctmField.selectedIndex >= 0) {
    updateKitSerialNumbers(ctmField.options[ctmField.selectedIndex].value);
  }
});





