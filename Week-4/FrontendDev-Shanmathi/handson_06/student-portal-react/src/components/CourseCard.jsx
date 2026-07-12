import { Link } from 'react-router-dom';

function CourseCard({ id, name, code, credits, grade, onEnroll }) {
  return (
    <article className="course-card">
      <h3><Link to={`/courses/${id}`}>{name}</Link></h3>
      <p>{code}</p>
      <p>{credits} credits</p>
      <p>Grade: {grade}</p>
      <button type="button" onClick={onEnroll}>Enroll</button>
    </article>
  );
}

export default CourseCard;
