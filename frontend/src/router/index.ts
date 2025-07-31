import { createRouter, createWebHistory } from "vue-router";

// Import route components
import Profile from "../pages/Profile.vue";
import Hobbies from "../pages/Hobbies.vue";
import SimilarHobbies from "../pages/SimilarHobbies.vue";
import FriendRequests from "../pages/FriendRequests.vue";
import FriendsList from "../pages/FriendsList.vue"; // Import the Friends List page
import Login from "../pages/Login.vue";

// Define routes
const routes = [
  { path: "/profile", name: "Profile", component: Profile, meta: { requiresAuth: true } },
  { path: "/hobbies", name: "Hobbies", component: Hobbies, meta: { requiresAuth: true } },
  { path: "/similar_hobbies", name: "SimilarHobbies", component: SimilarHobbies, meta: { requiresAuth: true } },
  { path: "/friend_requests", name: "FriendRequests", component: FriendRequests, meta: { requiresAuth: true } },
  { path: "/friends_list", name: "FriendsList", component: FriendsList, meta: { requiresAuth: true } }, // Add Friends List route
  { path: "/login", name: "Login", component: Login },
];

// Create router
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// Navigation guard to restrict access to authenticated users
router.beforeEach(async (to: any, _from: any, next: any) => {
  if (to.meta.requiresAuth) {
    try {
      const response = await fetch("/api/authenticated/", {
        credentials: "include", // Ensure cookies are sent for session authentication
      });

      if (response.ok) {
        const data = await response.json();
        if (data.authenticated) {
          next(); // Allow access if authenticated
        } else {
          window.location.href = "/login/"; // Redirect to login
        }
      } else {
        window.location.href = "/login/"; // Redirect to login if not authenticated
      }
    } catch (error) {
      console.error("Error during authentication check:", error);
      window.location.href = "/login/";
    }
  } else {
    next(); // Allow access to non-protected routes
  }
});

export default router;
