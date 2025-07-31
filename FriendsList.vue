<template>
  <div>
    <h2>Your Friends</h2>
    <table>
      <thead>
        <tr>
          <th>Username</th>
          <th>Email</th>
          <th>Hobbies</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="friend in friends" :key="friend.username">
          <td>{{ friend.username }}</td>
          <td>{{ friend.email }}</td>
          <td>{{ friend.hobbies.join(', ') }}</td>
        </tr>
      </tbody>
    </table>
    <p v-if="friends.length === 0">You have no friends yet.</p>
  </div>
</template>

<script lang="ts">
import { ref, onMounted } from "vue";

// Define the Friend interface for strict typing
interface Friend {
  username: string;
  email: string;
  hobbies: string[];
}

export default {
  name: "FriendsList",
  setup() {
    const friends = ref<Friend[]>([]);

    const fetchFriends = async (): Promise<void> => {
      try {
        const response = await fetch("/api/friends_list/", {
          credentials: "include",
        });
        if (response.ok) {
          const data = await response.json();
          friends.value = data.friends.map((friend: any) => ({
            username: friend.username,
            email: friend.email,
            hobbies: friend.hobbies,
          }));
        } else {
          console.error("Failed to fetch friends.");
        }
      } catch (error) {
        console.error("Error fetching friends:", error);
      }
    };

    onMounted(() => {
      fetchFriends().catch((error) =>
        console.error("Error during initial data fetch:", error)
      );
    });

    return {
      friends,
    };
  },
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}

table,
th,
td {
  border: 1px solid black;
}

th,
td {
  padding: 10px;
  text-align: left;
}
</style>
