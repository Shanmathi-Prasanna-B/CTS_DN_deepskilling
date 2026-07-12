import { courses as courseData } from './data.js';

const renderCourseCard = (course) => {
    const article = document.createElement('article');
    article.className = 'course-card';
    article.dataset.id = course.id;
    article.tabIndex = 0;
    article.setAttribute('role', 'button');
    article.setAttribute('aria-label', `View details for ${course.name}`);
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
        (sum, c) => sum + c.credits, 0
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

const showCourseDetails = (card) => {
    const course = courseData.find((c) => c.id === Number(card.dataset.id));
    if (course) {
        document.querySelector('#selected-course').textContent = `${course.name} — Grade: ${course.grade}`;
    }
};

document.querySelector('.course-grid').addEventListener('click', (event) => {
    const card = event.target.closest('.course-card');
    if (card) showCourseDetails(card);
});

document.querySelector('.course-grid').addEventListener('keydown', (event) => {
    if (event.key !== 'Enter' && event.key !== ' ') return;
    const card = event.target.closest('.course-card');
    if (card) {
        event.preventDefault();
        showCourseDetails(card);
    }
});

const navToggle = document.querySelector('.nav-toggle');
const mainNav = document.querySelector('.main-nav');

navToggle.addEventListener('click', () => {
    const expanded = navToggle.getAttribute('aria-expanded') === 'true';
    navToggle.setAttribute('aria-expanded', String(!expanded));
    mainNav.classList.toggle('open');
});

document.querySelectorAll('.main-nav a').forEach((link) => {
    link.addEventListener('click', () => {
        document.querySelectorAll('.main-nav a').forEach((l) => l.removeAttribute('aria-current'));
        link.setAttribute('aria-current', 'page');
    });
});

document.querySelector('.main-nav a[href="#hero-section"]').setAttribute('aria-current', 'page');
