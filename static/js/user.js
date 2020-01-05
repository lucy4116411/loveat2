/* global FetchData */
const API = {
  updateState: '/api/user/update/state',
};
let TR = [];

function toggle(ctx) {
  const el = ctx;
  const tr = ctx.parentNode.parentNode;
  if (el.value === 'frozen') {
    el.value = 'activate';
    el.classList.remove('btn-danger');
    el.classList.add('btn-primary');
    el.innerText = '移除';
    tr.classList.add('frozen');
  } else {
    el.value = 'frozen';
    el.classList.add('btn-danger');
    el.classList.remove('btn-primary');
    el.innerText = '加入';
    tr.classList.remove('frozen');
  }
}

async function updateState(e) {
  const result = await FetchData.post(API.updateState, {
    id: e.target.id,
    state: e.target.value,
  });
  if (result.status === 200) {
    toggle(e.target);
  }
}

function search() {
  const tar = document.getElementById('search-name').value;
  TR.forEach((cur) => {
    const account = cur.querySelector('td');
    if (account.innerText.includes(tar)) {
      cur.classList.remove('hidden');
    } else {
      cur.classList.add('hidden');
    }
  });
  return false;
}

function init() {
  // add event listener
  [...document.getElementsByClassName('update-state')].forEach((cur) => {
    cur.addEventListener('click', updateState);
  });
  document.getElementById('search-form').addEventListener('submit', search);
  // get all tr
  const trs = document.querySelectorAll('#user-table > tbody > tr');
  TR = [...trs];
}

window.addEventListener('load', init);
