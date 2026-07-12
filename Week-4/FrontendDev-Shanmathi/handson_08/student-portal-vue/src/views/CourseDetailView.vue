<script setup>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useEnrollmentStore } from '../stores/enrollment';

const route = useRoute();
const router = useRouter();
const store = useEnrollmentStore();

const courses = [
  { id: 1, name: 'Data Structures', code: 'CS101', credits: 4, grade: 'A' },
  { id: 2, name: 'Database Management', code: 'CS201', credits: 3, grade: 'B+' },
  { id: 3, name: 'Web Development', code: 'CS301', credits: 4, grade: 'A-' },
  { id: 4, name: 'Operating Systems', code: 'CS401', credits: 3, grade: 'B' },
  { id: 5, name: 'Computer Networks', code: 'CS501', credits: 3, grade: 'A' },
];

const course = computed(() => courses.find((c) => c.id === Number(route.params.id)));

function handleEnroll() {
  if (course.value) {
    store.enroll(course.value);
    router.push('/profile');
  }
}
</script>

<template>
  <section v-if="course">
    <h2>{{ course.name }}</h2>
    <p>{{ course.code }}</p>
    <p>{{ course.credits }} credits</p>
    <p>Grade: {{ course.grade }}</p>
    <button @click="handleEnroll">Enroll</button>
  </section>
  <p v-else>Course not found</p>
</template>

<style scoped>
button { padding: 8px 16px; background: #1e3a8a; color: #fff; border: none; border-radius: 6px; cursor: pointer; }
</style>
