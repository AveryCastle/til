const log = console.log;

const map = (fn, iter) => {
  const res = [];
  
  for(const element of iter) {
    res.push(fn(element));
  }

  return res;
};

const filter = (fn, iter) => {
  const res = [];
  for (const element of iter) {
    if (fn(element)) {
      res.push(element);
    }
  }
  return res;
};

const reduce = (fn, acc, iter) => {
  if (!iter) {
    iter = acc[Symbol.iterator]();
    acc = iter.next().value;
  }

  for (const element of iter) {
    acc = fn(acc, element);
  }
  return acc;
};

// curry --------------------------
const curry2 = f => (a, ..._) => _.length ? f(a, ..._) : (..._) => f(a, ..._);

const map2 = curry2((fn, iter) => {
  const res = [];
  
  for(const element of iter) {
    res.push(fn(element));
  }

  return res;
});

const filter2 = curry2((fn, iter) => {
  const res = [];
  for (const element of iter) {
    if (fn(element)) {
      res.push(element);
    }
  }
  return res;
});

const reduce2 = curry2((fn, acc, iter) => {
  if (!iter) {
    iter = acc[Symbol.iterator]();
    acc = iter.next().value;
  }

  for (const element of iter) {
    acc = fn(acc, element);
  }
  return acc;
});