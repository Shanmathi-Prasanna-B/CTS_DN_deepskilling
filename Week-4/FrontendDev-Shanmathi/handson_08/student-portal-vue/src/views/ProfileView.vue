<script setup>
import { storeToRefs } from 'pinia';
import { useEnrollmentStore } from '../stores/enrollment';

const store = useEnrollmentStore();
const { enrolledCourses, totalCredits } = storeToRefs(store);
</script>

<template>
  <section>
    <h2>My Profile</h2>
    <p>Total Credits: {{ totalCredits }}</p>
    <ul>
      <li v-for="course in enrolledCourses" :key="course.id">
        {{ course.name }} ({{ course.code }})
        <button @click="store.unenroll(course.id)">Remove</button>
      </li>
    </ul>
    <p v-if="!enrolledCourses.length">No courses enrolled.</p>
  </section>
</template>

<style scoped>
ul { list-style: none; padding: 0; }
li { display: flex; justify-content: space-between; padding: 12px; background: #fff; margin-bottom: 8px; border-radius: 6px; }
button { padding: 4px 12px; background: #991b1b; color: #fff; border: none; border-radius: 4px; cursor: pointer; }
</style>
