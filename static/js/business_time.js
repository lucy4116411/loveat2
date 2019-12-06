/* global FetchData , */
const bsAPI = {
  business_time: '/api/setting/business-time',
};

async function update() {
  const setTime = {};
  const week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'];
  week.forEach((element) => {
    setTime[element] = {
      start: document.getElementById(`${element}Start`).value,
      end: document.getElementById(`${element}End`).value,
    };
  });
  const result = await FetchData.post(bsAPI.business_time, setTime);
  if (result.status === 403) {
    document.getElementById('inform').outerText = '無此權限';
  } else if (result.status === 400) {
    document.getElementById('inform').outerText = '格式錯誤';
  } else {
    document.getElementById('inform').outerText = '更新成功';
  }
}

window.onload = function () {
  document.getElementById('btn').addEventListener('click', update);
};
