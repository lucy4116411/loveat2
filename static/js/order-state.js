/* global messaging */

const stateTable = {
  doing: '製作中',
  unknown: '未回應',
  finish: '已完成',
  cancel: '拒絕',
};
const stateClass = ['finish', 'doing', 'cancel', 'unknown'];

messaging.onMessage((payload) => {
  const detail = JSON.parse(payload.data.detail);
  // eslint-disable-next-line no-underscore-dangle
  const id = detail._id;
  // change color
  const tr = document.getElementById(`tr-${id}`);
  stateClass.forEach((el) => {
    tr.classList.remove(el);
  });
  tr.classList.add(detail.state);
  // change orderId
  if (detail.state === 'unknown') {
    document.getElementById(`id-${id}`).innerText = '?';
  } else if (detail.state === 'cancel') {
    document.getElementById(`id-${id}`).innerText = 'x';
  } else {
    document.getElementById(`id-${id}`).innerText = detail.orderID;
  }
  // change state
  document.getElementById(`state-${id}`).innerHTML = stateTable[detail.state];
});
