<template>
  <div>
    <h2>Users with Similar Hobbies</h2>
    <div>
      <label for="ageMin">Min Age:</label>
      <input v-model="ageMin" id="ageMin" type="number" placeholder="15" />

      <label for="ageMax">Max Age:</label>
      <input v-model="ageMax" id="ageMax" type="number" placeholder="20" />

      <button @click="fetchUsers">Apply Filters</button>
    </div>

    <table>
      <thead>
        <tr>
          <th>Username</th>
          <th>Email</th>
          <th>Age</th>
          <th>Shared Hobbies</th>
          <th>Hobbies</th>
          <th>Send Friend Request</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.username">
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.age }}</td>
          <td>{{ user.shared_hobbies }}</td>
          <td>{{ user.hobbies.join(', ') }}</td>
          <td>
            <button
            @click="sendFriendRequest(user.username)"
            :disabled="user.friend_request_sent || user.is_friend"
            >
            {{ user.friend_request_sent ? "Request Sent" : user.is_friend ? "Friends" : "Send Friend Request" }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <div>
      <button @click="prevPage" :disabled="!pagination.has_previous">Previous</button>
      <span>Page {{ pagination.page_number }} of {{ pagination.total_pages }}</span>
      <button @click="nextPage" :disabled="!pagination.has_next">Next</button>
    </div>
  </div>
</template>

<script lang="ts">
import { ref } from "vue";

export default {
  name: "SimilarHobbies",
  setup() {
    const users: any = ref([]);
    const pagination: any = ref({
      has_next: false,
      has_previous: false,
      page_number: 1,
      total_pages: 1,
    });

    const ageMin = ref("");
    const ageMax = ref("");

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

    const sendFriendRequest = async (username: string) => {
        try {
            const csrfToken = await getCsrfToken();
            const user: any = users.value.find((u: any) => u.username === username);

            // Disable button immediately
            if (user) user.friend_request_sent = true;

            const response = await fetch('/api/send_friend_request/', {
                method: 'POST',
                credentials: 'include', // Ensures cookies are included
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken, // Add the CSRF token here
                },
                body: JSON.stringify({ username }),
            });

            if (response.ok) {
                const data = await response.json();
                alert(data.message);
            } else {
                const errorData = await response.json();
                alert(errorData.error || "Failed to send friend request.");
                if (user) user.friend_request_sent = false; // Revert button state on failure
            }
        } catch (error) {
            console.error("Error sending friend request:", error);
            alert("An unexpected error occurred. Please try again later.");
            const user: any = users.value.find((u: any) => u.username === username);
            if (user) user.friend_request_sent = false; // Revert button state on failure
        }
    };




    const fetchUsers = async (page: any = 1) => {
      try {
        const params = new URLSearchParams();
        params.append("page", page);
        if (ageMin.value) params.append("age_min", ageMin.value);
        if (ageMax.value) params.append("age_max", ageMax.value);

        const response = await fetch(`/api/similar-users/?${params}`, {
          credentials: "include",
        });
        if (response.ok) {
          const data = await response.json();
          users.value = data.users;
          pagination.value = {
            has_next: data.has_next,
            has_previous: data.has_previous,
            page_number: data.page_number,
            total_pages: data.total_pages,
          };
        } else {
          console.error("Failed to fetch users:", response.statusText);
        }
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };

    const prevPage = () => {
      if (pagination.value.has_previous) {
        fetchUsers(pagination.value.page_number - 1);
      }
    };

    const nextPage = () => {
      if (pagination.value.has_next) {
        fetchUsers(pagination.value.page_number + 1);
      }
    };

    fetchUsers(); // Fetch users on component mount

    return {
      users,
      pagination,
      ageMin,
      ageMax,
      fetchUsers,
      prevPage,
      nextPage,
      sendFriendRequest,
    };
  },
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}

table, th, td {
  border: 1px solid black;
}

th, td {
  padding: 10px;
  text-align: left;
}
</style>
