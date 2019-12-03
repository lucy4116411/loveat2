/* eslint-disable no-unused-vars */
/* global Cart, $, FetchData */
/* eslint no-underscore-dangle: ["error", {"allow":["_id"]}] */
let myCart = null;

function drawItem(data) {
  const result = Object.keys(data).reduce((acc, key) => `${acc} <tr id="${key}">
              <td>${data[key].name}</td>
              <td>
                <input type="number" id="quantity-${key}" min="1" value="${data[key].quantity}" onclick="changeQuantity(this.id)">
              </td>
              <td>${data[key].price}</td>
              <td>
                <input type="text" id="description-${key}">
              </td>
              <td id="item-sum-${key}" >${data[key].price}</td>
              <td>
                <button id="delete-${key}" class="btn btn-primary" onClick="deleteItem(this.id)">Delete</button>
              </td>
            </tr>`, '');
  document.getElementById('cart-table').innerHTML = result;
}


function deleteItem(key) {
  const id = key.substr(7);
  myCart.delete(id);
  document.getElementById(id).innerHTML = '';
}

function orderTotal() {
  let total = 0;
  const dataSet = myCart.get();
  Object.keys(dataSet).forEach((key) => {
    total += dataSet[key].quantity * dataSet[key].price;
  });
  document.getElementById('total').innerHTML = total;
}

function changeQuantity(key) {
  const id = key.substr(9);
  const newQuantity = document.getElementById(key).value;
  const order = myCart.get();
  order[id].quantity = newQuantity;
  myCart.updateLocalStorage();
  document.getElementById(`item-sum-${id}`).innerHTML = order[id].price * order[id].quantity;
  orderTotal();
}

function orderDescription() {
  const description = [];
  const dataSet = myCart.get();
  Object.keys(dataSet).forEach((key) => {
    const text = document.getElementById(`description-${key}`).value;
    if (text !== '') {
      description.push(`${dataSet[key].name}:${text}`);
    }
  });
  return description.join(';');
}

function orderContent() {
  const postOrder = [];
  const dataSet = myCart.get();

  Object.keys(dataSet).forEach((key) => {
    const result = {};
    result.id = key;
    result.category = dataSet[key].category;
    result.quantity = dataSet[key].quantity;
    postOrder.push(result);
  });

  return postOrder;
}

function clearOrder() {
  myCart.clear();
  document.getElementById('cart-table').innerHTML = '';
}

function toState() {
  window.location = '/order/state';
}

function checkStatus(state) {
  if (state === 200) {
    document.getElementById('close-modal').addEventListener('click', toState);
    document.getElementById('hint-content').innerHTML = '下單成功';
    $('#order-send-hint-modal').modal('show');
    clearOrder();
  } else if (state === 401) {
    document.getElementById('hint-content').innerHTML = '您尚未登入';
    $('#order-send-hint-modal').modal('show');
  } else {
    document.getElementById('hint-content').innerHTML = '訂單錯誤或預定取餐時間未營業';
    $('#order-send-hint-modal').modal('show');
  }
}

async function sendOrder() {
  const order = {};
  const total = document.getElementById('total').innerHTML;
  order.takenAt = document.getElementById('order-take-time').value;
  order.notes = orderDescription();
  order.total = parseInt(total, 10);
  order.content = orderContent();
  const response = await FetchData.post('/api/order/new', order);
  checkStatus(response.status);
}


async function init() {
  myCart = await new Cart();
  orderTotal();
  drawItem(myCart.get());
  document.getElementById('clear-order').addEventListener('click', clearOrder);
  document.getElementById('send-order').addEventListener('click', sendOrder);
}

window.addEventListener('load', init);
