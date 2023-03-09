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

function setPriceByName(cart, name, price) {
    let i = indexOfItem(cart, name);
    if (i !== null) {
        let item = arrayGet(cart, i);
        return arraySet(cart, i, setPrice(item, price));
    }
    return cart;
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