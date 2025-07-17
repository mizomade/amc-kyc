import { defineStore } from 'pinia';
import { useNuxtApp } from '#app';   // Required if injecting api here (alternative below)

export const useHouseStore = defineStore('house', {
  state: () => ({
    house_id: null,
    house_details: {},
    members: []
  }),

  actions: {
    setHouseId(id) {
      this.house_id = id;
    },

    setHouseDetails(details) {
      this.house_details = details;
    },

    addMember(member) {
      this.members.push(member);
    },

    clearHouse() {
      this.house_id = null;
      this.house_details = {};
      this.members = [];
    },

    // Fetch members from API
    async fetchMembers($api) {
      if (!this.house_id) return;

      try {
        const response = await $api.get(`/house/${this.house_id}/members/`);
        this.members = response.data;
      } catch (error) {
        console.error('Failed to fetch house members:', error);
        this.members = [];
      }
    }
  }
});