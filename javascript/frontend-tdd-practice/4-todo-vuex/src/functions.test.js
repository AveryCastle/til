import { 
  addTask, 
  removeTask,
} from './functions';

test('addTask', () => {
  const state = {
    counter: () => 100,
    tasks: [],
  };

  const { tasks } = addTask(state, 'Hello');

  expect(tasks).toEqual([
    { id: 100, title: 'Hello', completed: false },
  ]);
});