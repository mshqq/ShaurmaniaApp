function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

function initTopBtn() {
  const button = document.querySelector('#topBtn');
  if (!button) return;

  button.addEventListener('click', () => {
    topFunction();
  });
}

function initCursor() {
  const cursor = document.createElement('div');
  cursor.classList.add('cursor');
  document.body.appendChild(cursor);

  document.addEventListener('mousemove', e => {
    cursor.style.left = e.clientX + 'px';
    cursor.style.top = e.clientY + 'px';
  });
}
initTopBtn();
initCursor();
