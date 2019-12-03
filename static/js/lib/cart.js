// eslint-disable-next-line no-unused-vars
class Cart {
  constructor() {
    this.prefix = 'loveat2-cart';
    if (this.prefix in localStorage) {
      this.content = JSON.parse(localStorage.getItem(this.prefix));
    } else {
      this.content = {};
    }
  }

  updateLocalStorage() {
    localStorage.setItem(this.prefix, JSON.stringify(this.content));
  }

  add(data) {
    if (data.id in this.content) {
      this.content[data.id].quantity += 1;
    } else {
      this.content[data.id] = {
        quantity: data.quantity,
      };
    }
    this.updateLocalStorage();
  }

  get() {
    return this.content;
  }

  delete(key) {
    delete this.content[key];
    this.updateLocalStorage();
  }

  clear() {
    localStorage.removeItem(this.prefix);
  }
}
