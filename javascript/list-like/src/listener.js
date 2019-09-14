export function bindEvent(courses, bind, callback) {
  toggleLike(courses, bind, callback);
}

function toggleLike(courses, bind, callback) {
  courses.forEach(course => {
    const id = course.id;
    bind(`btn-like-${id}`, 'click', () => {
      course.like = !course.like;
      callback();
    })
  });
}