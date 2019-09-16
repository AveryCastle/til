const log = console.log;

const curry = (f) => (a, ...args) => args.length ? f(a, ...args) : (...args) => f(a, ...args);

const reduce = curry((fn, acc, iter) => {
  if (!iter) {
    iter = acc[Symbol.iterator]();
    acc = iter.next().value;
  }
  for (const v of iter) {
    acc = fn(acc, v);
  }
  return acc;
});

const go = (...args) => reduce((a, f) => f(a), args);
