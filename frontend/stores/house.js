import { defineStore } from 'pinia';

export const useHouseStore = defineStore('house', {
  state: () => ({
    house: null,
    members: [],
  }),
  actions: {
    setHouse(houseData) {
      this.house = houseData;
    },
    addMember(memberData) {
      this.members.push(memberData);
    },
    async fetchMembers(houseId) {
      try {
        const response = await $fetch(`http://localhost:8000/api/house/${houseId}/members`);
        this.members = response;
      } catch (error) {
        console.error('Error fetching members:', error);
      }
    },
  },
});
