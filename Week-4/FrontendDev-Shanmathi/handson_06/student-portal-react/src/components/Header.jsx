import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';

function Header({ siteName }) {
  const enrolledCount = useSelector((state) => state.enrollment.enrolledCourses.length);

  return (
    <header className="header">
      <h1>{siteName}</h1>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/courses">Courses</Link>
        <Link to="/profile">Profile</Link>
      </nav>
      <span className="enrolled-count">Enrolled: {enrolledCount}</span>
    </header>
  );
}

export default Header;
