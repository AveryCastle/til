import { bindEvents } from './listener';

test('bind', () => {
  const events = {};

  const bind = (id, eventType, callback) => {
    events[`${id}.${eventType}`] = callback;
  };

  const update = () => {};

  const state = {
    tasks: [
      { id: 1, title: 'Sleep' },
      { id: 2, title: 'Wake up' },
    ],
  };

  bindEvents(state, { bind, update });

  expect(events['button-add-task.click']).toBeTruthy();
  expect(events['button-remove-task-1.click']).toBeTruthy();
  expect(events['checkbox-task-1.click']).toBeTruthy();
});