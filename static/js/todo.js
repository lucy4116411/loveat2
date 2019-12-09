/* global FetchData, $ */
/* eslint no-underscore-dangle: ["error", { "allow": ["_id"] }] */

const TODO_API = {
  todo: '/api/order/todo',
  update: '/api/order/update',
};

let TODO = [];
let ID_ORDER = -1;/* -1 is decreasing order, 1 is increasing order */
let TAKEN_ORDER = -1;/* -1 is decreasing order, 1 is increasing order */

const channel = new BroadcastChannel('order-todo');
channel.onmessage = (payload) => {
  console.log('hello');
  console.log(payload.data);
};

/*
messaging.onMessage((payload) => {
  console.log(payload);
  // start show notification

  const notificationTitle = payload.data.title;
  const notificationOptions = {
    body: payload.data.content,
    icon: '/favicon.ico',
  };
  const notification = new Notification(notificationTitle, notificationOptions);
  // deal with click event
  notification.onclick = () => {
    window.open(payload.data.url);
  };

});
*/


/* ----order function---- */
function orderFunction(mode, order) {
  let switching = true;
  while (switching) {
    switching = false;
    const tableRows = document.getElementById('order_table').rows;
    let index;
    let shouldSwitch;
    for (index = 1; index < tableRows.length - 1; index += 1) {
      shouldSwitch = false;
      let x; let xNext;
      if (mode === 1) { // sort by orderId
        x = parseInt(tableRows[index].getElementsByTagName('TD')[0].innerHTML, 10);
        xNext = parseInt(tableRows[index + 1].getElementsByTagName('TD')[0].innerHTML, 10);
      } else if (mode === 2) { // sort by takenAt
        x = new Date(tableRows[index].getElementsByTagName('TD')[1].innerHTML.replace('<br>', ' '));
        xNext = new Date(tableRows[index + 1].getElementsByTagName('TD')[1].innerHTML.replace('<br>', ' '));
      }

      if (order === -1) {
        if (x < xNext) {
          shouldSwitch = true;
          break;
        }
      } else if (order === 1) {
        if (x > xNext) {
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      tableRows[index].parentNode.insertBefore(tableRows[index + 1], tableRows[index]);
      switching = true;
    }
  }
}
/* ----sort by orderID---- */
function sortByOrderID() {
  orderFunction(1, ID_ORDER);
  ID_ORDER = (ID_ORDER === -1) ? 1 : -1;
}

/* ----sort by takenAt---- */
function sortByTakenAt() {
  orderFunction(2, TAKEN_ORDER);
  TAKEN_ORDER = (TAKEN_ORDER === -1) ? 1 : -1;
}

/* ----order finish deal---- */
async function orderFinish(event) {
  const tarId = event.target.id.replace('_finish', '');

  document.getElementById(`${tarId}_finish`).disabled = true;
  const result = await FetchData.post(TODO_API.update, {
    id: tarId,
    state: 'finish',
  });

  if (result.status === 403) { // permision denyied
    document.getElementById(`${tarId}_finish`).disabled = false;
    console.log('該帳號沒有此權限。');
  } else if (result.status === 404) { // order not found
    document.getElementById('orderHintContent').innerHTML = '該訂單不存在，更新失敗。';
    document.getElementById(`${tarId}_finish`).disabled = false;
    $('#orderHintModal').modal('show');
  } else { // successful
    // 推播
    document.getElementById(`${tarId}_order`).classList.add('finish');
  }
}

/* ----order end deal---- */
async function orderEnd(event) {
  const tarId = event.target.id.replace('_end', '');
  const tarOrder = document.getElementById(`${tarId}_order`);

  const result = await FetchData.post(TODO_API.update, {
    id: tarId,
    state: 'end',
  });

  if (result.status === 403) { // permision denyied
    console.log('該帳號沒有此權限。');
  } else if (result.status === 404) { // order not found
    document.getElementById('orderHintContent').innerHTML = '該訂單不存在，更新失敗。';
    $('#orderHintModal').modal('show');
  } else { // successful
    tarOrder.parentNode.removeChild(tarOrder);
  }
}

async function init() {
  const res = await FetchData.get(TODO_API.todo);
  TODO = await res.json();

  /* ----listener for orderID---- */
  document.getElementById('orderID').addEventListener('click', sortByOrderID);
  /* ----listener for takenAt---- */
  document.getElementById('myTakenAt').addEventListener('click', sortByTakenAt);
  /* ----listener for order finish ----*/
  TODO.forEach((element) => {
    document.getElementById(`${element._id}_finish`).addEventListener('click', orderFinish);
  });
  /* ----listener for order end ----*/
  TODO.forEach((element) => {
    document.getElementById(`${element._id}_end`).addEventListener('click', orderEnd);
  });
}

window.addEventListener('load', init);
