/* global FetchData, $ */
/* eslint no-underscore-dangle: 0 */

const newItemAPI = '/api/menu/item/new';

function clearContent() {
  document.getElementById('name').value = '';
  document.getElementById('type-list').options[0].selected = true;
  document.getElementById('price').value = '';
  document.getElementById('picture').value = '';
  document.getElementById('picture-show').setAttribute('src', '');
  document.getElementById('description').value = '';
}

async function upload() {
  if (document.forms['item-form'].reportValidity()) {
    const selection = document.getElementById('type-list');
    const index = selection.selectedIndex;
    const myForm = document.getElementById('item-form');
    const formData = new FormData(myForm);
    formData.append('type', selection.options[index].id.substring(5));
    const result = await FetchData.postForm(newItemAPI, formData);
    if (result.status === 403) {
      document.getElementById('alert-title').innerHTML = '發生錯誤！';
      document.getElementById('alert-body').innerHTML = '權限錯誤！請登入後再執行。';
    } else if (result.status === 409) {
      document.getElementById('alert-title').innerHTML = '發生錯誤！';
      document.getElementById('alert-body').innerHTML = '此種類已存在，請更改種類名！。';
    } else {
      document.getElementById('alert-title').innerHTML = '新增成功！';
      document.getElementById('alert-body').innerHTML = '單品新增成功！繼續新增下一筆菜單';
      clearContent();
    }
    $('#alert-modal').modal('show');
  }
}

// display on board instantly
function display() {
  const detail = document.getElementById('detail');
  let description = document.getElementById('description').value;
  description = description.replace(/\n/g, '<br />');
  detail.innerHTML = `名稱：${document.getElementById('name').value} <br>
                    價格：${document.getElementById('price').value} <br>
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
  document.getElementById('clear').addEventListener('click', clearContent);
  document.getElementById('submit').addEventListener('click', upload);
  document.getElementById('name').addEventListener('blur', display);
  document.getElementById('price').addEventListener('blur', display);
  document.getElementById('description').addEventListener('blur', display);
  document.getElementById('picture').addEventListener('change', function read() { readURL(this); });
}

window.addEventListener('load', init);
