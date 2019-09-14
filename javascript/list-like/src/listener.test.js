import { bindEvent } from './listener.js';

test('bindEvent', () => {
  const events = {};

  const courses = [
    {
      id: 1,
      title: 'hello',
      like: true,
    }
  ];

  const update = () => {};
  const bind = (id, eventType, callback) => {
    events[`${id}.${eventType}`] = callback;
  };
  
  bindEvent(courses, bind, update);
  
  expect(events['btn-like-1.click']).toBeTruthy();
});