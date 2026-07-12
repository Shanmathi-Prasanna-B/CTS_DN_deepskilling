function CourseCard({ name, code, credits, grade, onEnroll }) {
  return (
    <article className="course-card">
      <h3>{name}</h3>
      <p>{code}</p>
      <p>{credits} credits</p>
      <p>Grade: {grade}</p>
      <button type="button" onClick={onEnroll}>Enroll</button>
    </article>
  );
}

export default CourseCard;
