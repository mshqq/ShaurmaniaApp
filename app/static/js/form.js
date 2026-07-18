function initForm() {
  let nameInput = document.querySelector('#name');
  let emailInput = document.querySelector('#email');
  let form = document.querySelector('.form-group');

  document.querySelector('.form-button').addEventListener('click', e => {
    e.preventDefault();
    if (!validate()) return;

    const nameValue = nameInput.value.trim();
    const emailValue = emailInput.value.trim();

    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    fetch('/api/subscribe', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({ name: nameValue, email: emailValue })
    })
      .then(response => {
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        return response.json();
      })
      .then(() => {
        form.innerHTML =
          '<p class="form-success">Вы подписались! Ждите горячих акций на почте 🔥</p>';
      })
      .catch(error => {
        console.error('Fetch error:', error);
      });
  });

  function validate() {
    const nameValue = nameInput.value.trim();
    const emailValue = emailInput.value.trim();

    if (nameValue === '') {
      showError(nameInput, 'Поле обязательно');
      return false;
    }

    if (emailValue === '' || !emailValue.includes('@')) {
      showError(emailInput, 'Введите корректный Email');
      return false;
    }

    clearError(nameInput);
    clearError(emailInput);
    return true;
  }

  function showError(input, message) {
    input.classList.add('error');

    const error = input.previousElementSibling; // элемент после input
    if (error) error.textContent = message;
  }

  function clearError(input) {
    input.classList.remove('error');

    const error = input.previousElementSibling;
    if (error) error.textContent = '';
  }
}

export default initForm;
