jest.mock('./utils/counter');
jest.mock('./apis/task');

import { setMockCount } from './utils/counter';
import { setMockTasks } from './apis/task';
import { clearTask, getTasks, fetchTasks, addTask } from './service';

beforeEach(() => {
  setMockCount(1);

  clearTask();
});

test('clearTasks', () => {
  expect(getTasks()).toEqual([]);
});

test('fetchTasks', async () => {
  setMockTasks([
    { id: 1, title: 'TDD Practice' },
  ]);

  const tasks = await fetchTasks();

  expect(tasks).toEqual([
    { id: 1, title: 'TDD Practice' },
  ]);
});

test('addTask', () => {
  const tasks = addTask('FP');

  expect(tasks).toEqual([
    { id: 1, title: 'FP' },
  ]);
});