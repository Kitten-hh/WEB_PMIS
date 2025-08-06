<template>
    <div class="container mt-4">
      <notification-toggle-list
        title="Staff"
        :items="staffItems"
        @change="updateSetting"
      />
      <notification-toggle-list
        title="Projects"
        :items="projectItems"
        @change="updateSetting"
      />
      <notification-toggle-list
        title="Session and Category"
        :items="categoryItems"
        @change="updateSetting"
      />
    </div>
  </template>
  
  <script>
  //import NotificationToggleList from './NotificationToggleList.vue';
  
  export default {
    name: 'NotificationSettings',
    components: {
      //NotificationToggleList,
    },
    data() {
      return {
        notifications: {
          staff: false,
          projects: false,
          sessionCategory: false,
          // Add your dynamic properties here
        },
        staffItems: [
          { id: 'hb', label: 'hb', enabled: false },
          { id: 'sig', label: 'sig', enabled: false },
        ],
        projectItems: [
          { id: '00039', label: '00039', enabled: false },
          { id: '00930', label: '00930', enabled: false },
        ],
        categoryItems: [
          { id: 'newRequest', label: 'New Request', enabled: false },
          { id: 'allocation', label: 'Allocation', enabled: false },
          { id: 'highPriority', label: 'High Priority', enabled: false },
          // Add more categories as needed
        ],
      };
    },
    methods: {
      updateSetting(id, enabled) {
        console.log(`Updated ${id}:`, enabled);
        // Handle the change in settings, e.g., update the backend or local storage
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 600px;
  }
  
  .card-header {
    font-weight: bold;
    font-size: 1.25rem;
  }
  </style>
  