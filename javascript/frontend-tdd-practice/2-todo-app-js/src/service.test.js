jest.mock('./utils/counter');
jest.mock('./apis/task');

import { setMockCount } from './utils/counter';
import { setMockTasks } from './apis/task';
import { 
  clearTask, 
  getTasks, 
  fetchTasks, 
  addTask,
  removeTask,
  toggleTask,
} from './service';

beforeEach(() => {
  setMockCount(1);

  clearTask();
});

test('clearTasks', () => {
  expect(getTasks()).toEqual([]);
});

test('fetchTasks', async () => {
  setMockTasks([
    { id: 1, title: 'TDD Practice', completed: false },
  ]);

  const tasks = await fetchTasks();

  expect(tasks).toEqual([
    { id: 1, title: 'TDD Practice', completed: false },
  ]);
});

test('addTask', () => {
  const tasks = addTask('FP');

  expect(tasks).toEqual([
    { id: 1, title: 'FP', completed: false },
  ]);
});

test('removeTask', () => {
  addTask('Hello');

  const tasks = removeTask(1);
  expect(tasks).toEqual([]);
});

test('toggleTask', () => {
  addTask('Hello');

  const tasks = toggleTask(1);
  
  expect(tasks).toEqual([{ id: 1, title: 'Hello', completed: true }]);
});