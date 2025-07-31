<template>
    <div>
      <h2>Friend Requests</h2>
      <table>
        <thead>
          <tr>
            <th>Username</th>
            <th>Email</th>
            <th>Hobbies</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in friendRequests" :key="request.id">
            <td>{{ request.username }}</td>
            <td>{{ request.email }}</td>
            <td>{{ request.hobbies.join(', ') }}</td>
            <td>
              <button @click="acceptRequest(request.id)">Accept</button>
              <button @click="declineRequest(request.id)">Decline</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="friendRequests.length === 0">No friend requests.</p>
    </div>
  </template>
  
  <script lang="ts">
  import { ref, onMounted } from "vue";
  
  export default {
    name: "FriendRequests",
    setup() {
      const friendRequests: any = ref([]);
  
      const fetchFriendRequests = async () => {
        try {
          const response = await fetch("/api/friend_requests/", {
            credentials: "include",
          });
          if (response.ok) {
            const data = await response.json();
            friendRequests.value = data.friend_requests;
          } else {
            console.error("Failed to fetch friend requests.");
          }
        } catch (error) {
          console.error("Error fetching friend requests:", error);
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
          alert("Error fetching CSRF token: " + error);
        }
      }
  
      const handleRequest = async (id: any, method: string) => {
        try {
          const response = await fetch("/api/friend_requests/handle/", {
            method,
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": await getCsrfToken(),
            },
            credentials: "include",
            body: JSON.stringify({ id }),
          });
  
          if (response.ok) {
            const data = await response.json();
            alert(data.message);
            fetchFriendRequests(); // Refresh the list
          } else {
            console.error("Failed to handle friend request.");
          }
        } catch (error) {
          console.error("Error handling friend request:", error);
        }
      };
  
      const acceptRequest = (id: any) => handleRequest(id, "PUT");
      const declineRequest = (id: any) => handleRequest(id, "DELETE");
  
      onMounted(fetchFriendRequests);
  
      return {
        friendRequests,
        acceptRequest,
        declineRequest,
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
  
  button {
    margin-right: 5px;
  }
</style>