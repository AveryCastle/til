import { getTasks as apiGetTasks } from './apis/task';
import Counter from './utils/counter';

const state = {
  counter:  Counter(),
  tasks: [],
};

export const clearTask = () => {
  state.tasks = [];
}

export const fetchTasks = async () => {
  const tasks = await apiGetTasks();
  const maxId = Math.max(0, ...tasks.map(task => task.id));
  state.counter = Counter(maxId);
  state.tasks = tasks;
  return state.tasks;
}

export const getTasks = () => {
  return state.tasks;
}

export const addTask = title => {
  const { counter } = state;
  state.tasks = [
    ...state.tasks,
    { id: counter(), title, completed: false }
  ];

  return state.tasks;
}

export const removeTask = id => {
  state.tasks = state.tasks.filter(task => task.id !== id);
  return state.tasks;
}

export const toggleTask = id => {
  state.tasks.forEach(task => {
    if (task.id === id) {
      task.completed = !task.completed;
    }
  });

  return state.tasks;
}