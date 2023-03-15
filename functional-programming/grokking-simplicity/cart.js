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
    return withArrayCopy(array, function (copy) {
        copy[idx] = value;
    });
}

function push(array, elem) {
    return withArrayCopy(array, function (copy) {
        copy.push(elem);
    });
}

function drop_last(array) {
    return withArrayCopy(array, function (copy) {
        copy.pop();
    });
}

function drop_first(array) {
    return withArrayCopy(array, function (copy) {
        copy.shift();
    });
}

function withArrayCopy(array, modify) {
    const copy = array.slice();
    modify(copy);
    return copy;
}

function arrayGet(array, idx) {
    return array[idx];
}

function objectSet(object, key, value) {
    return withObjectCopy(object, function (copy) {
        copy[key] = value;
    });
}

function objectDelete(object, key) {
    return withObjectCopy(object, function (copy) {
        delete copy[key];
    });
}

function withObjectCopy(object, modify) {
    let copy = Object.assign({}, object);
    modify(copy);
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
} catch (error) {
    logToSnapErrors(error);
}

try {
    fetchProduct(productId);
} catch (error) {
    logToSnapErrors(error);
}


function tryCatch(f, errorHandler) {
    try {
        return f();
    } catch (error) {
        return errorHandler(error);
    }
}

function withLogging(f) {
    tryCatch(f, logToSnapErrors);
}

withLogging(function () {
    fetchProduct(productId);
});

withLogging(function () {
    saveUserData(user);
});


function wrapLogging(f) {
    return function (arg) {
        try {
            return f(arg);
        } catch (error) {
            return logToSnapErrors(error);
        }
    };
}

var saveUserDataWithLogging = wrapLogging(saveUserDataNoLogging);

function wrapIgnoreErrors(f) {
    return function (a1, a2, a3) {
        try {
            return f(a1, a2, a3);
        } catch (error) {
            return null;
        }
    };
}

IF(array.length === 0, function () {
    console.log('Array is empty.');
}, function () {
    console.log('Array has something in it.');
});

IF(hasItem(cart, 'shoes'), function () {
    return setPriceByName(cart, 'shoes', 0);
}, function () {
    return cart;
});

function IF(test, then, ELSE) {
    if (test) {
        return then();
    } else {
        return ELSE();
    }
}

function makeAdder(x) {
    return function (y) {
        return x + y;
    };
}

function emailsForCustomers(customers, goods, bests) {
    return map(customers, function (customers) {
        return emailForCustomer(customers, goods, bests);
    });
}

function map(array, f) {
    var newArray = [];
    forEach(array, function (element) {
        newArray.push(f(element));
    });
    return newArray;
}

map(customers, function (customer) {
    return {
        firstName: customer.firstName,
        lastName: customer.lastName,
        address: customer.address,
    };
});

function filter(array, f) {
    var newArray = [];
    forEach(array, function (element) {
        if (f(element)) {
            newArray.push();
        }
    });
    return newArray;
}

function selectBestCustomers(customers) {
    return filter(customers, isGoodCustomer);
}

function isGoodCustomer(customer) {
    return customer.purchases.length >= 3;
}

var testGroup = filter(customers, function (customer) {
    return customer.id % 3 === 0;
});

var nonTestGroup = filter(customers, function (customer) {
    return customer.id % 3 !== 0;
});

function reduce(array, init, f) {
    var accm = init;
    forEach(array, function (element) {
        accm = f(accm, element);
    });
    return accm;
};

function countAllPurchases(customers) {
    return reduce(customers, 0, function (total, customer) {
        return total + customer.puarchase.length;
    });
}

function sum(numbers) {
    return reduce(numbers, 0, function (total, number) {
        return total + number;
    });
}

function product(numbers) {
    return reduce(numbers, 1, function (total, number) {
        return total * number;
    });
}

function min(numbers) {
    return reduce(numbers, Number.MAX_VALUE, function (m, n) {
        if (m > n) {
            return n;
        } else {
            return m;
        }
    });
}



function map2(array, f) {
    return reduce(array, [], function (ret, element) {
        return ret.concat(f[lement]);
    });
}

function filter2(array, f) {
    return reduce(array, [], function (ret, elem) {
        if (f(elem)) {
            return ret.concat([elem]);
        } else {
            return ret;
        }
    });
}


function biggestPurchasesBestCustomers(customers) {
    var bestCustomers = filter(customers, isGoodCustomer);
    var biggestPurchases = map(bestCustomers, getBiggestPurchase);
    return biggestPurchases;
}

function getBiggestPurchases(customers) {
    return max3(customers, getBiggestPurchase);
}

function getBiggestPurchase(customers) {
    return maxKey(customers, { total: 0 }, getPurchaseTotal);
}

function getPurchaseTotal(purchase) {
    return purchase.total;
}

function max(numbers) {
    return reduce(numbers, Number.MIN_VALUE, function (m, n) {
        if (m > n) {
            return m;
        } else {
            return n;
        }
    });
}

function maxKey(array, init, f) {
    return reduce(array, init, function (biggestSoFar, element) {
        if (f(biggestSoFar) > f(element)) {
            return biggestSoFar;
        } else {
            return element;
        }
    });
}

function max3(numbers, init) {
    return maxKey(numbers, init, function (element) {
        return element;
    });
}


var firstTimers = filter(customers, isFirstTimer);

function isFirstTimer(customer) {
    return customer.purchases.length == 1;
}

var firstTimerEmails = map(firstTimers, getCustomerEmail);

function getCustomerEmail(customer) {
    return customer.email;
}

function bigSpenders(customers) {
    var withBigPurchases = filter(customers, hasBigPurchase);
    var with2OrMorePurchases = filter(withBigPurchases, has2OrMorePurchase);
    return with2OrMorePurchases;
}

function hasBigPurchase(customer) {
    return filter(customer.purchases, isBigPurchase);
}

function isBigPurchase(purchase) {
    return purchase.total > 100;
}

function has2OrMorePurchase(customer) {
    return customer.purchases.length >= 2;
}

function average(numbers) {
    return reduce(numbers, 0, plus) / numbers.length;
}

function plus(a, b) {
    return a + b;
}

function averagePurchaseTotals(customers) {
    return map(customers, function (customer) {
        var purchasesTotals = map(customer.purchases, getPurchaseTotal);
        return average(purchasesTotals);
    });
}

var window = 5;
var indices = range(0, array.length);
var windows = map(indices, function(i) {
    return array.slice(i, i + window);
});

var answer = map(windows, average);

function range(start, end) {
    var ret = [];
    for (var i = start; i < end; i++) {
        ret.push(i);
    }
    return ret;
}

function shoesAndSocksInventory(products) {
    var shoesOrShocks = filter(products, function(product) {
        return product.type == 'shoes' || product.type == 'socks';
    });
    var numberInInventories = map(shoesOrShocks, function(product) {
        return product.numberInInventory;
    })
    return reduce(numberInInventories, 0, plus);
}

var evaluations = [
    { name: 'Jane', position: 'catcher', score: 25 },
    { name: 'John', position: 'pitcher', score: 10 },
    { name: 'Harray', position: 'catcher', score: 3 },
];

var roster = reduce(evaluations, {}, function(roster, evaluation) {
    var position = roster[evaluation.position];
    if (roster[position]) {
        return roster;
    } else {
        return objectSet(roster, position, evaluation.name);
    }
});


var recommendations = map(employeeNames, function(name) {
    return {
        name: name,
        position: recommendPosition(name),
    };
});

var evaluations = map(recommendations, function(rec) {
    return objectSet(
        rec, 
        'score', 
        scorePlayer(rec.name, rec.position)
    );
});


var evaluationAscending = sortBy(evaluations, function(eval) {
    return eval.score;
});

var evaluationDescending = reverse(evaluationAscending);

function updateFiled(item, field, modify) {
    var value = item[field];
    var newValue = modify(value);
    var newItem = objectSet(item, field, newValue);
    return newItem;
}

function update(object, key, modify) {
    var value = object[key];
    var newValue = modify(value);
    var newObject = objectSet(object, key, newValue);
    return newObject;
}

var employee = {
    name: 'Kim',
    salary: 12000
};

function raise10Percent(salary) {
    return salary * 1.1;
}

var result = update(employee, 'salary', raise10Percent);


/**
 * p364. 연습문제
 */
var user = {
    firstName: "Joe",
    lastName: "Nash",
    email: "JOE@EXAMPLE.COM",
};

update(user, 'email', function(element) {
    return element.toLowerCase();
});

var item = {
    quantity: 2,
};

function tenXQuantity(item) {
    return update(item, 'quantity', function(quantity) {
        return quantity * 10;
    });
}

function update2(object, key1, key2, modify) {
    return update(object, key1, function(value1) {
        return update(value1, key2, modify);
    });
}

function incrementSize(item) {
    return update2(item, 'options', 'size', function(size) {
        return size + 1;
    });
}

function incrementSizeByName(cart, name) {
    return update(cart, name, function(item) {
        return update2(item, 'options', 'size', function(size) {
            return size + 1;
        });
    });
}

function update3(object, key1, key2, key3, modify) {
    return update(object, key1, function(object2) {
        return update2(object2, key2, key3, modify);
    });
}

function update4(object, k1, k2, k3, k4, modify) {
    return update(object, key1, function(object2) {
        return update3(object2, k2, k3, k4, modify);
    });
}

function update5(object, k1, k2, k3, k4, k5, modify) {
    return update(object, key1, function(object2) {
        return update4(object2, k2, k3, k4, k5, modify);
    });
}

function nestedUpdate(object, keys, modify) {
    if (keys.length == 0) {
        return modify(object);
    }
    var key1 = keys[0];
    var restOfKey = drop_first(keys);
    return update(object, key1, function(object2) {
        return nestedUpdate(object2, restOfKey, modify);
    })
}

function incrementSizeByName2(cart, name) {
    return nestedUpdate(cart, [name, 'option', 'size'], function(size) {
        return size + 1;
    });
}