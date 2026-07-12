import apiClient from './apiClient';

const fallback = [
  { id: 1, name: 'Data Structures', code: 'CS101', credits: 4, grade: 'A' },
  { id: 2, name: 'Database Management', code: 'CS201', credits: 3, grade: 'B+' },
  { id: 3, name: 'Web Development', code: 'CS301', credits: 4, grade: 'A-' },
  { id: 4, name: 'Operating Systems', code: 'CS401', credits: 3, grade: 'B' },
  { id: 5, name: 'Computer Networks', code: 'CS501', credits: 3, grade: 'A' },
];

function mapPosts(posts) {
  return posts.map((post, i) => ({
    id: post.id,
    name: fallback[i]?.name || post.title,
    code: fallback[i]?.code || `CS${post.id}`,
    credits: fallback[i]?.credits || 3,
    grade: fallback[i]?.grade || 'B',
  }));
}

export async function getAllCourses() {
  const posts = await apiClient.get('/posts', { params: { _limit: 5 } });
  return mapPosts(posts);
}

export async function getCourseById(id) {
  const post = await apiClient.get(`/posts/${id}`);
  const index = Number(id) - 1;
  return {
    id: post.id,
    name: fallback[index]?.name || post.title,
    code: fallback[index]?.code || `CS${post.id}`,
    credits: fallback[index]?.credits || 3,
    grade: fallback[index]?.grade || 'B',
  };
}

export async function enrollStudent(studentId, courseId) {
  return apiClient.post('/posts', { studentId, courseId, title: 'Enrollment' });
}
