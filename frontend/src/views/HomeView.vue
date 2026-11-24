<script setup>
import { RouterLink } from 'vue-router'
import TheWelcome from '../components/TheWelcome.vue'
</script>

<template>
  <!-- <main>
    <TheWelcome />
  </main> -->
  <h1>Welcome to the Home Page</h1>
  <p>This is the home page of our application.</p>
  <RouterLink to="/login">Enter into your account now! Login</RouterLink>
  <RouterLink to="/register">Don't have an account? Register</RouterLink>
  <br>
  <RouterLink to="/about">Go to About</RouterLink>
</template>
