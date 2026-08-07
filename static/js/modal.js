document.addEventListener('DOMContentLoaded', () => {

  function openModal($el) {
    $el.classList.add('is-active');

    // Si es un modal de mensajes, cerrarlo automáticamente
    if ($el.dataset.autoClose === "true") {
      setTimeout(() => {
        closeModal($el);
      }, 3000);
    }
  }

  function closeModal($el) {
    $el.classList.remove('is-active');
  }

  function closeAllModals() {
    document.querySelectorAll('.modal').forEach(($modal) => {
      closeModal($modal);
    });
  }

  document.querySelectorAll('.js-modal-trigger').forEach(($trigger) => {
    const modal = $trigger.dataset.target;
    const $target = document.getElementById(modal);

    $trigger.addEventListener('click', () => {
      openModal($target);
    });
  });

  document.querySelectorAll(
    '.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button'
  ).forEach(($close) => {
    const $target = $close.closest('.modal');

    $close.addEventListener('click', () => {
      closeModal($target);
    });
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      closeAllModals();
    }
  });

  // Abrir automáticamente los modales que ya tengan is-active
  document.querySelectorAll('.modal.is-active').forEach(($modal) => {
    if ($modal.dataset.autoClose === "true") {
      setTimeout(() => {
        closeModal($modal);
      }, 3000);
    }
  });

});