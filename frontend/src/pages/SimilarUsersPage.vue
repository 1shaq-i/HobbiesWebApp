<template>
  <div>
    <h1>Users with Similar Hobbies</h1>

    <!-- Filters -->
    <div class="filters">
      <label>
        Min Age:
        <input type="number" v-model="filters.ageMin" @input="fetchSimilarUsers" />
      </label>
      <label>
        Max Age:
        <input type="number" v-model="filters.ageMax" @input="fetchSimilarUsers" />
      </label>
    </div>

    <!-- User List -->
    <ul>
      <li v-for="user in users" :key="user.id">
        <strong>{{ user.name }}</strong> (Age: {{ user.age }}) - {{ user.commonHobbies }} common hobbies
        <br />
        Hobbies: {{ user.hobbies.join(', ') }}
      </li>
    </ul>

    <!-- Pagination Controls -->
    <div v-if="pagination.totalPages > 1" class="pagination">
      <button @click="changePage(-1)" :disabled="pagination.currentPage === 1">Previous</button>
      <span>Page {{ pagination.currentPage }} of {{ pagination.totalPages }}</span>
      <button @click="changePage(1)" :disabled="pagination.currentPage === pagination.totalPages">Next</button>
    </div>

    <!-- No Results Message -->
    <p v-if="users.length === 0">No users found with the specified criteria.</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

interface User {
  id: number;
  name: string;
  age: number;
  hobbies: string[];
  commonHobbies: number;
}

export default defineComponent({
  name: "SimilarUsersPage",
  setup() {
    const users = ref<User[]>([]);
    const filters = ref<{ ageMin: number | null; ageMax: number | null }>({
      ageMin: null,
      ageMax: null,
    });
    const pagination = ref({
      currentPage: 1,
      totalPages: 1,
    });

    const fetchSimilarUsers = async () => {
      try {
        const params = new URLSearchParams();
        if (filters.value.ageMin !== null)
          params.append("age_min", filters.value.ageMin.toString());
        if (filters.value.ageMax !== null)
          params.append("age_max", filters.value.ageMax.toString());
        params.append("page", pagination.value.currentPage.toString());

        const response = await fetch(`/api/similar-hobbies?${params.toString()}`);
        const data = await response.json();

        // Backend response structure:
        // { results: [{id, name, age, hobbies, common_hobbies}], total_pages }
        users.value = data.results.map((user: any) => ({
          id: user.id,
          name: user.name,
          age: user.age,
          hobbies: user.hobbies,
          commonHobbies: user.common_hobbies,
        }));
        pagination.value.totalPages = data.total_pages;
      } catch (error) {
        console.error("Error fetching similar users:", error);
      }
    };

    const changePage = (direction: number) => {
      const newPage = pagination.value.currentPage + direction;
      if (newPage > 0 && newPage <= pagination.value.totalPages) {
        pagination.value.currentPage = newPage;
        fetchSimilarUsers();
      }
    };

    // Fetch users on component mount
    fetchSimilarUsers();

    return { users, filters, pagination, fetchSimilarUsers, changePage };
  },
});
</script>

<style scoped>
.filters {
  margin-bottom: 1rem;
}
.pagination {
  margin-top: 1rem;
}
button {
  margin: 0 0.5rem;
}
</style>
