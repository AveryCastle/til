import { addTask, removeTask, toggleTask } from '../functions';
import { getTasks } from '../apis/task';
import Counter from '../utils/counter';

export default {
  async fetchTasks({ commit }) {
    const tasks = await getTasks();
    const maxId = Math.max(0, ...tasks.map(task => task.id));
    commit('setCounter', Counter(maxId + 1));
    commit('setTasks', tasks.slice(0, 10));
  },
  addTask({ commit, state }) {
    const { taskTitle: title } = state;
    const { tasks } = addTask(state, title);
    commit('setTasks', tasks);
    commit('setTaskTitle', '');
  },
  updateTaskTitle({ commit }, title) {
    commit('setTaskTitle', title);
  },
  removeTask({ commit, state }, id) {
    const { tasks } = removeTask(state, id);
    commit('setTasks', tasks);
  },
  toggleTask({ commit, state }, id) {
    const { tasks } = toggleTask(state, id);
    commit('setTasks', tasks);
  }
}