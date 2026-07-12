import { ref, computed } from 'vue';
import { defineStore } from 'pinia';

export const useEnrollmentStore = defineStore('enrollment', () => {
  const enrolledCourses = ref([]);

  const totalCredits = computed(() =>
    enrolledCourses.value.reduce((sum, c) => sum + c.credits, 0)
  );

  function enroll(course) {
    if (!enrolledCourses.value.some((c) => c.id === course.id)) {
      enrolledCourses.value.push(course);
    }
  }

  function unenroll(courseId) {
    enrolledCourses.value = enrolledCourses.value.filter((c) => c.id !== courseId);
  }

  function $reset() {
    enrolledCourses.value = [];
  }

  return { enrolledCourses, totalCredits, enroll, unenroll, $reset };
});
