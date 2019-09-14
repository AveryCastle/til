import { courseRender, likeRender } from './view';

test('courseRender', () => {
  const courses = [
    {
      id: 1,
      title: 'hello',
      like: true
    }
  ];
  
  const renderedView = courseRender(courses);
  expect(renderedView).toMatch(/찜 해제/);
});

test('likeRender', () => {
  const courses = [
    {
      id: 1,
      title: 'hello',
      like: true
    },
    {
      id: 2,
      title: 'bye',
      like: false
    }
  ];

  const renderedView = likeRender(courses);
  expect(renderedView).toMatch(/hello/);
  expect(renderedView).not.toMatch(/bye/);
});