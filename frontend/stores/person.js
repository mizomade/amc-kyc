// stores/person.js
import { defineStore } from 'pinia'

export const usePersonStore = defineStore('person', {
  state: () => ({
    person_id: null,
  }),

  actions: {
    setPersonId(id) {
      this.person_id = id
    },

    clearPersonId() {
      this.person_id = null
    },
  },
})
