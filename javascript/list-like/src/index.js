import { 
  courseRender, likeRender,
} from './view.js';

import {
  bindEvent,
} from './listener.js';

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

function bind(id, eventType, callback) {
  const el = document.getElementById(id);
  el.addEventListener(eventType, callback);
}

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
  bindEvent(courses, bind, update);
}

(() => {
  update();
})();