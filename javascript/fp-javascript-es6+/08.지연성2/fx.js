const log = console.log;

const curry = (fn) => (a, ...args) => args.length ? fn(a, ...args) : (...args) => fn(a, ...args);

const map = curry((fn, iter) => {
  const res = [];
  for (const a of iter) {
    res.push(fn(a));
  }
  return res;
});

const filter = curry((fn, iter) => {
  const res = [];
  for (const a of iter) {
    if (fn(a)) {
      res.push(a);
    }
  }
  return res;
});

const L = {};

L.range = function *(limit) {
  let i = -1;
  while (++i < limit) {
    yield i;
  }
};

L.map = curry(function *(fn, iter) {
  iter = iter[Symbol.iterator]();
  let cur;
  while (!(cur = iter.next()).done) {
    const a = cur.value;
    yield fn(a);
  }
  // for (const a of iter) yield fn(a);
});

L.filter = curry(function *(fn, iter) {
  iter = iter[Symbol.iterator]();
  let cur;
  while (!(cur = iter.next()).done) {
    const a = cur.value;
    if (fn(a)) {
      yield a;
    }
  }
  // === equivalent for for (...)
  // for (const a of iter) {
  //   if (fn(a)) {
  //     yield a;
  //   }
  // }
});

const take = curry((limit, iter) => {
  const res = [];
  iter = iter[Symbol.iterator]();
  let cur;
  while (!(cur = iter.next()).done) {
    if (res.length < limit) {
      const a = cur.value;
      res.push(a);
    } else {
      return res;
    }
  }
  // for (const a of iter) {
  //   if (res.length < limit) {
  //     res.push(a);
  //   } else {
  //     return res;
  //   }
  // }
});

const reduce = curry((fn, acc, iter) => {
  if (iter) {
    iter = iter[Symbol.iterator]();
  } else {
    iter = acc[Symbol.iterator]();
    acc = iter.next().value;
  }

  let cur;
  while (!(cur = iter.next()).done) {
    const a = cur.value;
    acc = fn (acc, a);
  }
  // for (const a of iter) {
  //   acc = fn(acc, a);
  // }
  return acc;
});

const go = (...args) => reduce((a, fn) => fn(a), args);

const pipe = (...fns) => (initial) => go(initial, ...fns);