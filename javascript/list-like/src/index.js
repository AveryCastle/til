const courses = [
  {
    id: 1,
    title: 'ios',
    like: false,
  },
  {
    id: 2,
    title: 'android',
    like: false,
  },
  {
    id: 3,
    title: 'java',
    like: false,
  },
  {
    id: 4,
    title: 'javascript',
    like: true,
  },
  {
    id: 5,
    title: 'node.js',
    like: false,
  },
  {
    id: 6,
    title: 'python',
    like: false,
  }
];

function getCourses() {
  return courses;
}

function fetchCourses() {
  const courses = getCourses();

  const el = document.querySelector('.blogList');
  el.innerHTML = courseRender(courses);
}

function fetchLikeCourses() {
  const courses = getCourses();

  const el = document.querySelector('.like-list');
  el.innerHTML = likeRender(courses);
}

function update() {
  fetchCourses();
  fetchLikeCourses();
  bindEvent(courses, update);
}

function courseRender(courses) {
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

function likeRender(courses) {
  return `
    ${courses.filter(course => course.like)
              .map(course => `
              <li>${course.title}</li>
              `).join('')}
  `;
}

function bindEvent(courses, callback) {
  toggleLike(courses, callback);
}

function toggleLike(courses, callback) {
  courses.forEach(course => {
    const id = course.id;
    const el = document.getElementById(`btn-like-${id}`);
    el.addEventListener('click', () => {
      course.like = !course.like;
      callback();
    });
  });
}

(() => {
  update();
})();