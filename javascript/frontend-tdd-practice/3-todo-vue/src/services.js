import { getTasks as apiGetTasks } from './apis/task';
import Counter from './utils/counter';

const state = {
  tasks: [],
  counter: Counter(),
};

const clearTasks = () => {
  state.tasks = [];
};

const fetchTasks = async () => {
  const tasks = await apiGetTasks();
  const maxId = Math.max(0, ...tasks.map(task => task.id));
  state.counter = Counter(maxId);
  state.tasks = tasks.slice(0, 10);
  return state.tasks;
}

const getTasks = () => {
  return state.tasks;
}

const addTask = (title) => {
  const { counter } = state;

  state.tasks = [
    ...state.tasks,
    { id: counter(), title, completed: false }
  ];

  return state.tasks;
}

const removeTask = (id) => {
  const { tasks } = state;

  state.tasks = tasks.filter(task => task.id !== id);

  return state.tasks;
}

export {
  clearTasks,
  fetchTasks,
  getTasks,
  addTask,
  removeTask,
};