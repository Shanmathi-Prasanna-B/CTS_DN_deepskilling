<script setup>
import { ref, computed, onMounted } from 'vue';
import CourseCard from '../components/CourseCard.vue';
import { RouterLink } from 'vue-router';
import { useEnrollmentStore } from '../stores/enrollment';

const store = useEnrollmentStore();
const courses = ref([]);
const searchTerm = ref('');

const fallback = [
  { id: 1, name: 'Data Structures', code: 'CS101', credits: 4, grade: 'A' },
  { id: 2, name: 'Database Management', code: 'CS201', credits: 3, grade: 'B+' },
  { id: 3, name: 'Web Development', code: 'CS301', credits: 4, grade: 'A-' },
  { id: 4, name: 'Operating Systems', code: 'CS401', credits: 3, grade: 'B' },
  { id: 5, name: 'Computer Networks', code: 'CS501', credits: 3, grade: 'A' },
];

onMounted(() => {
  courses.value = fallback;
});

const filteredCourses = computed(() =>
  courses.value.filter((c) => c.name.toLowerCase().includes(searchTerm.value.toLowerCase()))
);
</script>

<template>
  <section>
    <h2>Courses</h2>
    <input v-model="searchTerm" placeholder="Search courses..." />
    <div class="course-grid">
      <CourseCard v-for="course in filteredCourses" :key="course.id" v-bind="course">
        <RouterLink :to="`/courses/${course.id}`">View Details</RouterLink>
        <button @click="store.enroll(course)">Enroll</button>
      </CourseCard>
    </div>
  </section>
</template>

<style scoped>
.course-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 20px; }
input { width: 100%; padding: 10px; margin-bottom: 16px; }
button { margin-top: 8px; padding: 8px 16px; background: #1e3a8a; color: #fff; border: none; border-radius: 6px; cursor: pointer; }
</style>
