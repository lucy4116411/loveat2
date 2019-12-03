/* eslint-disable max-len */
/* eslint-disable guard-for-in */
/* eslint-disable no-underscore-dangle */
/* eslint-disable no-restricted-syntax */
/* golbal FetchData, Cart */

const TestCase = [
  {
    _id: '5dd67f098f0f6afb3ebc1b6b',
    category: 'item',
    quantity: 1,
  },
  {
    _id: '5dda567d09d84aa89699121c',
    category: 'combo',
    quantity: 1,
  },
  {
    _id: '5dd67f098f0f6afb3ebc1b6a',
    category: 'item',
    quantity: 1,
  },
  {
    _id: '5dd67f098f0f6afb3ebc1b69',
    category: 'item',
    quantity: 1,
  },
  {
    _id: '5dda57c047b0e46ffecb2b9a',
    category: 'combo',
    quantity: 1,
  },
];


const PREFIX = 'loveat2-cart';


function clearItem() {
  localStorage.clear();
}

async function addItem(dataSet) {
  const tempOrder = await dataSet;
  const jsonOrder = JSON.stringify(tempOrder);
  localStorage.setItem(PREFIX, jsonOrder);
}

async function assignData(item, combo) {
  const tmp = [];
  const itemTmp = await item;
  const comboTmp = await combo;

  for (let i = 0; i < itemTmp.length; i += 1) {
    itemTmp[i].category = 'item';
    itemTmp[i].quantity = 1;
    tmp.push(itemTmp[i]);
  }
  for (let j = 0; j < comboTmp.length; j += 1) {
    comboTmp[j].category = 'combo';
    comboTmp[j].quantity = 1;
    tmp.push(comboTmp[j]);
  }
  return tmp;
}


async function getItem() {
  const dataSet = JSON.parse(localStorage.getItem(PREFIX));
  const itemId = [];
  const comboId = [];
  for (const data in dataSet) {
    if (dataSet[data].category === 'item') {
      itemId.push(dataSet[data]._id);
    } else if (dataSet[data].category === 'combo') {
      comboId.push(dataSet[data]._id);
    }
  }
  const itemData = await FetchData.post('/api/menu/item', itemId);
  const comboData = await FetchData.post('/api/menu/combo', comboId);
  const tmpItem = itemData.json();
  const tmpCombo = comboData.json();
  const tmp = assignData(tmpItem, tmpCombo);
  addItem(tmp);
  return tmp;
}


function clearOrder() {
  document.getElementById('cart-table').innerHTML = '';
  localStorage.removeItem(PREFIX);
}


async function drawItem(dataPromise) {
  const data = await dataPromise;
  const result = Object.keys(data).reduce((acc, key) => `${acc} <tr id="${key}">
              <td>${data[key].name}</td>
              <td>
                <input type="number" id="quantity-${key}" min="1" value="${data[key].quantity}" onclick="changeQuantity(this.id)">
              </td>
              <td>${data[key].price}</td>
              <td>
                <input type="text" id="description-${key}" onclick="changeQuantity(this.id)">
              </td>
              <td id="item-sum-${key}" >${data[key].price}</td>
              <td>
                <button id="delete-${key}" class="btn btn-primary" onClick="deleteItem(this.id)">Delete</button>
              </td>
            </tr>`, '');
  document.getElementById('cart-table').innerHTML = result;
}


function setItem(data) {
  const itemJsonString = JSON.stringify(data);
  localStorage.setItem(PREFIX, itemJsonString);
}


function deleteItem(key) {
  const tar = key.charAt(key.length - 1);
  const dataSet = JSON.parse(localStorage.getItem(PREFIX));
  dataSet.splice(tar, 1);
  // addItem
  if (Object.keys(dataSet).length === 0) {
    localStorage.removeItem(PREFIX);
    // Cart.clear();
  } else {
    const jsonOrder = JSON.stringify(dataSet);
    localStorage.setItem(PREFIX, jsonOrder);
  }
  drawItem(getItem());
}

// 計算單品總價
async function calculateItemPrice(key, quantity) {
  const allItem = getItem();
  const data = await allItem;
  const tar = key.charAt(key.length - 1);
  document.getElementById(`item-sum-${tar}`).innerHTML = quantity * data[tar].price;
}

async function changeQuantity(key) {
  const newQuantity = document.getElementById(key).value;
  const tar = key.charAt(key.length - 1);
  const dataSet = await getItem();
  dataSet[tar].quantity = parseInt(newQuantity, 10);
  for (let i = 0; i < dataSet.length; i += 1) {
    console.log(dataSet[i]);
  }

  // addItem
  const jsonOrder = JSON.stringify(dataSet);
  console.log(jsonOrder);
  localStorage.removeItem(PREFIX);
  localStorage.setItem(PREFIX, jsonOrder);
  // const result = `<input type="number" id="${key}" min="1" value="${newQuantity}" onclick="changeQuantity(this.id)">`;
  // document.getElementById(key).innerHTML = '';
  // document.getElementById(key).innerHTML = result;
  calculateItemPrice(key, newQuantity);
}

function orderSum() {

}

async function dealOrder() {
  const postOrder = [];
  const dataSet = await getItem();
  for (const data in dataSet) {
    const result = {};
    console.log(dataSet[data]);
    result.id = dataSet[data]._id;
    result.category = dataSet[data].category;
    result.quantity = dataSet[data].quantity;
    postOrder.push(result);
  }
  console.log(postOrder);
  return postOrder;
}

async function sendOrder() {
  const order = [];
  order.takenAt = document.getElementById('order-take-time').value;
  order.notes = '不要番茄醬';
  order.total = 490;
  order.content = await dealOrder();
  console.log(order);
  FetchData.post('/api/order/new', order);
}


async function init() {
  // add button listener
  document.getElementById('clear-order').addEventListener('click', clearOrder);
  document.getElementById('send-order').addEventListener('click', sendOrder);
  await addItem(TestCase);
  drawItem(getItem());
}

window.addEventListener('load', init);
