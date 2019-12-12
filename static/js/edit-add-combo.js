/* global FetchData, $ */
/* eslint no-underscore-dangle: 0 */
/* eslint no-unused-vars: ["error", { "varsIgnorePattern": "deleteItem" }] */
const menuEditAPI = {
  all: '/api/menu',
  newCombo: '/api/menu/combo/new',
};

const itemsObj = {};

function display() {
  const detail = document.getElementById('detail');
  let description = document.getElementById('description').value;
  description = description.replace(/\n/g, '<br />');

  const itemTbodyRows = document.querySelectorAll('#item-table tbody tr');
  let items = '';
  Array.from(itemTbodyRows).forEach((eachItem) => {
    items += `<br>&nbsp;&nbsp;&nbsp;&nbsp;${eachItem.cells[1].innerHTML} * ${eachItem.cells[0].innerHTML}`;
  });

  detail.innerHTML = `名稱：${document.getElementById('name').value} <br>
                    價格：${document.getElementById('price').value} <br>
                    品項：${items}<br>
                    說明：${description}`;
}


function clearContent() {
  const idName = ['name', 'price', 'picture', 'description'];
  idName.forEach((id) => {
    document.getElementById(id).value = '';
  });
  document.getElementById('type-list').options[0].selected = true; // select no.1 option
  document.getElementById('picture-show').setAttribute('src', '');
  document.getElementById('item-type').options[0].selected = true; // select no.1 option
  document.getElementById('item-quantity').value = 1;
  document.querySelector('#item-table tbody').innerHTML = '';
  Object.keys(itemsObj).forEach((item) => {
    delete itemsObj[item];
  });
  display();
}

function checkStatus(status) {
  const statusResult = {
    403: {
      title: '發生錯誤',
      body: '權限錯誤！請登入後再執行。',
    },
    409: {
      title: '發生錯誤',
      body: '此名稱已存在，請更改名字！。',
    },
    200: {
      title: '單品新增成功',
      body: '單品新增成功！繼續新增下一筆菜單',
    },
  };

  if (status === 200) clearContent();
  document.getElementById('alert-title').innerHTML = statusResult[status].title;
  document.getElementById('alert-body').innerHTML = statusResult[status].body;
  $('#alert-modal').modal('show');
}

// display on board instantly


async function itemBytypeInit() {
  document.getElementById('item').options.length = 0;
  const res = await FetchData.get(menuEditAPI.all);
  const result = await res.json();
  result.forEach((items) => {
    if (items.type === document.getElementById('item-type').value) {
      items.content.forEach((item) => {
        const option = document.createElement('option');
        option.text = item.name;
        option.id = `item-${item._id}`;
        document.getElementById('item').options.add(option);
      });
    }
  });
  // select no.1 option
  document.getElementById('item').options[0].selected = true;
}

function deleteItem(e) {
  // delete row
  const i = e.parentNode.parentNode.rowIndex;
  const itemsTable = document.getElementById('item-table');
  const deleteItemRow = [...itemsTable.rows][i];
  const itemId = deleteItemRow.id;

  itemsTable.deleteRow(i);
  delete itemsObj[itemId];
  display();
}

function addItem() {
  document.getElementById('txt').innerText = '';
  if (document.getElementById('item-quantity').value > 0) {
    const itemTbody = document.querySelector('#item-table tbody');
    const item = document.getElementById('item');
    const itemId = item.options[item.selectedIndex].id.substring(5);
    const itemQuantity = document.getElementById('item-quantity').value;
    if (itemId in itemsObj) {
      itemsObj[itemId].quantity += parseInt(itemQuantity, 10);
      document.getElementById(`quantity-${itemId}`).innerHTML = itemsObj[itemId].quantity;
    } else {
      itemsObj[itemId] = {
        name: item.value,
        quantity: parseInt(itemQuantity, 10),
      };
      const tmp = `<tr id="${itemId}"><td>${itemsObj[itemId].name}</td>
            <td id ="quantity-${itemId}">${itemsObj[itemId].quantity}</td>
            <td><button type="button" id="delete-${itemId}" class="btn btn-primary delete-btn" onclick="deleteItem(this)">刪除</button></td></tr>`;
      itemTbody.insertAdjacentHTML('beforeend', tmp);
    }
    // to initialize form table
    document.getElementById('item-type').options[0].selected = true; // 選擇第一個
    itemBytypeInit();
    document.getElementById('item-quantity').value = 1;
  } else {
    document.getElementById('txt').innerText = '請填入大於0的數字！';
  }
  display();
}

async function upload() {
  if (document.forms['combo-form'].reportValidity()) {
    if (document.querySelector('#item-table tbody').innerHTML === '') {
      document.getElementById('txt').innerText = '請至少加入一項！';
    } else {
      const selection = document.getElementById('type-list');
      const index = selection.selectedIndex;

      let content = [];
      const rows = document.getElementById('item-table').getElementsByTagName('tr');
      Array.from(rows).forEach((itemRow) => {
        if (itemRow.id.match('item-')) {
          content.push({
            id: itemRow.id.substring(5),
            quantity: itemRow.cells[1].innerHTML,
          });
        }
      });
      content = JSON.stringify(content);
      const myForm = document.getElementById('combo-form');
      const formData = new FormData(myForm);


      formData.append('type', selection.options[index].id.substring(5));
      formData.append('price', document.getElementById('price').value);
      formData.append('content', content);

      const result = await FetchData.postForm(menuEditAPI.newCombo, formData);
      checkStatus(result.status);
    }
  }
}


// let picture can show instantly
function readURL(input) {
  if (input.files && input.files[0]) {
    const reader = new FileReader();
    reader.onload = function loadPicture(e) {
      document.getElementById('picture-show').setAttribute('src', e.target.result);
    };
    reader.readAsDataURL(input.files[0]);
  }
}


function init() {
  itemBytypeInit();
  document.getElementById('clear').addEventListener('click', clearContent);
  document.getElementById('submit').addEventListener('click', upload);
  document.getElementById('add-item-btn').addEventListener('click', addItem);
  document.getElementById('name').addEventListener('change', display);
  document.getElementById('price').addEventListener('change', display);
  document.getElementById('price').addEventListener('keyup', display);
  document.getElementById('description').addEventListener('change', display);
  document.getElementById('picture').addEventListener('change', function read() { readURL(this); });
  document.getElementById('item-type').addEventListener('change', itemBytypeInit);
}

window.addEventListener('load', init);
