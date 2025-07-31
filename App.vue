<template>
    <main class="container pt-4">
      <div>
        <router-link :to="{ name: 'Hobbies' }">Hobbies</router-link>
        |
        <router-link :to="{ name: 'Profile' }">Profile</router-link>
        |
        <router-link :to="{ name: 'SimilarHobbies' }">Similar Hobbies</router-link>
        |
        <router-link :to="{ name: 'FriendRequests' }">Friend Requests</router-link>
        |
        <router-link :to="{ name: 'FriendsList' }">Friends List</router-link>
        |
        <a href="#" @click.prevent="logout">Logout</a>
      </div>
      <RouterView class="flex-shrink-0" />
    </main>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  
  export default defineComponent({
    methods: {
      async logout() {
        try {
          const response = await fetch("/logout/", {
            method: "GET",
            credentials: "include",
          });
          if (response.ok) {
            window.location.href = "/login/"; // Redirect to login page
          } else {
            console.error("Logout failed");
          }
        } catch (error) {
          console.error("Error during logout:", error);
        }
      },
    },
  });
  </script>
  
  <style scoped>
  </style>
  