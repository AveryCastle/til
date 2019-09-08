jest.mock('./utils/counter');
jest.mock('./apis/task');

import { setMockCount } from './utils/counter';
import { setMockTasks } from './apis/task';

import {
  clearTasks,
  fetchTasks,
  getTasks,
  addTask,
  removeTask,
} from './services';

beforeEach(() => {
  setMockCount(100);

  clearTasks();
});

test('clearTasks', () => {
  clearTasks();

  expect(getTasks()).toEqual([]);
});

test('fetchTasks', async () => {
  setMockTasks([
    { id: 100, title: 'hello', completed: false }
  ]);

  const tasks = await fetchTasks();

  expect(tasks).toEqual([
    { id: 100, title: 'hello', completed: false }
  ]);
});

test('addTask', () => {
  const tasks = addTask('hello');

  expect(tasks).toEqual([
    { id: 100, title: 'hello', completed: false }
  ]);
});

test('removeTask', () => {
  setMockTasks([
    { id: 100, title: 'hello', completed: false }
  ]);
  
  const tasks = removeTask(100);

  expect(tasks).toEqual([]);
});