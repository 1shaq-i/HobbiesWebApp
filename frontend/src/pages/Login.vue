<template>
    <div class="login-container">
      <h1>Login</h1>
      <form @submit.prevent="login">
        <div>
          <label for="username">Username</label>
          <input type="text" v-model="form.username" required />
        </div>
        <div>
          <label for="password">Password</label>
          <input type="password" v-model="form.password" required />
        </div>
        <button type="submit">Login</button>
      </form>
      <p>
        Don't have an account? <router-link to="/register">Register here</router-link>.
      </p>
    </div>
  </template>
  
  <script setup lang="ts">
  import { reactive } from "vue";
  import { useRouter } from "vue-router";
  
  const router = useRouter();
  
  const form = reactive({
    username: "",
    password: ""
  });
  
  const login = async () => {
    try {
      const response = await fetch("/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
        credentials: "include"
      });
  
      if (response.ok) {
        alert("Login successful! Redirecting to the main page...");
        router.push("/profile"); // Redirect to the profile or main page
      } else {
        const data = await response.json();
        alert(`Login failed: ${data.error || "Invalid credentials"}`);
      }
    } catch (error: any) {
      alert("An error occurred: " + error.message);
    }
  };
  </script>
  
  <style>
  /* Add your styles here */
  </style>
  