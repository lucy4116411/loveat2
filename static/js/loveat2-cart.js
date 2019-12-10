
/* eslint-disable no-unused-vars */
/* global Cart, $, FetchData */
/* eslint no-underscore-dangle: ["error", {"allow":["_id"]}] */

let myCart = null;


function orderTotal() {
  let total = 0;
  const dataSet = myCart.get();
  Object.keys(dataSet).forEach((key) => {
    total += dataSet[key].quantity * dataSet[key].price;
  });
  document.getElementById('total').innerHTML = total;
}

function deleteItem(e) {
  const itemId = e.target.id.substr(7);
  const key = e.target.parentNode.parentNode.rowIndex;
  myCart.delete(itemId);
  document.getElementById('cart-table').deleteRow(key);
  orderTotal();
}


function updateSum(id) {
  const order = myCart.get();
  document.getElementById(`item-sum-${id}`).innerHTML = order[id].price * order[id].quantity;
}

function changeQuantity(e) {
  let newQuantity = parseInt(e.target.value, 10);
  const id = e.target.id.substr(9);

  if (newQuantity <= 0 || Number.isNaN(newQuantity)) {
    document.getElementById('hint-content').innerHTML = '輸入錯誤';
    document.getElementById('bussiness_data').style.display = 'none';
    $('#order-send-hint-modal').modal('show');
    newQuantity = 1;
    e.target.value = newQuantity;
  }

  myCart.updateQuantity(id, newQuantity);
  updateSum(id);
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
  const dataSet = myCart.get();
  const postOrder = Object.keys(dataSet).reduce((acc, key) => {
    acc.push({
      id: key,
      category: dataSet[key].category,
      quantity: dataSet[key].quantity,
    });
    return acc;
  }, []);
  return postOrder;
}

function clearOrder() {
  myCart.clear();
  document.getElementById('item-table').innerHTML = '';
  document.getElementById('total').innerHTML = 0;
}

function toState() {
  window.location = '/order/state';
}

function checkStatus(status) {
  const order = myCart.get();
  if (status === 200) {
    document.getElementById('close-modal').addEventListener('click', toState);
    document.getElementById('hint-content').innerHTML = '下單成功';
    document.getElementById('bussiness_data').style.display = 'none';
    clearOrder();
  } else if (status === 401) {
    document.getElementById('hint-content').innerHTML = '您尚未登入';
    document.getElementById('bussiness_data').style.display = 'none';
  } else {
    document.getElementById('hint-content').innerHTML = '訂單錯誤或預定取餐時間未營業';
  }
  $('#order-send-hint-modal').modal('show');
}

async function sendOrder() {
  const takenTime = document.getElementById('order-take-time').value;
  if (takenTime === null || Date.parse(takenTime).valueOf() < Date.now()) {
    document.getElementById('hint-content').innerHTML = '訂單錯誤或預定取餐時間未營業';
    $('#order-send-hint-modal').modal('show');
  } else {
    const order = {};
    const total = document.getElementById('total').innerHTML;
    order.takenAt = takenTime;
    order.notes = orderDescription();
    order.total = parseInt(total, 10);
    order.content = orderContent();
    const response = await FetchData.post('/api/order/new', order);
    checkStatus(response.status);
  }
}

function drawItem(data) {
  const result = Object.keys(data).reduce((acc, key) => `${acc} <tr id="${key}">
              <td>${data[key].name}</td>
              <td>
                <input type="number" id="quantity-${key}" min="1" value="${data[key].quantity}" class="quantity-input form-control">
              </td>
              <td>${data[key].price}</td>
              <td>
                <input class="form-control" type="text" id="description-${key}">
              </td>
              <td id="item-sum-${key}" >${data[key].price * data[key].quantity}</td>
              <td>
                <button id="delete-${key}" class="btn btn-primary delete-item" type="button">Delete</button>
              </td>
            </tr>`, '');
  // draw it
  document.querySelector('#cart-table tbody').innerHTML = result;
  // add event listener
  const quantityInput = document.getElementsByClassName('quantity-input');
  [...quantityInput].forEach((cur) => {
    cur.addEventListener('change', changeQuantity);
  });

  const deleteBtn = document.getElementsByClassName('delete-item');
  [...deleteBtn].forEach((cur) => {
    cur.addEventListener('click', deleteItem);
  });
}


async function init() {
  myCart = await new Cart();
  orderTotal();
  drawItem(myCart.get());
  document.getElementById('clear-order').addEventListener('click', clearOrder);
  document.getElementById('send-order').addEventListener('click', sendOrder);
}

window.addEventListener('load', init);
