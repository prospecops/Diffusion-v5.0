// update_ctm_fields.js

// Event handling after DOM content is fully loaded
document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM fully loaded and parsed');

  const ctmField = document.getElementById('ctmField');
  console.log('ctmField element:', ctmField);

  const updateKitSerialNumbers = (selectedCtmName) => {
    console.log('updateKitSerialNumbers called with:', selectedCtmName);
    const kitSerialField = document.getElementById('kitSerialField');
    kitSerialField.innerHTML = ''; // Clear previous options

    // Fetch the ctmsWithKitsData from the script tag
    const ctmsWithKitsData = JSON.parse(document.getElementById('ctmsWithKitsData').textContent);
    console.log('Parsed ctmsWithKitsData:', ctmsWithKitsData);

    // Attempt to find the selected CTM and its kits
    const ctmKits = ctmsWithKitsData.find(ctm => ctm.ctm_name === selectedCtmName);
    console.log('Selected CTM Kits:', ctmKits);

    if (ctmKits && ctmKits.kit_serial_numbers) {
      // Append options related to the selected CTM
      ctmKits.kit_serial_numbers.forEach(serialNumber => {
        const option = new Option(serialNumber, serialNumber);
        kitSerialField.add(option);
      });
      console.log('Kit serial numbers updated for:', selectedCtmName);
    } else {
      console.log('No kits found for:', selectedCtmName);
    }
  };

  // Update kit serial numbers when a CTM name is selected
  ctmField.addEventListener('change', function() {
    console.log('CTM field changed:', this.value);
    updateKitSerialNumbers(this.value);
  });

  // Initial population of kit serial numbers if there's a preselected CTM
  if (ctmField.selectedIndex >= 0) {
    console.log('Initial CTM selected:', ctmField.options[ctmField.selectedIndex].value);
    updateKitSerialNumbers(ctmField.options[ctmField.selectedIndex].value);
  } else {
    console.log('No initial CTM selected');
  }
});

console.log('update_ctm_fields.js script executed');


