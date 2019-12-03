/* global FetchData , */
const bsAPI = {
  business_time: '/api/setting/business-time',
};

async function update() {
  const result = await FetchData.post(bsAPI.business_time, {
    mon: {
      start: document.getElementById('monStart').value,
      end: document.getElementById('monEnd').value,
    },
    tue: {
      start: document.getElementById('tueStart').value,
      end: document.getElementById('tueEnd').value,
    },
    wed: {
      start: document.getElementById('wedStart').value,
      end: document.getElementById('wedEnd').value,
    },
    thu: {
      start: document.getElementById('thuStart').value,
      end: document.getElementById('thuEnd').value,
    },
    fri: {
      start: document.getElementById('friStart').value,
      end: document.getElementById('friEnd').value,
    },
    sat: {
      start: document.getElementById('satStart').value,
      end: document.getElementById('satEnd').value,
    },
    sun: {
      start: document.getElementById('sunStart').value,
      end: document.getElementById('sunEnd').value,
    },
  });
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
