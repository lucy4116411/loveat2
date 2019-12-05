/* global FetchData, $ */
/* eslint no-underscore-dangle: 0 */
/* eslint no-unused-vars: ["error", { "varsIgnorePattern": "deleteItemOrCombo" }] */
const menuEditAPI = {
  all: '/api/menu',
  newType: '/api/menu/type/new',
  updateType: '/api/menu/type/update',
  deleteType: '/api/menu/type/delete',
  deleteItem: '/api/menu/item/delete',
  deleteCombo: '/api/menu/combo/delete',
};

async function deleteItemOrCombo(e) {
  let result;
  if (e.id.match('item')) {
    result = await FetchData.post(menuEditAPI.deleteItem, {
      id: e.id.substring(12),
    });
  } else {
    result = await FetchData.post(menuEditAPI.deleteCombo, {
      id: e.id.substring(13),
    });
  }

  if (result.status === 403) {
    // show wrong msg
    e.setAttribute('data-toggle', 'model');
    e.setAttribute('data-target', '#alert-modal');
    $('#alert-modal').modal('show');
    e.removeAttribute('data-toggle');
    e.removeAttribute('data-target');
  } else {
    // delete row
    const i = e.parentNode.parentNode.rowIndex;
    document.getElementById('menu-table').deleteRow(i);
  }
}

async function menuInit() {
  const menu = document.getElementById('menu');
  const menuArray = await FetchData.get(menuEditAPI.all).then((res) => res.json());
  let tmpTbody = '';
  menuArray.forEach((eachMeal) => {
    const eachMealtype = eachMeal.category;
    // item & combo 's form are different, so need to resolve them, respectively
    eachMeal.content.forEach((element) => {
      // haven't know wheather item or combo, so I write element
      let content = '';
      if (eachMeal.category === 'combo') {
        element.content.forEach((item) => {
          content += `${item.quantity} * ${item.name} <br>`;
        });
      } else {
        content = element.name;
      }
      tmpTbody += `<tr><td>${element.name}</td>
              <td>${element.price}</td>
              <td>${content}</td>
              <td><img src='/img/${element.picture}'></td>
              <td>${element.description}</td>
              <td><button class="btn btn-primary">
                  <a href="{{ url_for('menu_web.edit_item') }}">修改</a>
                  </button>
                  <button id="delete-${eachMealtype}-${element._id}"class="btn btn-primary"onclick="deleteItemOrCombo(this)">刪除</button></td></tr>`;
    });
  });
  menu.innerHTML = tmpTbody;
}

// 這裡等小合用好新的type API 應該需要再改(?
async function getTypeSelection(list) {
  const selection = document.getElementById(list);
  const result = await FetchData.get(menuEditAPI.all).then((res) => res.json());
  result.forEach((Eachresult, index) => {
    const option = document.createElement('option');
    option.text = Eachresult.type;
    option.value = index + 1; // index = 0 is 'all' // not sure value = ? , index+1? type?
    selection.options.add(option);
  });
}
function typeSelectionInit() {
  getTypeSelection('type-list');
  getTypeSelection('update-type-list');
  getTypeSelection('delete-type-list');
}

async function addType() {
  if (document.forms['add-type-form'].reportValidity()) {
    // resolve category's value
    const selection = document.getElementById('item-or-combo-type');
    const category = selection.options[selection.selectedIndex];
    // start post
    const result = await FetchData.post(menuEditAPI.newType, {
      type: document.getElementById('add-type').value,
      category: category.value,
    });

    if (result.status === 403) {
      // show wrong msg
      document.getElementById('add-type-txt').innerText = '權限錯誤。';
    } else if (result.status === 409) {
      document.getElementById('add-type-txt').innerText = '該種類已存在，請重新輸入。';
    } else {
      // show successful msg
      document.getElementById('add-type-txt').innerText = '成功新增！';
      document.getElementById('add-type').value = '';
      selection.options[0].selected = true;
    }
  }
  typeSelectionInit();
}

// 這也是等小河的type API出來
/*
async function updateType() {
  if (document.forms['update-type-form'].reportValidity()) {
    const selection = document.getElementById('update-type-list');
    const category = selection.options[selection.selectedIndex];
    let id;
    const menuArray = await FetchData.get(menuEditAPI.all).then((res) => res.json());
    // 找不到id QQ
    for (index in menuArray) {
      if (category.innerText == menuArray[index].type) {
        console.log(menuArray);
        console.log(menuArray[index]);
        console.log(menuArray[index].content);
        id = menuArray[index].id;
        break;
      }
    }

    console.log(category.innerText);
    console.log(id);
    // start post

        const result = await FetchData.post(menuEditAPI.update, {
            id: document.getElementById('login-user-name').value,
            type: document.getElementById('update-type').value,
        });

        if (result.status === 403) {
            // show wrong msg
            document.getElementById('update-type-txt').innerText = '權限錯誤。';
        } else if (result.status == 409) {
            document.getElementById('update-type-txt').innerText = '該種類已存在。';
        } else {
            // show successful msg
            document.getElementById('update-type-txt').innerText = '重設密碼信件已發送，請至信箱查看。';
            delayURL("/menu", 1800);
        }

  }
}
*/
/*
function deleteType() {
  if (document.forms['delete-type-form'].reportValidity()) {


        const result = await FetchData.post(menuEditAPI.delete, {
            id: document.getElementById('login-user-name').value,
        });

        if (result.status === 403) {
            // show wrong msg
            document.getElementById('delete-type-txt').innerText = '權限錯誤。';
        } else if (result.status == 409) {
            document.getElementById('delete-type-txt').innerText = '該種類已存在。';
        } else {
            // show successful msg
            document.getElementById('delete-type-txt').innerText = '重設密碼信件已發送，請至信箱查看。';
            delayURL("/menu", 1800);
        }

  }
}
*/
function init() {
  typeSelectionInit();
  menuInit();
  document.getElementById('add-type-btn').addEventListener('click', addType);
  // document.getElementById('update-type-btn').addEventListener('click', updateType);
  // document.getElementById('delete-type-btn').addEventListener('click', deleteType);
}

window.addEventListener('load', init);
