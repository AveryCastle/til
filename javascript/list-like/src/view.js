export function courseRender(courses) {
  return `
    <ul>
      ${courses.map(course => `
        <li>
          ${ course.title }
          <button type="button" id="btn-like-${ course.id }">${ course.like ? '찜 해제' : '찜하기' }</button>
        </li>
      `
      ).join('')}
    </ul>
  `;
}

export function likeRender(courses) {
  return `
    ${courses.filter(course => course.like)
              .map(course => `
              <li>${course.title}</li>
              `).join('')}
  `;
}