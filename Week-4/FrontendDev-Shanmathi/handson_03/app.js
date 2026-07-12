import { courses as courseData } from './data.js';

const formattedCourses = courseData.map(
    (course) => `${course.code} — ${course.name} (${course.credits} credits)`
);
console.log('Formatted courses:', formattedCourses);

const highCreditCourses = courseData.filter((course) => course.credits >= 4);
console.log('Courses with 4+ credits:', highCreditCourses.length);

const totalCredits = courseData.reduce((sum, course) => sum + course.credits, 0);
console.log('Total credits:', totalCredits);

const renderCourseCard = (course) => {
    const article = document.createElement('article');
    article.className = 'course-card';
    article.dataset.id = course.id;
    article.tabIndex = 0;
    article.innerHTML = `
        <h3>${course.name}</h3>
        <p>${course.code}</p>
        <span>${course.credits} credits</span>
        <span class="grade">Grade: ${course.grade}</span>
    `;
    return article;
};

const renderCourses = (coursesToRender) => {
    const grid = document.querySelector('.course-grid');
    grid.innerHTML = '';
    const fragment = document.createDocumentFragment();
    coursesToRender.forEach((course) => {
        fragment.appendChild(renderCourseCard(course));
    });
    grid.appendChild(fragment);
    document.querySelector('#total-credits').textContent = `Total Credits: ${coursesToRender.reduce(
        (sum, c) => sum + c.credits,
        0
    )}`;
    document.querySelector('#results-count').textContent = `${coursesToRender.length} courses found`;
};

let currentCourses = [...courseData];
renderCourses(currentCourses);

document.querySelector('#search-courses').addEventListener('input', (event) => {
    const term = event.target.value.toLowerCase();
    currentCourses = courseData.filter((course) => course.name.toLowerCase().includes(term));
    renderCourses(currentCourses);
});

document.querySelector('#sort-credits').addEventListener('click', () => {
    currentCourses = [...currentCourses].sort((a, b) => b.credits - a.credits);
    renderCourses(currentCourses);
});

document.querySelector('.course-grid').addEventListener('click', (event) => {
    const card = event.target.closest('.course-card');
    if (!card) return;
    const course = courseData.find((c) => c.id === Number(card.dataset.id));
    if (course) {
        document.querySelector('#selected-course').textContent = `${course.name} — Grade: ${course.grade}`;
    }
});

document.querySelector('.course-grid').addEventListener('keydown', (event) => {
    if (event.key !== 'Enter') return;
    const card = event.target.closest('.course-card');
    if (!card) return;
    const course = courseData.find((c) => c.id === Number(card.dataset.id));
    if (course) {
        document.querySelector('#selected-course').textContent = `${course.name} — Grade: ${course.grade}`;
    }
});
