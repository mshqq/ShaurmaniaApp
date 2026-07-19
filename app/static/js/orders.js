const showLoader = () => {
  const cancelButton = document.querySelector('.modal-cancel');
  if (cancelButton) {
    cancelButton.disabled = true;
  }

  const submitButton = document.querySelector('.modal-submit');
  if (submitButton) {
    submitButton.disabled = true;
    submitButton.textContent = `Заказ создаётся...`;
  }

  const loadingText = document.createElement('div');
  loadingText.className = 'loading';

  const modalControls = document.querySelector('.modal-controls');
  const parentDiv = modalControls.parentNode;
  if (!parentDiv.querySelector('.loading')) {
    parentDiv.insertBefore(loadingText, modalControls);
  }
};

const hideLoader = () => {
  const cancelButton = document.querySelector('.modal-cancel');
  if (cancelButton) {
    cancelButton.disabled = false;
  }

  const submitButton = document.querySelector('.modal-submit');
  if (submitButton) {
    submitButton.disabled = false;
    submitButton.textContent = `Оформить заказ`;
  }

  const loadingText = document.querySelector('.loading');
  if (loadingText) {
    loadingText.remove();
  }
};

document.addEventListener('order:submit', function (event) {
  showLoader();

  const order = event.detail;
  const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

  fetch('/api/order', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
    body: JSON.stringify(order)
  })
    .then(function (response) {
      if (!response.ok) {
        throw new Error('Ошибка сервера: ' + response.status);
      }
      return response.json();
    })
    .then(function (data) {
      return new Promise(function (resolve) {
        setTimeout(resolve, 1000);
      }).then(function () {
        redirect(data.redirect_url);
      });
    })
    .catch(function (error) {
      console.error('Не удалось отправить заказ:', error);
      hideLoader();
      showOrderError();
    });
});

function redirect(redirect_url) {
  window.location.href = redirect_url;
}

function showOrderError() {
  alert('Не удалось оформить заказ. Попробуйте ещё раз.');
}
