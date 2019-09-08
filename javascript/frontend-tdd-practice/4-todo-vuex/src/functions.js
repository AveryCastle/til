export const addTask = (state, title) => {
  const { counter, tasks } = state;
  return {
    ...state,
    tasks: [...tasks, { id: counter(), title, completed: false }],
  };
};

export const removeTask = (state, id) => {
  const { tasks } = state;
  return {
    ...state,
    tasks: tasks.filter(task => task.id !== id),
  };
};

export const toggleTask = (state, id) => {
  const { tasks } = state;
  return {
    ...state,
    tasks: tasks.map(task =>
      task.id !== id ? task : { ...task, completed: !task.completed }
    ),
  };
};