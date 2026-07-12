import { useEffect, useState } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import CourseCard from './components/CourseCard';
import StudentProfile from './components/StudentProfile';
import { courses as initialCourses } from './data/courses';

function App() {
  const [courses, setCourses] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [enrolledCourses, setEnrolledCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadCourses() {
      try {
        const response = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=5');
        if (!response.ok) throw new Error('Failed to load courses');
        const posts = await response.json();
        const mapped = posts.map((post, index) => ({
          id: post.id,
          name: initialCourses[index]?.name || post.title,
          code: initialCourses[index]?.code || `CS${post.id}0`,
          credits: initialCourses[index]?.credits || 3,
          grade: initialCourses[index]?.grade || 'B',
        }));
        setCourses(mapped);
      } catch (err) {
        setError(err.message);
        setCourses(initialCourses);
      } finally {
        setLoading(false);
      }
    }
    loadCourses();
  }, []);

  useEffect(() => {
    if (courses.length) {
      console.log('Courses updated');
    }
  }, [courses]);

  const handleEnroll = (course) => {
    setEnrolledCourses((prev) =>
      prev.some((c) => c.id === course.id) ? prev : [...prev, course]
    );
  };

  const filteredCourses = courses.filter((course) =>
    course.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <>
      <Header siteName="Student Portal" enrolledCount={enrolledCourses.length} />
      <main className="container">
        {loading && <p className="loading">Loading...</p>}
        {error && <p className="error">{error}</p>}
        {!loading && (
          <>
            <input
              type="text"
              placeholder="Search courses..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <div className="course-grid">
              {filteredCourses.map((course) => (
                <CourseCard key={course.id} {...course} onEnroll={() => handleEnroll(course)} />
              ))}
            </div>
          </>
        )}
        <StudentProfile />
      </main>
      <Footer />
    </>
  );
}

export default App;
