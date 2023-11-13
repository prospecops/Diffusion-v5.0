// handle_shipment_status.js

document.addEventListener('DOMContentLoaded', function() {
  const shipmentStatusModal = document.getElementById('shipmentStatusModal');
  const shipmentStatusField = document.getElementById('shipmentStatusField');
  const saveShipmentStatusButton = document.getElementById('saveShipmentStatusButton');

  const resetShipmentStatus = () => {
    // Enable all options except the first placeholder option
    Array.from(shipmentStatusField.options).forEach((option, index) => {
      option.disabled = index === 0;
    });

    // Reset to the default option
    shipmentStatusField.value = "";
    saveShipmentStatusButton.disabled = true;
  };

  shipmentStatusField.addEventListener('change', function() {
    if (this.value) {
      // Disable the placeholder option after a valid selection
      this.options[0].disabled = true;
      saveShipmentStatusButton.disabled = false;
    }
  });

  shipmentStatusModal.addEventListener('show.bs.modal', resetShipmentStatus);
});
