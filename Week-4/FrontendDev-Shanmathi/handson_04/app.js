import { courses as localCourses } from './data.js';

const API_BASE = 'https://jsonplaceholder.typicode.com';

export async function apiFetch(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}: Failed to fetch ${url}`);
    }
    return response.json();
}

export function fetchUser(id) {
    return fetch(`${API_BASE}/users/${id}`)
        .then((response) => response.json())
        .then((user) => {
            console.log('User (Promise):', user.name);
            return user;
        });
}

export async function fetchUserAsync(id) {
    try {
        const response = await fetch(`${API_BASE}/users/${id}`);
        const user = await response.json();
        console.log('User (async/await):', user.name);
        return user;
    } catch (error) {
        console.error('Fetch user error:', error);
        throw error;
    }
}

export function fetchAllCourses() {
    return new Promise((resolve) => {
        setTimeout(() => resolve(localCourses), 1000);
    });
}

export async function fetchNotifications(useBadUrl = false) {
    const url = useBadUrl ? `${API_BASE}/nonexistent` : `${API_BASE}/posts?_limit=5`;
    return apiFetch(url);
}

export async function fetchUserPosts(userId) {
    const response = await axios.get(`${API_BASE}/posts`, { params: { userId } });
    return response.data;
}

const renderCourseCard = (course) => `
    <article class="course-card">
        <h3>${course.name}</h3>
        <p>${course.code}</p>
        <span>${course.credits} credits</span>
    </article>
`;

const renderNotificationCard = (post) => `
    <article class="notification-card">
        <h3>${post.title}</h3>
        <p>${post.body}</p>
    </article>
`;

const coursesGrid = document.querySelector('#courses-grid');
const coursesLoading = document.querySelector('#courses-loading');
const notificationsSection = document.querySelector('#notifications');
const notificationsLoading = document.querySelector('#notifications-loading');
const notificationsError = document.querySelector('#notifications-error');
const retryBtn = document.querySelector('#retry-notifications');

let useBadUrl = false;

async function loadCourses() {
    coursesLoading.style.display = 'block';
    coursesGrid.innerHTML = '';
    try {
        const courses = await fetchAllCourses();
        coursesGrid.innerHTML = courses.map(renderCourseCard).join('');
    } finally {
        coursesLoading.style.display = 'none';
    }
}

async function loadNotifications() {
    notificationsLoading.style.display = 'block';
    notificationsError.style.display = 'none';
    retryBtn.style.display = 'none';
    notificationsSection.querySelector('.notification-list').innerHTML = '';
    try {
        const posts = await fetchNotifications(useBadUrl);
        notificationsSection.querySelector('.notification-list').innerHTML = posts
            .map(renderNotificationCard)
            .join('');
    } catch (error) {
        notificationsError.textContent = `Unable to load notifications: ${error.message}`;
        notificationsError.style.display = 'block';
        retryBtn.style.display = 'inline-block';
    } finally {
        notificationsLoading.style.display = 'none';
    }
}

fetchUser(1);
fetchUserAsync(1);

Promise.all([fetchUserAsync(1), fetchUserAsync(2)]).then(([user1, user2]) => {
    console.log('Promise.all users:', user1.name, user2.name);
});

loadCourses();
loadNotifications();

retryBtn.addEventListener('click', () => {
    useBadUrl = false;
    loadNotifications();
});

document.querySelector('#simulate-error').addEventListener('click', () => {
    useBadUrl = true;
    loadNotifications();
});

axios.interceptors.request.use((config) => {
    console.log(`API call started: ${config.url}`);
    return config;
});

fetchUserPosts(1).then((posts) => {
    console.log(`User 1 has ${posts.length} posts via Axios`);
});
