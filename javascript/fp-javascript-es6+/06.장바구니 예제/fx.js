const log = console.log;

const curry = (f) => (a, ..._) => _.length? f(a, ..._) : (..._) => f(a, ..._);

const map = curry((f, iter) => {
  const res = [];
  for (const element of iter) {
    res.push(f(element));
  }
  return res;
});

const filter = curry((f, iter) => {
  const res = [];
  for (const element of iter) {
    if (f(element)) {
      res.push(element);
    }
  }
  return res;
});

const reduce = curry((f, acc, iter) => {
  if (!iter) {
    iter = acc[Symbol.iterator]();
    acc = iter.next().value;
  }
  for (const element of iter) {
    acc = f(acc, element);
  }

  return acc;
});

const go = (...args) => reduce((a, f) => f(a), args);

const pipe = (f, ...fs) => (...args) => go(f(...args), ...fs);