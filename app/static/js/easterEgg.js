function initEasterEgg() {
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
}

export default initEasterEgg;
