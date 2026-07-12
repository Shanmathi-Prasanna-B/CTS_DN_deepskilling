<script setup>
defineProps({
  name: String,
  code: String,
  credits: Number,
  grade: String,
});
</script>

<template>
  <article class="course-card">
    <h3>{{ name }}</h3>
    <p>{{ code }}</p>
    <p>{{ credits }} credits</p>
    <p>Grade: {{ grade }}</p>
    <slot />
  </article>
</template>

<style scoped>
.course-card { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
</style>
