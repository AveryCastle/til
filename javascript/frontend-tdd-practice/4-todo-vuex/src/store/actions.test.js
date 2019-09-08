jest.mock('../apis/task');

import { setMockTasks } from '../apis/task';

import actions from './actions';

const {
  addTask,
} = actions;

test('addTask', () => {
  const commit = jest.fn();
  const state = {
    counter: () => 100,
    tasks: [],
    taskTitle: 'Hello',
  };

  addTask({ commit, state });

  expect(commit.mock.calls[0][0]).toBe('setTasks');
  expect(commit.mock.calls[0][1]).toHaveLength(1);

  expect(commit.mock.calls[1]).toEqual(['setTaskTitle', '']);
  
})