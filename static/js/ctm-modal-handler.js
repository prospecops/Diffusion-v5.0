// ctm-modal-opener.js
document.addEventListener('DOMContentLoaded', () => {
  const individualCTMButton = document.getElementById('addIndividualCTMButton');
  const bulkCTMButton = document.getElementById('bulkCTMButton');
  const drugField = document.getElementById('drugField'); // Assuming this is the correct ID
  const kitSerialField = document.getElementById('kitSerialField'); // Assuming this is the correct ID

  // Function to update the Kit # / Serial # list
  function updateKitSerialNumbers(drugId) {
    // Clear previous options
    kitSerialField.innerHTML = '';

    // Fetch the new list of kits based on the selected drug
    fetch(`/get-kit-serials/?drug_id=${drugId}`)
      .then(response => response.json())
      .then(data => {
        // Populate the kitSerialField with new options
        data.kit_serials.forEach(kit => {
          const option = new Option(kit.text, kit.id);
          kitSerialField.add(option);
        });
      }).catch(error => {
        console.error('Error fetching kit serial numbers:', error);
      });
  }

  if (individualCTMButton) {
    individualCTMButton.addEventListener('click', () => {
      new bootstrap.Modal(document.getElementById('individualCTMModal')).show();
    });
  }

  if (bulkCTMButton) {
    bulkCTMButton.addEventListener('click', () => {
      new bootstrap.Modal(document.getElementById('bulkCTMModal')).show();
    });
  }

  if (drugField) {
    drugField.addEventListener('change', function(e) {
      updateKitSerialNumbers(e.target.value);
    });
  }
});

