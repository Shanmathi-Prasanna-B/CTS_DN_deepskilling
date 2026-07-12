import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import CourseCard from '../components/CourseCard';
import { courses } from '../data/courses';
import { enroll } from '../store/enrollmentSlice';

function CoursesPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const filtered = courses.filter((c) =>
    c.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleEnroll = (course) => {
    dispatch(enroll(course));
    navigate('/profile');
  };

  return (
    <section>
      <h2>Courses</h2>
      <input
        type="text"
        placeholder="Search courses..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <div className="course-grid">
        {filtered.map((course) => (
          <CourseCard key={course.id} {...course} onEnroll={() => handleEnroll(course)} />
        ))}
      </div>
    </section>
  );
}

export default CoursesPage;
