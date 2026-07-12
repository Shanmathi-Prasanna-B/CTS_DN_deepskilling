import { configureStore } from '@reduxjs/toolkit';
import coursesReducer from './coursesSlice';
import enrollmentReducer from './enrollmentSlice';

export const store = configureStore({
  reducer: {
    courses: coursesReducer,
    enrollment: enrollmentReducer,
  },
});

export const selectCourses = (state) => state.courses.items;
export const selectCoursesLoading = (state) => state.courses.loading;
export const selectCoursesError = (state) => state.courses.error;
export const selectEnrolledCourses = (state) => state.enrollment.enrolledCourses;
