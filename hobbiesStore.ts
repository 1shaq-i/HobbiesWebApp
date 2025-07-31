import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useHobbiesStore = defineStore('hobbies', () => {
  const hobbies = ref<Hobby[]>([]);
  const isLoading = ref(false);

  interface Hobby {
    id: number;
    name: string;
  }

  const fetchHobbies = async () => {
    isLoading.value = true;
    try {
      const response = await fetch(`/api/hobbies/`, {
        method: 'GET',
        credentials: 'include', // Ensures cookies are sent for authentication
      });
      if (response.ok) {
        hobbies.value = await response.json();
        console.log('Hobbies fetched:', hobbies.value);
      } else {
        console.error(`Failed to fetch hobbies. Status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error fetching hobbies:', error);
    } finally {
      isLoading.value = false;
    }
  };

  return { hobbies, fetchHobbies, isLoading };
});
