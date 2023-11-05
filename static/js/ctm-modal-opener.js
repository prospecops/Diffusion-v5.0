// ctm-modal-opener.js
document.addEventListener('DOMContentLoaded', () => {
  const individualCTMButton = document.getElementById('addIndividualCTMButton');
  const bulkCTMButton = document.getElementById('bulkCTMButton');

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
});
