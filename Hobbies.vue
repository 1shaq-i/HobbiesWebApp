<template>
    <div class="h3">
      {{ title }}
    </div>
    <ul>
      <li v-for="(hobby) in hobbiesStore.hobbies" :key="hobby.id">
        {{ hobby.name }}
      </li>
    </ul>
    <button data-bs-toggle="modal" data-bs-target="#addHobbyModal">
      Add Hobby
    </button>
  
    <!-- Modal for adding a hobby -->
    <div class="modal fade" id="addHobbyModal" tabindex="-1" aria-labelledby="addHobbyModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="addHobbyModalLabel">Add Hobby</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label for="name" class="form-label">Name</label>
              <input v-model="newHobby.name" type="text" class="form-control" id="name" />
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Close
            </button>
            <button type="button" class="btn btn-primary" @click="createHobby()" data-bs-dismiss="modal">
              Save
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, onMounted, ref } from "vue";
  import { useHobbiesStore } from "../stores/hobbiesStore";
  
  export default defineComponent({
    setup() {
        const hobbiesStore = useHobbiesStore();
        const newHobby = ref<{ name: string }>({ name: "" });

        onMounted(() => {
            hobbiesStore.fetchHobbies();
        });

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
    
        // Create a new hobby
        const createHobby = async () => {
            if (!newHobby.value.name) {
                alert("Hobby name is required.");
                return;
            }
    
            // Check if the hobby already exists in the store
            const existingHobby = hobbiesStore.hobbies.find(
                (hobby) => hobby.name.toLowerCase() === newHobby.value.name.toLowerCase()
            );
    
            if (existingHobby) {
                alert("This hobby already exists.");
                return;
            }

            const csrfToken = await getCsrfToken();
            try {
                const response = await fetch(`/api/hobbies/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrfToken,
                    },
                    body: JSON.stringify({ name: newHobby.value.name }),
                });
    
                if (response.ok) {
                    const addedHobby = await response.json();
                    hobbiesStore.hobbies.push(addedHobby); // Add to store
                    newHobby.value.name = ""; 
                } else {
                    const error = await response.json();
                    alert("Error adding hobby: " + error.error);
                }
                } catch (error) {
                console.error("Error creating hobby:", error);
                alert("An error occurred while adding the hobby.");
            }
        };
    
        return {
            hobbiesStore,
            title: "Hobbies",
            newHobby,
            createHobby,
        };
    },
  });
  </script>
  
  <style scoped>
  </style>
  