function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

function changeCategory(button) {
  document.querySelector('.menu__category.active').classList.remove('active');
  button.classList.add('active');

  let category = button.dataset.category;
  document.querySelectorAll('.menu__card').forEach(card => {
    card.style.display = category === 'all' || card.dataset.category === category ? '' : 'none';
  });
}

document.querySelectorAll('.menu__category').forEach(button => {
  button.addEventListener('click', () => {
    changeCategory(button);
  });
});

const menuParent = document.querySelector('.menu__goodies');

fetch('/api/products')
  .then(response => {
    return response.json();
  })
  .then(goodies => {
    let menu = '';
    goodies.forEach(product => {
      path = STATIC_URL + product.image_path;
      menu += `
            <div class="menu__card" data-category="${product.category}">
              <img src="${path}" alt="${product.name}" class="menu__card-img" />
              <div class="menu__card-info">
                <p class="menu__card-title">${product.name}</p>
                  <p class="menu__card-description">${product.description}</p>
                  <p class="menu__card-composition">${product.composition}</p>
                <div class="menu__card-controls">
                  <p class="menu__card-price">${product.price} ₽</p>
                  <button class="menu__card-button">Добавить в корзину</button>
                </div>
              </div>
            </div>`;
    });
    menuParent.innerHTML = menu;
  });

setInterval(() => {
  window.location.reload();
}, 15000);

let current = 0;
let slides = document.querySelectorAll('.slide');
let bubbles = document.querySelectorAll('.slider__bubble');

function goTo(index) {
  current = (index + slides.length) % slides.length;

  slides.forEach(s => s.classList.remove('active'));
  slides[current].classList.add('active');

  bubbles.forEach(b => b.classList.remove('active'));
  bubbles[current].classList.add('active');
}

document.querySelector('.slider__next').addEventListener('click', () => {
  goTo(current + 1);
});

document.querySelector('.slider__prev').addEventListener('click', () => {
  goTo(current - 1);
});

const autoplay = setInterval(() => {
  goTo(current + 1);
}, 3000);

const cursor = document.createElement('div');
cursor.classList.add('cursor');
document.body.appendChild(cursor);

document.addEventListener('mousemove', e => {
  cursor.style.left = e.clientX + 'px';
  cursor.style.top = e.clientY + 'px';
});

let nameInput = document.querySelector('#name');
let emailInput = document.querySelector('#email');
let form = document.querySelector('.form-group');

document.querySelector('.form-button').addEventListener('click', e => {
  e.preventDefault();
  if (!validate()) return;

  const nameValue = nameInput.value.trim();
  const emailValue = emailInput.value.trim();

  fetch('/api/subscribe', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
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

let lastKey = null;

function gazan() {
  const audio = new Audio('/static/music/music.mp3');
  audio.play();
  setTimeout(() => {
    audio.pause();
    document.querySelector('img.gazan').style.display = 'none';
  }, 5000);

  gazanBtn = document.querySelector('.nav__container');
  gazanBtn.innerHTML += '<img class="gazan" src="/static/img/features/gazan.png"></img>';

  lastKey = null;
}

document.addEventListener('keydown', e => {
  if (lastKey === '6' && e.key === '7') {
    gazan();
  } else {
    lastKey = e.key;
  }
});
