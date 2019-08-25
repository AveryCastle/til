import { add, add1 } from './calculator';

test('add', () => {
  expect(add(1, 2)).toBe(3);
  expect(add(10, 20)).toBe(30);
  expect(add(1, undefined)).toBe(1);
  expect(add(null, 10)).toBe(10);
  expect(add(null, undefined)).toBe(0);
  expect(add1(1, 2, 3, 4, 5)).toBe(15);
  expect(add1(1, 2, 3, 4, undefined)).toBe(10);
  expect(add1(null, 2, 3, 4, undefined)).toBe(9);
});