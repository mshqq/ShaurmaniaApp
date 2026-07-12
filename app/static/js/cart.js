function initCart() {
  const counter = document.querySelector('.nav__btn');
  const cards = document.querySelectorAll('.menu__card');
  const modal = document.querySelector('.modal');
  const openCart = document.getElementById('openModal');
  const overlay = document.querySelector('.modal-overlay');
  const closeButton = document.querySelector('.modal-close');
  const cancelButton = document.querySelector('.modal-cancel');
  const composition = document.querySelector('.composition');
  const total = document.querySelector('.cart-total');
  const orderForm = document.getElementById('orderForm');
  const pickupField = document.getElementById('pickupField');
  const deliveryAddressField = document.getElementById('deliveryAddressField');
  const pickupAddress = document.getElementById('pickupAddress');
  const deliveryAddress = document.getElementById('deliveryAddress');

  if (!counter || cards.length === 0 || !modal || !openCart || !orderForm) {
    return;
  }

  const cart = [];

  function formatPrice(value) {
    return `${value.toLocaleString('ru-RU')} ₽`;
  }

  function getProductDetails(productId) {
    const control = document.querySelector(`[data-product-id="${productId}"]`);
    if (!control) {
      return null;
    }

    const card = control.closest('.menu__card');
    if (!card) {
      return null;
    }

    const titleEl = card.querySelector('.menu__card-title');
    const imgEl = card.querySelector('.menu__card-img');
    const priceEl = card.querySelector('.menu__card-price');

    const priceText = priceEl.textContent;
    const priceNumber = Number(priceText.replace(/[^\d.,]/g, '').replace(',', '.'));

    return {
      id: productId,
      name: titleEl.textContent.trim(),
      image: imgEl.src,
      price: priceNumber
    };
  }

  function getCartItem(productId) {
    return cart.find(item => item.id === productId);
  }

  function renderCounter() {
    const count = cart.reduce((sum, item) => sum + item.quantity, 0);
    counter.dataset.count = count;
    counter.classList.toggle('empty', count === 0);
  }

  function renderOpenCartButton() {
    const isEmpty = cart.length === 0;
    openCart.disabled = isEmpty;
    openCart.classList.toggle('disabled', isEmpty);
  }

  function renderCardControls(productId) {
    const button = document.querySelector(`.menu__card-button[data-product-id="${productId}"]`);
    const extraButton = document.querySelector(
      `.menu__card-extra button[data-product-id="${productId}"]`
    );

    let controls = null;
    if (button) {
      controls = button.parentElement;
    } else if (extraButton) {
      controls = extraButton.closest('.menu__card-controls');
    }
    if (!controls) {
      return;
    }

    const item = getCartItem(productId);
    const existingExtra = controls.querySelector('.menu__card-extra');

    if (!item) {
      if (existingExtra) {
        existingExtra.remove();
      }
      if (!button) {
        const addButton = document.createElement('button');
        addButton.className = 'menu__card-button';
        addButton.dataset.productId = productId;
        addButton.textContent = 'В корзину';
        controls.append(addButton);
      }
      return;
    }

    if (button) {
      button.remove();
    }
    let extra = existingExtra;
    if (!extra) {
      extra = document.createElement('div');
      extra.className = 'menu__card-extra';
    }
    extra.innerHTML = `
      <button data-product-id="${productId}" data-type="minus" type="button"><span>➖</span></button>
      <p data-product-id="${productId}">${item.quantity}</p>
      <button data-product-id="${productId}" data-type="plus" type="button"><span>➕</span></button>
    `;
    if (!existingExtra) {
      controls.append(extra);
    }
  }

  function renderModal() {
    if (cart.length === 0) {
      composition.innerHTML = '<p class="cart-empty">Корзина пока пуста.</p>';
      total.textContent = formatPrice(0);
      return;
    }

    composition.innerHTML = cart
      .map(
        item => `
          <article class="cart__item">
            <img class="cart__item-img" src="${item.image}" alt="" />
            <div class="cart__item-info">
              <p class="cart__item-name">${item.name}</p>
              <p class="cart__item-price">${formatPrice(item.price)}</p>
            </div>
            <div class="cart__item-controls">
              <button type="button" data-cart-action="minus" data-product-id="${item.id}">-</button>
              <p>${item.quantity}</p>
              <button type="button" data-cart-action="plus" data-product-id="${item.id}">+</button>
            </div>
          </article>
        `
      )
      .join('');

    total.textContent = formatPrice(
      cart.reduce((sum, item) => sum + item.price * item.quantity, 0)
    );
  }

  function syncCart(productId) {
    renderCardControls(productId);
    renderCounter();
    renderOpenCartButton();
    if (modal.style.display === 'grid') {
      renderModal();
    }
  }

  function addToCart(productId) {
    const existingProduct = getCartItem(productId);
    if (existingProduct) {
      existingProduct.quantity += 1;
    } else {
      const product = getProductDetails(productId);
      if (!product) {
        return;
      }
      cart.push({ ...product, quantity: 1 });
    }
    syncCart(productId);
  }

  function removeFromCart(productId) {
    const item = getCartItem(productId);
    if (!item) {
      return;
    }
    item.quantity -= 1;
    if (item.quantity === 0) {
      cart.splice(cart.indexOf(item), 1);
    }
    syncCart(productId);
  }

  function populatePickupAddresses() {
    fetch('/api/locations', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`Ошибка сервера: ${response.status}`);
        }
        return response.json();
      })
      .then(addresses => {
        console.log(addresses);
        pickupAddress.innerHTML = '<option value="" disabled>Выберите адрес</option>';
        addresses.forEach(address => {
          const option = new Option(address.address, address.id);
          pickupAddress.add(option);
        });
        pickupAddress.selectedIndex = 0;
      });
  }

  function toggleDeliveryFields() {
    const isDelivery = orderForm.elements.fulfillment.value === 'Доставка';
    pickupField.hidden = isDelivery;
    deliveryAddressField.hidden = !isDelivery;
    pickupAddress.required = !isDelivery;
    deliveryAddress.required = isDelivery;
  }

  function openModal() {
    renderModal();
    modal.style.display = 'grid';
    document.body.classList.add('modal-open');
    requestAnimationFrame(() => modal.classList.add('active'));
  }

  function closeModal() {
    modal.classList.remove('active');
    document.body.classList.remove('modal-open');
    setTimeout(() => {
      modal.style.display = 'none';
    }, 300);
  }

  function showEmptyCartWarning() {
    if (!cartEmptyWarning) {
      return;
    }
    cartEmptyWarning.classList.remove('cart-empty-warning--visible');

    void cartEmptyWarning.offsetWidth;

    cartEmptyWarning.classList.add('cart-empty-warning--visible');

    setTimeout(function () {
      cartEmptyWarning.classList.remove('cart-empty-warning--visible');
    }, 1200);
  }

  document.addEventListener('click', event => {
    const addButton = event.target.closest('.menu__card-button');
    if (addButton) {
      addToCart(addButton.dataset.productId);
      return;
    }
    const extraButton = event.target.closest('.menu__card-extra button');
    if (extraButton) {
      extraButton.dataset.type === 'plus'
        ? addToCart(extraButton.dataset.productId)
        : removeFromCart(extraButton.dataset.productId);
    }
  });

  modal.addEventListener('click', event => {
    const control = event.target.closest('[data-cart-action]');
    if (!control) {
      return;
    }
    control.dataset.cartAction === 'plus'
      ? addToCart(control.dataset.productId)
      : removeFromCart(control.dataset.productId);
  });

  openCart.addEventListener('click', openModal);
  closeButton.addEventListener('click', closeModal);
  cancelButton.addEventListener('click', closeModal);
  overlay.addEventListener('click', closeModal);

  orderForm.addEventListener('change', event => {
    if (event.target.name === 'fulfillment') {
      toggleDeliveryFields();
    }
  });

  orderForm.addEventListener('submit', event => {
    event.preventDefault();
    if (cart.length === 0) {
      showEmptyCartWarning();
      return;
    }
    if (!orderForm.reportValidity()) {
      return;
    }

    const formData = new FormData(orderForm);
    const delivery_type = formData.get('fulfillment');
    let location_id;
    let delivery_address;

    if (delivery_type === 'Самовывоз') {
      delivery_address = null;
      location_id = formData.get('pickupAddress');
    }

    if (delivery_type === 'Доставка') {
      delivery_address = formData.get('deliveryAddress');
      location_id = null;
    }

    const order = {
      customer_name: formData.get('customerName'),
      customer_phone: formData.get('customerPhone'),
      delivery_type,
      location_id,
      delivery_address,
      cart: cart.map(({ id, name, price, quantity }) => ({ id, name, price, quantity })),
      total_price: cart.reduce((sum, item) => sum + item.price * item.quantity, 0)
    };

    document.dispatchEvent(new CustomEvent('order:submit', { detail: order }));
  });

  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && modal.style.display === 'grid') {
      closeModal();
    }
  });

  populatePickupAddresses();
  toggleDeliveryFields();
  renderCounter();
  renderOpenCartButton();
}

export default initCart;
