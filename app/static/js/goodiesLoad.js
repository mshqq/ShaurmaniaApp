import initCart from './cart.js';

function initGoodies() {
  const menuParent = document.querySelector('.menu__goodies');

  fetch('/api/products')
    .then(response => response.json())
    .then(goodies => {
      menuParent.innerHTML = '';
      goodies.forEach(product => {
        const path = STATIC_URL + product.image_path;
        const card = document.createElement('div');

        card.classList.add('menu__card');
        card.setAttribute('data-category', product.category);

        card.innerHTML = `
              <img src="" alt="" class="menu__card-img" />
              <div class="menu__card-info">
                <p class="menu__card-title"></p>
                <p class="menu__card-composition"></p>
                <div class="menu__card-controls">
                  <p class="menu__card-price"></p>
                  <button class="menu__card-button">В корзину</button>
                </div>
              </div>
        `;

        card.querySelector('.menu__card-img').src = path;
        card.querySelector('.menu__card-img').alt = product.name;
        card.querySelector('.menu__card-title').textContent = product.name;
        card.querySelector('.menu__card-composition').textContent = product.composition;
        card.querySelector('.menu__card-price').textContent = `${product.price} ₽`;

        const button = card.querySelector('.menu__card-button');
        button.setAttribute('data-product-id', product.id);

        menuParent.appendChild(card);
      });
      initCart();
    });
}

export default initGoodies;
