import { render } from './view';

test('render', () => {
  const state = {
    tasks: [
      { id: 1, title: 'Sleep' },
      { id: 2, title: 'Wake Up' },
    ],
  };
  const html = render(state);

  expect(html).toMatch('<ul>');
  expect(html).toMatch('Sleep');
  expect(html).toMatch('Wake Up');
  expect(html).toMatch('Add');
});