function initSlider() {
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
}

export default initSlider;
