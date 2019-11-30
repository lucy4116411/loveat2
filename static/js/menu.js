/* global FetchData */
/* eslint no-underscore-dangle: ["error", { "allow": ["_id"] }] */

const MENU_API = '/api/menu';

const ID_TO_NAME = {};// {"_id1":"name1",...}
const TYPE_DATA = {}; // {type1:{"id":[], "category":"item"},...}
let UNCATER_ITEM_INDEX = '';
let UNCATER_COMBO_INDEX = '';
// const CONTENT = []; // for local storage


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

/* ---- load local storage ---- */
/*
async function loadLocalStorage() {

}
*/
/* ---- user add item into local storage ----*/
/*
function setLocalStorage(event) {
  const submitId = event.target.id;
  const id = submitId.replace('submit_', '');
  const inputId = submitId.replace('submit', 'input');
  const quantity = parseInt(document.getElementById(inputId).value);
  let category = '';

  for (const i in TYPE_DATA) {
    if (TYPE_DATA[i].id.includes(id)) {
      category = TYPE_DATA[i].category;
    }
  }

  const data = {
    _id: id,
    category,
    quantity,
  };

  let exitFlag = false;


  if (data.quantity > 0) {
    for (const i of CONTENT) {
      if (id === i._id) {
        i.quantity += quantity;
        exitFlag = true;
      }
    }
    if (exitFlag === false) {
      CONTENT.push({ "_id": id, "category": ID_TO_CATEGORY_DATA[id], quantity });
    }
    // localStorage.setItem('content', CONTENT);
    console.log('CONTENT: ', JSON.stringify(CONTENT));
  }
}
*/
async function init() {
  /* ---- fetch menu data ----- */
  let totalType = 0;
  await FetchData.get(MENU_API)
    .then((res) => res.json()).then((menu) => {
      let itemIndex = 0;
      const itemAll = [];
      const comboAll = [];
      menu.forEach((type) => {
        if (type.type === '未分類(單品)') {
          UNCATER_ITEM_INDEX = `type${itemIndex + 1}`;
        } else if (type.type === '未分類(套餐)') {
          UNCATER_COMBO_INDEX = `type${itemIndex + 1}`;
        }
        TYPE_DATA[`type${itemIndex + 1}`] = { id: [], category: '' };
        TYPE_DATA[`type${itemIndex + 1}`].category = type.category;
        type.content.forEach((i) => {
          if (type.category === 'item') {
            itemAll.push(i._id);
          } else if (type.category === 'combo') {
            comboAll.push(i._id);
          }
          TYPE_DATA[`type${itemIndex + 1}`].id.push(i._id);
          ID_TO_NAME[i._id] = i.name;
        });
        itemIndex += 1;
      });
      TYPE_DATA[UNCATER_ITEM_INDEX].id = itemAll;
      TYPE_DATA[UNCATER_COMBO_INDEX].id = comboAll;
      totalType = itemIndex;
    });
  // load_local_storage();

  /* -- listener for type --*/
  for (let i = 0; i < totalType; i += 1) {
    document.getElementById(`type${i + 1}`).addEventListener('click', searchByType);
  }
  /* -- listener for search --*/
  document.getElementById('search').addEventListener('keypress', searchByName);

  /* -- listener for add item --*/
  /*
  for (const i in ID_TO_NAME) {
    document.getElementById(`submit_${i}`).addEventListener('click', setLocalStorage);
  }
  */
}

window.addEventListener('load', init);
