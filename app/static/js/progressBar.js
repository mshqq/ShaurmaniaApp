const statuses = {
  accepted: [10, 0],
  cooking: [37, 1],
  pending: [62, 2],
  done: [100, 3]
};

const orderURL = location.pathname.split('/').pop();
const targetURL = `/api/order/status/${orderURL}`;

function setDone(icons, idx) {
  let index = 0;
  icons.forEach(icon => {
    if (index < idx) {
      icon.classList.add('done');
      icon.classList.remove('active');
    }
    index += 1;
  });
}

function setActive(icons, idx) {
  icons[idx].classList.add('active');
}

function changeStatus(status) {
  const progressBar = document.querySelector('.status-track-fill');
  progressBar.style.width = `${statuses[status][0]}%`;

  const icons = document.querySelectorAll('.status-step');
  setDone(icons, statuses[status][1]);
  setActive(icons, statuses[status][1]);

  const etaTime = document.querySelector('#etaTime');
  const deliveryType = document.querySelector('.status-track').dataset.deliveryType;

  switch (status) {
    case 'pending':
      etaTime.textContent = deliveryType === 'Самовывоз' ? 'Готов к выдаче' : 'В пути';
      break;
    case 'done':
      etaTime.textContent = 'Завершен';
      etaTime.classList.add('text-success');
      break;
  }
}

async function updateStatus() {
  let status;

  do {
    const response = await fetch(targetURL);
    status = await response.json();

    changeStatus(status.status);

    if (status.status !== 'done') {
      await new Promise(resolve => setTimeout(resolve, 5000));
    }
  } while (status.status !== 'done');
}

updateStatus();
