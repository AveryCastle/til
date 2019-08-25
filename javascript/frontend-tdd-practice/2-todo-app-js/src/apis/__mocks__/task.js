let mockTasks = [];

export const setMockTasks = tasks => {
  mockTasks = tasks;
};

export const getTasks = async () => {
  return mockTasks;
}