/* eslint-disable no-underscore-dangle */
/* eslint-disable no-unused-vars */
/* global FetchData */

/**
 * @description do operating at local storage
 *
 * @class Cart
 */
class Cart {
  constructor() {
    return (async () => {
      this.prefix = 'loveat2-cart';
      if (this.prefix in localStorage) {
        this.content = JSON.parse(localStorage.getItem(this.prefix));
        const itemList = [];
        const comboList = [];
        Object.keys(this.content).forEach((key) => {
          if (this.content[key].category === 'item') {
            itemList.push(key);
          } else {
            comboList.push(key);
          }
        });
        const itemResult = await FetchData.post('/api/menu/item', itemList).then((res) => res.json());
        const comboResult = await FetchData.post('/api/menu/combo', comboList).then((res) => res.json());
        itemResult.forEach((cur) => {
          this.content[cur._id].price = cur.price;
          this.content[cur._id].name = cur.name;
        });
        comboResult.forEach((cur) => {
          this.content[cur._id].price = cur.price;
          this.content[cur._id].name = cur.name;
        });
      } else {
        this.content = {};
      }
      return this;
    })();
  }

  /**
   * @description update the order which key is loveat2-cart
   *
   * @memberof Cart
   */
  updateLocalStorage() {
    localStorage.setItem(this.prefix, JSON.stringify(this.content));
  }

  /**
   * @description add the item quantity which key is loveat2-cart
   *
   * @param {*} data
   * @memberof Cart
   */
  add(data) {
    if (data._id in this.content) {
      this.content[data._id].quantity += 1;
    } else {
      this.content[data._id] = {
        category: data.category,
        quantity: data.quantity,
      };
    }
    this.updateLocalStorage();
  }

  /**
   * @description get order form local storage
   *
   * @returns
   * @memberof Cart
   */
  get() {
    return this.content;
  }

  /**
   * @description delete the target item by key
   *
   * @param {*} key index of deleting item
   * @memberof Cart
   */
  delete(key) {
    delete this.content[key];
    this.updateLocalStorage();
  }

  /**
   * @description remove the item which key is loveat2-cart
   *
   * @memberof Cart
   */
  clear() {
    localStorage.removeItem(this.prefix);
  }
}
