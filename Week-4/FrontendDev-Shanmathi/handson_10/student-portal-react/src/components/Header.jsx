import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { selectEnrolledCourses } from '../store/store';

function Header() {
  const enrolledCourses = useSelector(selectEnrolledCourses);

  return (
    <header className="header">
      <h1>Student Portal</h1>
      <nav>
        <Link to="/">Courses</Link>
        <Link to="/profile">Profile</Link>
      </nav>
      <span>Enrolled: {enrolledCourses.length}</span>
    </header>
  );
}

export default Header;
