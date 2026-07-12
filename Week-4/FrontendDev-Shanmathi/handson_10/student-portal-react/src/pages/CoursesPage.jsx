import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import CourseCard from '../components/CourseCard';
import { fetchAllCourses } from '../store/coursesSlice';
import {
  selectCourses,
  selectCoursesLoading,
  selectCoursesError,
} from '../store/store';
import { enroll } from '../store/enrollmentSlice';

function CoursesPage() {
  const dispatch = useDispatch();
  const courses = useSelector(selectCourses);
  const loading = useSelector(selectCoursesLoading);
  const error = useSelector(selectCoursesError);
  const [searchTerm, setSearchTerm] = useState('');
  const [useBadUrl, setUseBadUrl] = useState(false);

  useEffect(() => {
    dispatch(fetchAllCourses());
  }, [dispatch, useBadUrl]);

  const filtered = courses.filter((c) =>
    c.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <section>
      <h2>Courses</h2>
      <input
        type="text"
        placeholder="Search courses..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      {loading && <p className="loading">Loading courses...</p>}
      {error && (
        <div className="error">
          <p>{error}</p>
          <button type="button" onClick={() => { setUseBadUrl(false); dispatch(fetchAllCourses()); }}>
            Retry
          </button>
        </div>
      )}
      <div className="course-grid">
        {filtered.map((course) => (
          <CourseCard
            key={course.id}
            {...course}
            onEnroll={() => dispatch(enroll(course))}
          />
        ))}
      </div>
    </section>
  );
}

export default CoursesPage;
