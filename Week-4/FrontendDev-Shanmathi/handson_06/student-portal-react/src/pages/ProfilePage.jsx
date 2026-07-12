import { useSelector, useDispatch } from 'react-redux';
import { unenroll } from '../store/enrollmentSlice';

function ProfilePage() {
  const enrolledCourses = useSelector((state) => state.enrollment.enrolledCourses);
  const dispatch = useDispatch();

  return (
    <section>
      <h2>My Profile</h2>
      <h3>Enrolled Courses ({enrolledCourses.length})</h3>
      {enrolledCourses.length === 0 ? (
        <p>No courses enrolled yet.</p>
      ) : (
        <ul className="enrolled-list">
          {enrolledCourses.map((course) => (
            <li key={course.id}>
              {course.name} ({course.code})
              <button type="button" onClick={() => dispatch(unenroll(course.id))}>
                Remove
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export default ProfilePage;
