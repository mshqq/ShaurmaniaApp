document.addEventListener('order:submit', function (event) {
  var order = event.detail;

  var submitButton = document.querySelector('#orderForm button[type="submit"]');
  if (submitButton) {
    submitButton.disabled = true;
    submitButton.textContent = 'Отправка...';
  }

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
      redirect(data.redirect_url);
    })
    .catch(function (error) {
      console.error('Не удалось отправить заказ:', error);
      showOrderError();
    })
    .finally(function () {
      if (submitButton) {
        submitButton.disabled = false;
        submitButton.textContent = 'Оформить заказ';
      }
    });
});

function redirect(redirect_url) {
  window.location.href = redirect_url;
}

function showOrderError() {
  alert('Не удалось оформить заказ. Попробуйте ещё раз.');
}
