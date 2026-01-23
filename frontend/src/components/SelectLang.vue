<script setup>
defineProps({
  modelValue: String,
  options: Array,
  label: {
    type: String,
    default: ''
  }
})
const emit = defineEmits(['update:modelValue'])
</script>

<template>
  <div class="select-lang">
    <label v-if="label" class="select-label">{{ label }}</label>
    <div class="select-wrapper">
      <select
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        class="custom-select"
      >
        <option v-for="option in options" :key="option.code" :value="option.code">
          {{ option.name }}
        </option>
      </select>
    </div>
  </div>
</template>

<style scoped>
.select-lang {
  display: flex;
  flex-direction: column;
}

.select-label {
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--cl-gray-400);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-family: var(--font-display);
}

.select-wrapper {
  position: relative;
}

.custom-select {
  width: 100%;
  padding: 0.8rem 1rem;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background-color: rgba(0, 0, 0, 0.3);
  color: var(--cl-white);
  font-size: 1rem;
  font-family: var(--font-primary);
  cursor: pointer;
  transition: all 0.3s ease;
  appearance: none; /* Remove default arrow */
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23F1890E' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1em;
}

.custom-select:focus {
  outline: none;
  border-color: var(--cl-primary);
  box-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
  background-color: rgba(0, 0, 0, 0.5);
}

.custom-select option {
  background-color: var(--cl-bg-dark);
  color: var(--cl-white);
  padding: 10px;
}
</style>
