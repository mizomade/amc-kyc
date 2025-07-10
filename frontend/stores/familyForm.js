import { defineStore } from 'pinia'

export const useFamilyFormStore = defineStore('familyForm', {
  state: () => ({
    house: {
      house_number: '',
      parent_house_id: null,
      veng_id: null,
      street: '',
      landmarks: '',
      is_owner: true,
      lsc_number: '',
      awmtan_kum: null,
      pem_luh_chhan: '',
      have_tenant: false,
      household_size: null,
      is_tenant: false,
      landlord_name: '',
      landlord_phone: '',
      landlord_veng: '',
      latitude: null,
      longitude: null,
    },
    house_id: null,
    father_id: null,
    mother_id: null,
    members: [], // list of all family members
  }),

  actions: {
    setHouseId(id) {
      this.house_id = id
    },
    setFatherId(id) {
      this.father_id = id
    },
    setMotherId(id) {
      this.mother_id = id
    },
    addMember(member) {
      this.members.push(member)
    },
    updateHouseField(key, value) {
      this.house[key] = value
    },
    reset() {
      this.house_id = null
      this.father_id = null
      this.mother_id = null
      this.house = {
        house_number: '',
        parent_house_id: null,
        veng_id: null,
        street: '',
        landmarks: '',
        is_owner: true,
        lsc_number: '',
        awmtan_kum: null,
        pem_luh_chhan: '',
        have_tenant: false,
        household_size: null,
        is_tenant: false,
        landlord_name: '',
        landlord_phone: '',
        landlord_veng: '',
        latitude: null,
        longitude: null,
      }
      this.members = []
    }
  }
})
