import { useSelector, useDispatch } from 'react-redux';
import { selectEnrolledCourses } from '../store/store';
import { unenroll } from '../store/enrollmentSlice';

function ProfilePage() {
  const enrolledCourses = useSelector(selectEnrolledCourses);
  const dispatch = useDispatch();

  return (
    <section>
      <h2>My Profile</h2>
      <h3>Enrolled Courses ({enrolledCourses.length})</h3>
      <ul className="enrolled-list">
        {enrolledCourses.map((course) => (
          <li key={course.id}>
            {course.name} ({course.code})
            <button type="button" onClick={() => dispatch(unenroll(course.id))}>Remove</button>
          </li>
        ))}
      </ul>
      {!enrolledCourses.length && <p>No courses enrolled yet.</p>}
    </section>
  );
}

export default ProfilePage;
