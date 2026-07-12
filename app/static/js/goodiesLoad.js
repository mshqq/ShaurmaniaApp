import initCart from './cart.js';

function initGoodies() {
  const menuParent = document.querySelector('.menu__goodies');
  fetch('/api/products')
    .then(response => {
      return response.json();
    })
    .then(goodies => {
      let menu = '';
      goodies.forEach(product => {
        const path = STATIC_URL + product.image_path;
        menu += `
            <div class="menu__card" data-category="${product.category}">
              <img src="${path}" alt="${product.name}" class="menu__card-img" />
              <div class="menu__card-info">
                <p class="menu__card-title">${product.name}</p>
                  <p class="menu__card-composition">${product.composition}</p>
                <div class="menu__card-controls">
                  <p class="menu__card-price">${product.price} ₽</p>
                  <button class="menu__card-button" data-product-id="${product.id}">В корзину</button>
                </div>
              </div>
            </div>`;
      });
      menuParent.innerHTML = menu;
      initCart();
    });
}

export default initGoodies;
