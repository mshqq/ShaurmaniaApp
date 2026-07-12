function changeCategory(button) {
  document.querySelector('.menu__category.active').classList.remove('active');
  button.classList.add('active');

  let category = button.dataset.category;
  document.querySelectorAll('.menu__card').forEach(card => {
    card.style.display = category === 'all' || card.dataset.category === category ? '' : 'none';
  });
}

function initCategoryFilter() {
  document.querySelectorAll('.menu__category').forEach(button => {
    button.addEventListener('click', () => {
      changeCategory(button);
    });
  });

  const activeButton = document.querySelector('menu__category.active');
  if (activeButton) {
    changeCategory(activeButton);
  }
}

export default initCategoryFilter;
