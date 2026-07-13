const statuses = {
  accepted: [10, 0],
  cooking: [37, 1],
  pending: [62, 2],
  done: [100, 3]
};

let orderURL = location.pathname.slice(7);
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
  progressBar = document.querySelector('.status-track-fill');
  progressBar.style.width = `${statuses[status][0]}%`;
  console.log(`Поменяли ширину на ${statuses[status][0]}`);
  console.log(`Готовы статусы до ${statuses[status][1]}`);

  icons = document.querySelectorAll('.status-step');
  setDone(icons, statuses[status][1]);
  setActive(icons, statuses[status][1]);
  console.log(icons);
}

async function updateStatus() {
  let status;

  do {
    const response = await fetch(targetURL);
    status = await response.json();

    console.log(status);
    changeStatus(status.status);

    if (status.status !== 'done') {
      await new Promise(resolve => setTimeout(resolve, 5000));
    }
  } while (status.status !== 'done');
}

updateStatus();

// do {
//   fetch(targetURL)
//     .then(response => response.json())
//     .then(data => console.log(data));
// } while (data.status !== 'done');
