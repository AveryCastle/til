import { addTask } from './service';

export const bindEvents = (state, methods) => {
  bindAddTask(state, methods);
};

const bindAddTask = (state, { bind, getValue, update }) => {
  bind('button-add-task', 'click', () => {
    const title = getValue('input-task-title');
    addTask(title);
    update();
  });
};