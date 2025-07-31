<template>
  <div>
    <h2>User Profile</h2>
    <form @submit.prevent="updateProfile">
      <div>
        <label for="username">Username:</label>
        <input v-model="profile.username" id="username" type="text" required />
      </div>
      <div>
        <label for="email">Email:</label>
        <input v-model="profile.email" id="email" type="email" required />
      </div>
      <div>
        <label for="firstName">First Name:</label>
        <input v-model="profile.first_name" id="firstName" type="text" />
      </div>
      <div>
        <label for="lastName">Last Name:</label>
        <input v-model="profile.last_name" id="lastName" type="text" />
      </div>
      <div>
        <label for="dateOfBirth">Date of Birth:</label>
        <input v-model="profile.date_of_birth" id="dateOfBirth" type="date" />
      </div>
      <div>
        <label>Hobbies:</label>
        <div v-for="hobby in hobbies" :key="hobby.id">
          <input type="checkbox" :value="hobby.id" v-model="profile.hobbies" />
          {{ hobby.name }}
        </div>
      </div>
      <button type="submit">Update Profile</button>
    </form>
    <div v-if="successMessage" class="success">{{ successMessage }}</div>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>

    <h2>Update Password</h2>
    <form @submit.prevent="updatePassword">
      <div>
        <label for="oldPassword">Current Password:</label>
        <input v-model="passwordData.old_password" id="oldPassword" type="password" required />
      </div>
      <div>
        <label for="newPassword1">New Password:</label>
        <input v-model="passwordData.new_password1" id="newPassword1" type="password" required />
      </div>
      <div>
        <label for="newPassword2">Confirm Password:</label>
        <input v-model="passwordData.new_password2" id="newPassword2" type="password" required />
      </div>
      <button type="submit">Update Password</button>
    </form>
    <div v-if="passwordSuccessMessage" class="success">{{ passwordSuccessMessage }}</div>
    <div v-if="passwordErrorMessage" class="error">{{ passwordErrorMessage }}</div>

    <h2>Delete Account</h2>
    <p class="warning">This action cannot be undone.</p>
    <button class="delete-button" @click="deleteAccount">Delete Account</button>
  </div>
</template>


<script lang="ts">
import { ref, onMounted } from "vue";
import { useHobbiesStore } from "../stores/hobbiesStore";

export default {
  name: "Profile",
  setup() {
    const profile = ref({
      username: "",
      email: "",
      first_name: "",
      last_name: "",
      date_of_birth: "",
      hobbies: [], // Array of selected hobby IDs
    });

    const passwordData: any = ref({
      old_password: "", // Rename current_password to old_password
      new_password1: "", // Rename new_password to new_password1
      new_password2: "", // Rename confirm_password to new_password2
});


    const errorMessage: any = ref(null);
    const successMessage: any = ref(null);
    const passwordErrorMessage: any = ref(null);
    const passwordSuccessMessage: any = ref(null);
    const hobbiesStore = useHobbiesStore();
    const hobbies = hobbiesStore.hobbies;

    const fetchProfile = async () => {
      try {
        const response = await fetch("/api/profile/", {
          credentials: "include",
        });
        if (response.ok) {
          const data = await response.json();
          profile.value = {
            ...data,
            hobbies: data.hobbies.map((hobby: string) => hobby[0]), // Extract hobby IDs
          };
        } else {
          console.error("Failed to fetch profile data");
        }
      } catch (error) {
        console.error("Error fetching profile:", error);
      }
    };

    async function getCsrfToken() {
      try {
        const response = await fetch("/csrf/", {
          credentials: "include",
        });
        if (response.ok) {
          const data = await response.json();
          return data.csrfToken;
        } else {
          alert("Failed to fetch CSRF token");
        }
      } catch (error) {
        alert("Error fetching CSRF token:" + error);
      }
    }

    const updateProfile = async () => {
      errorMessage.value = null;
      successMessage.value = null;

      const csrfToken = await getCsrfToken();
      try {
        const response = await fetch("/api/profile/update/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          credentials: "include",
          body: JSON.stringify(profile.value),
        });

        if (response.ok) {
          const data = await response.json();
          successMessage.value = data.message || "Profile updated successfully.";
        } else {
          const errorData = await response.json();
          errorMessage.value = errorData.errors || "Failed to update profile.";
        }
      } catch (error: any) {
        console.error("Error updating profile:", error);
        errorMessage.value = "An error occurred. Please try again.";
      }
    };

    const updatePassword = async () => {
      passwordErrorMessage.value = null;
      passwordSuccessMessage.value = null;

      try {
        const response = await fetch("/api/password/update/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
          body: JSON.stringify(passwordData.value),
        });

        if (response.ok) {
          const data = await response.json();
          passwordSuccessMessage.value = data.message || "Password updated successfully.";
          passwordData.value = { current_password: "", new_password: "", confirm_password: "" }; // Clear the form
        } else {
          const errorData = await response.json();
          passwordErrorMessage.value = errorData.errors || "Failed to update password.";
        }
      } catch (error) {
        console.error("Error updating password:", error);
        passwordErrorMessage.value = "An error occurred. Please try again.";
      }
    };

    const deleteAccount = async () => {
      const confirmation = confirm(
        "Are you sure you want to delete your account? This action cannot be undone."
      );
      if (!confirmation) return;

      try {
        const csrfToken = await getCsrfToken(); 
        const response = await fetch("/api/delete_user/", {
          method: "DELETE",
          headers: {
            "X-CSRFToken": csrfToken,
          },
          credentials: "include",
        });

        if (response.ok) {
          alert("Your account has been successfully deleted.");
          window.location.href = "/login/"; // Redirect to login page
        } else {
          const errorData = await response.json();
          alert(errorData.error || "Failed to delete account.");
        }
      } catch (error) {
        console.error("Error deleting account:", error);
        alert("An unexpected error occurred. Please try again.");
      }
    };

    onMounted(() => {
      hobbiesStore.fetchHobbies();
      fetchProfile();
    });

    return {
      profile,
      passwordData,
      errorMessage,
      successMessage,
      passwordErrorMessage,
      passwordSuccessMessage,
      hobbies,
      updateProfile,
      updatePassword,
      deleteAccount,
    };
  },
};

</script>
<style scoped>
.error {
  color: red;
}
.success {
  color: green;
}
.warning {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}
.delete-button {
  background-color: red;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
}
.delete-button:hover {
  background-color: darkred;
}
</style>