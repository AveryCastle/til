function freeTieClip(cart) {
    let hasTie = isInCart(cart, 'tie');
    let hasTieClip = isInCart(cart, 'tie clip');

    if (hasTie && !hasTieClip) {
        let tieClip = make_item("tie_clip", 0);
        return add_item(cart, tieClip);
    }

    return cart;
}

function add_item(cart, item) {
    return add_element_last(cart, item);
}

function isInCart(cart, name) {
    return indexOfItem(cart, name) !== null;
}

function make_item(name, price) {
    return {
        name: name,
        price: price,
    };
}

function remove_item_by_name(cart, name) {
    let idx = indexOfItem(cart, name);
    if (idx != null) {
        return removeItems(cart, idx, 1);
    }
    return cart;
}

function indexOfItem(cart, name) {
    for (let i = 0; i < cart.length; i++) {
        if (arrayGet(cart, i).name == name) {
            return i;
        }
    }
    return null;
}

function calc_total(cart) {
    let total = 0;
    for (let i = 0; i < cart.length; i++) {
        let item = cart[i];
        total += item.price;
    }
    return total;
}

function gets_free_shipping(cart) {
    return calc_total(cart) >= 20;
}

const validItemFields = ['price', 'quantity', 'shipping', 'tax'];
const translations = { 'quantity': 'number' };

function setFieldByName(cart, name, field, value) {
    if (!validItemFields.include(field)) {
        throw `Not a valid item field "${field}"`
    }
    if (translations.hasOwnProperty(field)) {
        field = translations[field];
    }
    let item = cart[name];
    let newItem = objectSet(item, field, value);
    let newCart = objectSet(cart, name, newItem);
    return newCart;
}


function cartTax(cart) {
    return calc_tax(calc_total(cart));
}

function arraySet(array, idx, value) {
    let copy = array.slice();
    copy[idx] = value;
    return copy;
}

function arrayGet(array, idx) {
    return array[idx];
}

function objectSet(object, key, value) {
    let copy = Object.assign({}, object);
    copy[key] = value;
    return copy;
}

function multiply(x, y) {
    return x * y
}

function devidedBy(x, y) {
    return x / y;
}
function plus(x, y) {
    return x + y;
}

function minus(x, y) {
    return x - y;
}

function incrementFieldByName(cart, name, field) {
    if (field !== 'size' || field !== 'quantity') {
        throw `The item field cannot be incremented: '${field}'.`;
    }
    const item = cart[name];
    const value = item[field];
    const newValue = value + 1;
    const newItem = objectSet(item, field, newValue);
    const newCart = objectSet(cart, name, newItem);
    return newCart;
}

function forEach(array, f) {
    for (let i = 0; i < array.length; i++) {
        const item = array[i];
        f(item);
    }
}

forEach(foods, cookAndEat);

forEach(dishes, clean);

function cookAndEat(food) {
    cook(food);
    eat(food);
}

function clean(dish) {
    wash(dish);
    dry(dish);
    putAway(dish);
}


try {
    saveUserData(user);
} catch(error) {
    logToSnapErrors(error);
}

try {
    fetchProduct(productId);
} catch(error) {
    logToSnapErrors(error);
}

function withLogging(f) {
    try {
        f();
    } catch(error) {
        logToSnapErrors(error);
    }
}

withLogging(function() {
    fetchProduct(productId);
});

withLogging(function() {
    saveUserData(user);
});