import Counter from './counter';

test('counter', () => {
  const counter = Counter(100);

  expect(counter()).toBe(100);
  expect(counter()).toBe(101);
  expect(counter()).toBe(102);
});