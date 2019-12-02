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
  if (result.status === 403) { alert('無此權限'); } else if (result.status === 400) { alert('格式錯誤'); } else { window.location.reload(); }
}

function saveTime() {
  const value1 = document.getElementById('monStart').value;
  const value2 = document.getElementById('monEnd').value;
  const value3 = document.getElementById('tueStart').value;
  const value4 = document.getElementById('tueEnd').value;
  const value5 = document.getElementById('wedStart').value;
  const value6 = document.getElementById('wedEnd').value;
  const value7 = document.getElementById('thuStart').value;
  const value8 = document.getElementById('thuEnd').value;
  const value9 = document.getElementById('friStart').value;
  const value10 = document.getElementById('friEnd').value;
  const value11 = document.getElementById('satStart').value;
  const value12 = document.getElementById('satEnd').value;
  const value13 = document.getElementById('sunStart').value;
  const value14 = document.getElementById('sunEnd').value;
  localStorage.setItem('time1', value1);
  localStorage.setItem('time2', value2);
  localStorage.setItem('time3', value3);
  localStorage.setItem('time4', value4);
  localStorage.setItem('time5', value5);
  localStorage.setItem('time6', value6);
  localStorage.setItem('time7', value7);
  localStorage.setItem('time8', value8);
  localStorage.setItem('time9', value9);
  localStorage.setItem('time10', value10);
  localStorage.setItem('time11', value11);
  localStorage.setItem('time12', value12);
  localStorage.setItem('time13', value13);
  localStorage.setItem('time14', value14);
  update();
}

window.onload = function () {
  document.getElementById('btn').addEventListener('click', saveTime);
  document.getElementById('monStart').value = localStorage.getItem('time1');
  document.getElementById('monEnd').value = localStorage.getItem('time2');
  document.getElementById('tueStart').value = localStorage.getItem('time3');
  document.getElementById('tueEnd').value = localStorage.getItem('time4');
  document.getElementById('wedStart').value = localStorage.getItem('time5');
  document.getElementById('wedEnd').value = localStorage.getItem('time6');
  document.getElementById('thuStart').value = localStorage.getItem('time7');
  document.getElementById('thuEnd').value = localStorage.getItem('time8');
  document.getElementById('friStart').value = localStorage.getItem('time9');
  document.getElementById('friEnd').value = localStorage.getItem('time10');
  document.getElementById('satStart').value = localStorage.getItem('time11');
  document.getElementById('satEnd').value = localStorage.getItem('time12');
  document.getElementById('sunStart').value = localStorage.getItem('time13');
  document.getElementById('sunEnd').value = localStorage.getItem('time14');
  // localStorage.clear();
};
