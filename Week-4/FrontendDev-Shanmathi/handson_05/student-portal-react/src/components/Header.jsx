function Header({ siteName, enrolledCount }) {
  return (
    <header className="header">
      <h1>{siteName}</h1>
      <nav>
        <a href="#home">Home</a>
        <a href="#courses">Courses</a>
        <a href="#profile">Profile</a>
      </nav>
      <span className="enrolled-count">Enrolled: {enrolledCount}</span>
    </header>
  );
}

export default Header;
