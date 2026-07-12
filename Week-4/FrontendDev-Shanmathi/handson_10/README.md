# Handson 10 - State Management Framework Comparison

## React + Redux Toolkit
Uses createSlice and createAsyncThunk for async API calls. Components dispatch actions and read state via useSelector. Redux DevTools provides time-travel debugging. More boilerplate than Context but scales well for large apps.

## Angular + NgRx
Follows the same Redux pattern with Actions, Reducers, Effects, and Selectors. Effects handle side effects (API calls) outside reducers. Built-in DI and RxJS integration. Steeper learning curve but excellent for enterprise Angular apps.

## Vue + Pinia
Official Vue state library with simpler API than Vuex. Composition API stores with ref/reactive. storeToRefs preserves reactivity when destructuring. Less boilerplate than Redux/NgRx, great TypeScript support.

## Key Differences
- **Boilerplate:** Pinia < Redux Toolkit < NgRx
- **Learning curve:** Pinia easiest, NgRx steepest
- **Tooling:** Redux DevTools (React), Vue DevTools Pinia tab (Vue), NgRx Store DevTools (Angular)
