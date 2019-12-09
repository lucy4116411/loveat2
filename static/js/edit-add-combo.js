/* global FetchData, $ */
/* eslint no-underscore-dangle: 0 */
/* eslint no-unused-vars: ["error", { "varsIgnorePattern": "deleteItem" }] */
const menuEditAPI = {
  all: '/api/menu',
  newCombo: '/api/menu/combo/new',
};

function display() {
  const detail = document.getElementById('detail');
  let description = document.getElementById('description').value;
  description = description.replace(/\n/g, '<br />');
  detail.innerHTML = `名稱：${document.getElementById('name').value} <br>
                    價格：${document.getElementById('price').value} <br>
                    品項：<br>
                    說明：${description}`;
}

function clearContent() {
  document.getElementById('name').value = '';
  document.getElementById('type-list').options[0].selected = true;
  document.getElementById('price').value = '';
  document.getElementById('picture').value = '';
  document.getElementById('picture-show').setAttribute('src', '');
  document.getElementById('description').value = '';

  document.getElementById('item-type').options[0].selected = true; // 選擇第一個
  // document.getElementById('item').options[0].selected=true; // 選擇第一個
  document.getElementById('item-quantity').value = 1;


  document.getElementById('item-tbody').innerHTML = '';
  display();
}

async function itemBytypeInit() {
  document.getElementById('item').options.length = 0;
  const result = await FetchData.get(menuEditAPI.all).then((res) => res.json());
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
  document.getElementById('item').options[0].selected = true; // 選擇第一個
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
    const item = document.getElementById('item');
    const tmp = `<tr id="${item.options[item.selectedIndex].id}"><td>${item.value}</td>
            <td>${document.getElementById('item-quantity').value}</td>
            <td><button type="button" class="btn btn-primary" onclick="deleteItem(this)">刪除</button></td></tr>`;
    itemTbody.innerHTML += tmp;
    // to initialize form table
    document.getElementById('item-type').options[0].selected = true; // 選擇第一個
    itemBytypeInit();
    document.getElementById('item-quantity').value = 1;
  }
}

async function upload() {
  if (document.forms['combo-form'].reportValidity()) {
    const selection = document.getElementById('type-list');
    const index = selection.selectedIndex;

    // 尚未檢查，等model出來
    let content = '[';
    const rows = document.getElementById('item-table').getElementsByTagName('tr');
    const len = rows.length - 1;
    Array.from(rows).forEach((itemRow, i) => {
      if (itemRow.id.match('item-')) {
        content += `{"id":"${itemRow.id.substring(5)}","quantity":${itemRow.cells[1].innerHTML}}`;
      }
      if (i !== 0 && i < len) content += ',';
    });
    content += ']';
    const myForm = document.getElementById('combo-form');
    const formData = new FormData(myForm);


    formData.append('type', selection.options[index].id.substring(5));
    formData.append('price', document.getElementById('price').value);
    formData.append('content', content);

    const result = await FetchData.postForm(menuEditAPI.newCombo, formData);

    if (result.status === 403) {
      document.getElementById('alert-title').innerHTML = '發生錯誤！';
      document.getElementById('alert-body').innerHTML = '權限錯誤！請登入後再執行。';
    } else if (result.status === 409) {
      document.getElementById('alert-title').innerHTML = '發生錯誤！';
      document.getElementById('alert-body').innerHTML = '此種類已存在，請更改種類名！。';
    } else {
      document.getElementById('alert-title').innerHTML = '新增成功！';
      document.getElementById('alert-body').innerHTML = '單品新增成功！繼續新增下一筆菜單';
      // to initialized all
      clearContent();
    }
    $('#alert-modal').modal('show');
  }
}

// display on board instantly

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
  document.getElementById('name').addEventListener('blur', display);
  document.getElementById('price').addEventListener('blur', display);
  document.getElementById('description').addEventListener('blur', display);
  document.getElementById('picture').addEventListener('change', function read() { readURL(this); });
  document.getElementById('item-type').addEventListener('change', itemBytypeInit);
}

window.addEventListener('load', init);
