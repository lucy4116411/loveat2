/* global Cart, FetchData */
/* eslint no-underscore-dangle: ["error", { "allow": ["_id"] }] */


const ID_TO_NAME = {}; // {"_id1":"name1",...}
const TYPE_DATA = {}; // {type1:{"id":[], "category":"item"},...}
let UNCATER_ITEM_INDEX = '';
let UNCATER_COMBO_INDEX = '';
let myCart = null;


/* ---- 點選type 將其他type相關之餐點class設為hidden----*/
function searchByType(event) {
  const tarType = event.target.id;
  const tarTypeId = TYPE_DATA[tarType].id;
  tarTypeId.forEach((id) => {
    document.getElementById(id).classList.remove('hidden');
  });
  if (tarType === UNCATER_ITEM_INDEX || tarType === UNCATER_COMBO_INDEX) {
    if (tarType === UNCATER_ITEM_INDEX) {
      TYPE_DATA[UNCATER_COMBO_INDEX].id.forEach((id) => {
        document.getElementById(id).classList.add('hidden');
      });
    } else {
      TYPE_DATA[UNCATER_ITEM_INDEX].id.forEach((id) => {
        document.getElementById(id).classList.add('hidden');
      });
    }
  } else {
    Object.keys(TYPE_DATA).forEach((type) => {
      if (tarType !== type && type !== UNCATER_ITEM_INDEX && type !== UNCATER_COMBO_INDEX) {
        TYPE_DATA[type].id.forEach((id) => {
          document.getElementById(id).classList.add('hidden');
        });
      }
    });
  }
}

/* ---- search by name ---- */
function searchByName(event) {
  if (event.which === 13) { // enter key
    const itemName = document.getElementById('search').value;
    Object.keys(ID_TO_NAME).forEach((id) => {
      if (ID_TO_NAME[id].includes(itemName)) {
        document.getElementById(id).classList.remove('hidden');
      } else {
        document.getElementById(id).classList.add('hidden');
      }
    });
  }
}

/* ---- user add item into local storage ----*/
async function addContent(event) {
  const itemId = event.target.id.replace('submit_', '');
  const itemQuantity = parseInt(document.getElementById(`input_${itemId}`).value, 10);
  let itemCategory = '';

  Object.keys(TYPE_DATA).forEach((type) => {
    if (TYPE_DATA[type].id.includes(itemId)) {
      itemCategory = TYPE_DATA[type].category;
    }
  });

  const data = {
    _id: itemId,
    category: itemCategory,
    quantity: itemQuantity,
  };

  myCart.add(data);
}

async function init() {
  myCart = await new Cart();
  /* ---- fetch menu data ----- */
  const res = await FetchData.get('/api/menu');
  const menu = await res.json();
  let totalType = 0;
  const itemAll = [];
  const comboAll = [];
  menu.forEach((type) => {
    if (type.type === '未分類(單品)') {
      UNCATER_ITEM_INDEX = `type${totalType + 1}`;
    } else if (type.type === '未分類(套餐)') {
      UNCATER_COMBO_INDEX = `type${totalType + 1}`;
    }
    TYPE_DATA[`type${totalType + 1}`] = { id: [], category: '' };
    TYPE_DATA[`type${totalType + 1}`].category = type.category;
    type.content.forEach((i) => {
      if (type.category === 'item') {
        itemAll.push(i._id);
      } else if (type.category === 'combo') {
        comboAll.push(i._id);
      }
      TYPE_DATA[`type${totalType + 1}`].id.push(i._id);
      ID_TO_NAME[i._id] = i.name;
    });
    totalType += 1;
  });
  TYPE_DATA[UNCATER_ITEM_INDEX].id = itemAll;
  TYPE_DATA[UNCATER_COMBO_INDEX].id = comboAll;


  /* -- listener for type --*/
  for (let i = 0; i < totalType; i += 1) {
    document.getElementById(`type${i + 1}`).addEventListener('click', searchByType);
  }
  /* -- listener for search --*/
  document.getElementById('search').addEventListener('keypress', searchByName);

  /* -- listener for add item --*/
  Object.keys(ID_TO_NAME).forEach((i) => {
    document.getElementById(`submit_${i}`).addEventListener('click', addContent);
  });
}

window.addEventListener('load', init);
