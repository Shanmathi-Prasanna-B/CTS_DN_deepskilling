import { useState } from 'react';

function StudentProfile() {
  const [profile, setProfile] = useState({ name: '', email: '', semester: '' });

  const handleChange = (field) => (event) => {
    setProfile((prev) => ({ ...prev, [field]: event.target.value }));
  };

  return (
    <section id="profile" className="profile">
      <h2>Student Profile</h2>
      <form>
        <label>
          Name
          <input type="text" value={profile.name} onChange={handleChange('name')} />
        </label>
        <label>
          Email
          <input type="email" value={profile.email} onChange={handleChange('email')} />
        </label>
        <label>
          Semester
          <input type="number" value={profile.semester} onChange={handleChange('semester')} />
        </label>
      </form>
    </section>
  );
}

export default StudentProfile;
