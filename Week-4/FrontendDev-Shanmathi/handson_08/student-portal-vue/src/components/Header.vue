<script setup>
import { storeToRefs } from 'pinia';
import { RouterLink } from 'vue-router';
import { useEnrollmentStore } from '../stores/enrollment';

const store = useEnrollmentStore();
const { enrolledCourses } = storeToRefs(store);
</script>

<template>
  <header class="header">
    <h1>Student Portal</h1>
    <nav>
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/courses">Courses</RouterLink>
      <RouterLink to="/profile">Profile</RouterLink>
    </nav>
    <span>Enrolled: {{ enrolledCourses.length }}</span>
  </header>
</template>

<style scoped>
.header { display: flex; justify-content: space-between; align-items: center; padding: 20px 40px; background: #1e3a8a; color: #fff; }
nav { display: flex; gap: 16px; }
a { color: #fff; text-decoration: none; }
</style>
