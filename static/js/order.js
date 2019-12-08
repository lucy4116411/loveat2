/* global  $, FetchData,messaging */
/* eslint no-underscore-dangle: 0 */
/* eslint-disable no-unused-vars */

const updateOrderAPI = '/api/order/update';

async function update(state, id) {
  const result = await FetchData.post(updateOrderAPI, {
    id,
    state,
  });
  if (result.status === 200) {
    const idx = document.getElementById(id).rowIndex;
    document.getElementById('pending-table').deleteRow(idx);
  } else {
    document.getElementById('orderHintContent').innerHTML = '更新訂單失敗!<br>請再次點擊訂單';
    $('#orderHintModal').modal('show');
  }
}

messaging.onMessage((payload) => {
  const detail = JSON.parse(payload.data.detail);
  const table = document.querySelector('#pending-table tbody');

  // set <td> detail.content[i].name * detail.content[i].quantity
  const content = detail.content.reduce((acc, cur) => `${acc} ${cur.name}*${cur.quantity}<br>`, '');

  const result = `
    <tr>
      <td>${detail.takenAt}</td>
      <td>${content}</td>
      <td>${detail.notes}</td>
      <td>
        <button class= "btn btn-primary" onclick='update('doing',${detail._id})'>接受</button>
        <button class= "btn btn-danger" onclick='update('cancel',${detail._id})'>拒絕</button>
      </td>

    </tr>
  `;
  table.innerHTML += result;
  console.log("new message");
  console.log(result);
});
