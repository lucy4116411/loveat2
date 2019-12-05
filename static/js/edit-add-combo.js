/* global FetchData */
/* eslint no-unused-vars: ["error", { "varsIgnorePattern": "deleteItem" }] */
const menuEditAPI = {
  all: '/api/menu',
  newCombo: '/api/menu/item/combo',
};

async function typeSelectionInit() { // 等小河的API出來，應該還會再改
  const selection = document.getElementById('type');
  const result = await FetchData.get(menuEditAPI.all).then((res) => res.json());
  result.forEach((Eachresult, index) => {
    if (Eachresult.category === 'item') {
      const option = document.createElement('option');
      option.text = Eachresult.type;
      option.value = index;
      selection.options.add(option);
    }
  });
}

function deleteItem(e) {
  // delete row
  const i = e.parentNode.parentNode.rowIndex;
  document.getElementById('item-table').deleteRow(i);
}

function addItem() {
  document.getElementById('txt').innerText = '';
  if (document.getElementById('item-quantity').value === '') {
    document.getElementById('txt').innerText = '請填入大於0的數字！';
  } else {
    const itemTbody = document.getElementById('item-tbody');
    const tmp = `<tr><td>${document.getElementById('item').value}</td>
            <td>${document.getElementById('item-quantity').value}</td>
            <td><button type="button" class="btn btn-primary" onclick="deleteItem(this)">刪除</button></td></tr>`;
    itemTbody.innerHTML += tmp;
    // to initialize form table
    document.getElementById('item-type').value = ''; // 選擇第一個
    document.getElementById('item').value = ''; // 選擇第一個
    document.getElementById('item-quantity').value = 1;
  }
}

function upload() { // combo比較不一樣的是，要先處理content轉為字串，再用formData.append把content加進去再回傳
  if (document.forms['combo-form'].reportValidity()) {
    // 不確定下巴要textarea船到資料庫是要\n還是<br>?
    // let description = document.getElementById('description').value;
    // document.getElementById('description').value = description.replace(/\n/g, '<br />');
    const myForm = document.getElementById('myForm');
    const formData = new FormData(myForm);
    const option = {
      method: 'POST',
      body: formData,
    };
    fetch(menuEditAPI.newItem, option);
  }
}

// display on board instantly
function display() {
  const detail = document.getElementById('detail');
  let description = document.getElementById('description').value;
  description = description.replace(/\n/g, '<br />');
  detail.innerHTML = `名稱：${document.getElementById('name').value} <br>
                    價格：${document.getElementById('price').value} <br>
                    品項：<br>
                    說明：${description}`;
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
  typeSelectionInit();
  document.getElementById('submit').addEventListener('click', upload);
  document.getElementById('add-item-btn').addEventListener('click', addItem);
  document.getElementById('name').addEventListener('blur', display);
  document.getElementById('price').addEventListener('blur', display);
  document.getElementById('description').addEventListener('blur', display);
  document.getElementById('picture').addEventListener('change', function read() { readURL(this); });
}

window.addEventListener('load', init);
