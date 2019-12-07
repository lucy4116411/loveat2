const API = EventSource('/api/order/update');

API.onmessage = function updateStatus(event) {
  const jsonObject = JSON.parse(event.data);
  const { orderID } = jsonObject.id;
  const { state } = jsonObject.state;
  let stateMessage = '';
  document.getElementById(orderID).innerHTML = '';// reset

  switch (state) {
    case 'doing': stateMessage = '製作中'; break;
    case 'finish': stateMessage = '已完成'; break;
    case 'cancel': stateMessage = '拒絕'; break;
    case 'unknown': stateMessage = '未回應'; break;
    default: break;
  }

  document.getElementById(orderID).innerHTML = stateMessage;
};
