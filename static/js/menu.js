/* global FetchData */
const MENU_API = "/api/menu";


MENU_DATA = []; //menu data
ID_TO_NAME = {};//{"_id1":"name1",...}
TYPE_DATA = {}; //{type1:{"id":[], "category":"item"},...}
CONTENT = [];   //for local storage


/*---- 點選type 將其他type相關之餐點class設為hidden----*/
function search_by_type(event) {
  let tar_type = event.target.id;
  for(let type in TYPE_DATA){
    if(tar_type != type){
      for(let id of TYPE_DATA[type]['id']){
        document.getElementById(id).classList.add("hidden");
      }
    }
    else{
      for(let id of TYPE_DATA[type]['id']){
        document.getElementById(id).classList.remove("hidden");
      }
    }
  }
}

/*---- search by name ---- */
function search_by_name(event){
  if(event.which == 13){// enter key
    let item_name = document.getElementById("search").value;
    for(let i in ID_TO_NAME){
      if(ID_TO_NAME[i].includes(item_name)){
        document.getElementById(i).classList.remove("hidden");
      }
      else{
        document.getElementById(i).classList.add("hidden");
      }
    }
  }
}

/*---- load local storage ---- */
async function load_local_storage(){
  if(typeof localStorage !=="undefined"){
    try{
      CONTENT = await localStorage.getItem('content');
      console.log("load a local storage");
    }catch(e){
      console.log("some error",e);
    }
  }
  else{
    localStorage.setItem('content') = [];
    console.log("initialize the local storage");
  }
}

/*---- user add item into local storage ----*/ 
function set_local_storage(event){
  
  let submit_id = event.target.id;
  let id = submit_id.replace("submit_","");
  let input_id = submit_id.replace("submit","input");
  let quantity = parseInt(document.getElementById(input_id).value);
  let category = "";

  for(let i in TYPE_DATA){
    if(TYPE_DATA[i]['id'].includes(id)){
      category = TYPE_DATA[i]['category'];
    }
  }

  let data = {
              "_id": id,
              "category":category,
              "quantity":quantity
             };
  
  console.log(data);
  let exit_flag = false;

  
  if(data["quantity"] > 0){
    for(let i of CONTENT){
      if(id == i["_id"]){
        i["quantity"] += quantity; 
        exit_flag = true;
      }
    }
    if(exit_flag == false){
      CONTENT.push({"_id":id,"category":ID_TO_CATEGORY_DATA[id],"quantity":quantity});
    }
    //localStorage.setItem('content', CONTENT);
    console.log("CONTENT: ",JSON.stringify(CONTENT));
  }

}

async function init() {
  /*---- fetch menu data ----- */
  total_type = 0;
  await FetchData.get(MENU_API)
  .then(res => {
    return res.json();
  }).then(menu =>{
    let item_index = 0;
    menu.forEach(function(type){
      TYPE_DATA[`type${item_index+1}`] = {'id':[],'category':""};
      TYPE_DATA[`type${item_index+1}`]['category'] = type['category'];
      for(let i of type['content']){
        TYPE_DATA[`type${item_index+1}`]['id'].push(i['_id']);
        ID_TO_NAME[i['_id']] = i['name'];
      }
      item_index += 1;
    });
    total_type = item_index;
  });
  load_local_storage();
  
  /*-- listener for type --*/
  for (let i = 0 ;i < total_type; i++) {
    document.getElementById(`type${i+1}`).addEventListener('click', search_by_type);
  }
  /*-- listener for search --*/
  document.getElementById("search").addEventListener('keypress', search_by_name);

  /*-- listener for add item --*/
  for(let i in ID_TO_NAME){
    document.getElementById(`submit_${i}`).addEventListener('click', set_local_storage);
  }
}

window.addEventListener('load', init);
