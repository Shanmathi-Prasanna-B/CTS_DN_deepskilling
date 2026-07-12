import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { courses } from '../data/courses';
import { enroll } from '../store/enrollmentSlice';

function CourseDetailPage() {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const course = courses.find((c) => c.id === Number(courseId));

  if (!course) {
    return <p>Course not found</p>;
  }

  const handleEnroll = () => {
    dispatch(enroll(course));
    navigate('/profile');
  };

  return (
    <section className="course-detail">
      <h2>{course.name}</h2>
      <p>Code: {course.code}</p>
      <p>Credits: {course.credits}</p>
      <p>Grade: {course.grade}</p>
      <button type="button" onClick={handleEnroll}>Enroll</button>
    </section>
  );
}

export default CourseDetailPage;
