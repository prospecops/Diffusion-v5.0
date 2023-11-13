// handle_depot_selection.js

document.addEventListener('DOMContentLoaded', function() {
  const selectDepotModal = document.getElementById('selectDepotModal');
  const depotSelectionField = document.getElementById('depotSelectionField');
  const saveDepotSelectionButton = document.getElementById('saveDepotSelectionButton');
  const selectDepotButton = document.getElementById('selectDepotButton');
  const depotDetailsTableBody = document.querySelector('.depot-details-table tbody');
  let currentSelectedDepot = null;

  // Parse depot data from embedded JSON.
  const depots = JSON.parse(document.getElementById('depotsData').textContent);

  // Function to update the depot details in the table.
  const updateDepotDetails = (selectedDepotName) => {
    // Find depot details based on the selected name.
    const selectedDepot = depots.find(depot => depot.name === selectedDepotName);

    // Clear existing rows in the table body.
    depotDetailsTableBody.innerHTML = '';

    if (selectedDepot) {
      // Insert a new row with depot details.
      const row = depotDetailsTableBody.insertRow();
      row.insertCell(0).textContent = selectedDepot.name;
      row.insertCell(1).textContent = selectedDepot.address;
    }
  };

  // Function to update the dropdown options.
  const updateDropdownOptions = () => {
    Array.from(depotSelectionField.options).forEach(option => {
      // Disable the currently selected depot in the dropdown.
      option.disabled = option.value === currentSelectedDepot;
    });
  };

  // Event listener for depot selection changes.
  depotSelectionField.addEventListener('change', function() {
    // Enable the save button only if a different depot is selected.
    saveDepotSelectionButton.disabled = !this.value || this.value === currentSelectedDepot;
  });

  // Event listener for the save button click.
  saveDepotSelectionButton.addEventListener('click', function() {
    // Update details and set the current selection.
    currentSelectedDepot = depotSelectionField.value;
    updateDepotDetails(currentSelectedDepot);

    // Change button text to indicate depot change.
    selectDepotButton.textContent = 'Change Depot';

    // Hide the modal.
    $('#selectDepotModal').modal('hide');
  });

  // Event listener for when the modal is shown.
  selectDepotModal.addEventListener('show.bs.modal', function() {
    resetDepotSelection();
    updateDropdownOptions();
  });

  // Function to reset the selection in the modal.
  const resetDepotSelection = () => {
    depotSelectionField.value = "";
    saveDepotSelectionButton.disabled = true;
  };
});

