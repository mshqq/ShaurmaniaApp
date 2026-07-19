function initSlider() {
  let current = 0;
  const slides = document.querySelectorAll('.slide');
  const bubbles = document.querySelectorAll('.slider__bubble');
  const sliderContainer = document.querySelector('.slider__carousel');

  if (slides.length === 0) return;

  function goTo(index) {
    current = (index + slides.length) % slides.length;

    slides.forEach(s => s.classList.remove('active'));
    slides[current].classList.add('active');

    bubbles.forEach(b => b.classList.remove('active'));
    bubbles[current].classList.add('active');
  }

  let autoplay;

  function startAutoplay() {
    clearInterval(autoplay);
    autoplay = setInterval(() => {
      goTo(current + 1);
    }, 3000);
  }

  function stopAutoplay() {
    clearInterval(autoplay);
  }

  startAutoplay();

  document.querySelector('.slider__next').addEventListener('click', () => {
    goTo(current + 1);
    startAutoplay();
  });

  document.querySelector('.slider__prev').addEventListener('click', () => {
    goTo(current - 1);
    startAutoplay();
  });

  if (sliderContainer) {
    sliderContainer.addEventListener('mouseenter', stopAutoplay);
    sliderContainer.addEventListener('mouseleave', startAutoplay);
  }
}

export default initSlider;
