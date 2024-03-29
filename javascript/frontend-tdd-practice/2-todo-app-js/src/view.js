export const render = ({ tasks }) => {
  return `
    <div>
      <ul>
      ${tasks.map(task =>`
        <li>
        <input type="checkbox"
            id="checkbox-task-${task.id}"
            ${task.completed ? 'checked' : ''}
            />
          ${task.title}   
          ${task.completed ? '[DONE]' : ''}
          <button type="button"
                  id="button-remove-task-${task.id}">
          Remove
          </button>
        </li>
      `).join('')}
      </ul>
    </div>
    <div>
      <input type="text" id="input-task-title">
      <button type="button" id="button-add-task">Add</button>
    </div>
  `;
};