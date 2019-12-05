/* global FetchData */

const menuEditAPI = {
  all: '/api/menu',
  newItem: '/api/menu/item/new',
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

function upload() {
  if (document.forms['item-form'].reportValidity()) {
  // 不確定下巴要textarea船到資料庫是要\n還是<br>?
    // let description = document.getElementById('description').value;
    // document.getElementById('description').value = description.replace(/\n/g, '<br />');
    const myForm = document.getElementById('item-form');
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
  document.getElementById('name').addEventListener('blur', display);
  document.getElementById('price').addEventListener('blur', display);
  document.getElementById('description').addEventListener('blur', display);
  document.getElementById('picture').addEventListener('change', function read() { readURL(this); });
}

window.addEventListener('load', init);
