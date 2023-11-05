// modal-handler.js
document.addEventListener('DOMContentLoaded', () => {
  // General modal close functionality
  const closeButtons = document.querySelectorAll('.btn-close[data-bs-dismiss="modal"]');

  closeButtons.forEach(button => {
    button.addEventListener('click', () => {
      let modal = bootstrap.Modal.getInstance(button.closest('.modal'));
      modal.hide();
    });
  });

  // Optional: if you're using jQuery and Bootstrap's JavaScript
  $('.modal').on('hidden.bs.modal', function () {
    // Perform any action on modal close if necessary
  });
});
document.addEventListener('DOMContentLoaded', (event) => {
  // Function to remove the modal backdrop manually.
  function removeBackdrop() {
    let backdrop = document.querySelector('.modal-backdrop');
    if (backdrop) {
      backdrop.parentNode.removeChild(backdrop);
    }
    // Reactivate scrolling on the body.
    document.body.classList.remove('modal-open');
  }

  // Attach close event listener to all close buttons.
  document.querySelectorAll('.btn-close[data-bs-dismiss="modal"]').forEach(closeButton => {
    closeButton.addEventListener('click', function () {
      // Bootstrap's data-bs-dismiss attribute should take care of hiding the modal
      // The manual backdrop removal is a fallback in case it doesn't get removed
      removeBackdrop();
    });
  });

  // Additionally, if you want to handle the modal hidden event globally, add this listener:
  $('#yourModalId').on('hidden.bs.modal', function (e) {
    removeBackdrop();
  });

  // Replace 'yourModalId' with the actual ID of your modal if you want to handle this event for a specific modal,
  // or use the `.modal` selector to apply this to all modals.
});

