export const render = ({ tasks }) => {
  return `
    <div>
      <ul>
      ${tasks.map(task =>`
        <li>
          ${task.title}   
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