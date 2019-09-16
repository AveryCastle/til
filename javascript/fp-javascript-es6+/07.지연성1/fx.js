const log = console.log;

const reduce = (fn, acc, iter) => {
  if (!iter) {
    iter = acc[Symbol.iterator]();
    acc = iter.next().value;
  }
  for (const v of iter) {
    acc = fn(acc, v);
  }
  return acc;
};