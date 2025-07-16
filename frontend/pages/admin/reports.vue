<template>
  <div class="min-h-screen bg-gray-50 p-4 sm:p-6 lg:p-8">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-3xl font-bold tracking-tight text-gray-900 mb-8">Reports Dashboard</h1>

      <!-- Tabs -->
      <div class="bg-white rounded-lg shadow-sm mb-8">
        <nav class="flex space-x-1 p-1.5" aria-label="Tabs">
          <!-- <button @click="setActiveReport('summary')" :class="[activeReport === 'summary' ? 'bg-blue-600 text-white shadow-md' : 'text-gray-600 hover:bg-gray-200', 'px-4 py-2.5 font-medium text-sm rounded-md transition']">
            <Icon name="heroicons:chart-pie" class="w-5 h-5 mr-2 inline-block" /> Summary
          </button> -->
          <button @click="setActiveReport('persons')" :class="[activeReport === 'persons' ? 'bg-blue-600 text-white shadow-md' : 'text-gray-600 hover:bg-gray-200', 'px-4 py-2.5 font-medium text-sm rounded-md transition']">
            <Icon name="heroicons:users" class="w-5 h-5 mr-2 inline-block" /> Citizens Report
          </button>
          <button @click="setActiveReport('houses')" :class="[activeReport === 'houses' ? 'bg-blue-600 text-white shadow-md' : 'text-gray-600 hover:bg-gray-200', 'px-4 py-2.5 font-medium text-sm rounded-md transition']">
            <Icon name="heroicons:home-modern" class="w-5 h-5 mr-2 inline-block" /> Houses Report
          </button>
        </nav>
      </div>

      <!-- Report Panels -->
      <div class="bg-white rounded-lg shadow-lg p-6 min-h-[500px]">
        <!-- Summary -->
        <div v-if="activeReport === 'summary'">
          <h2 class="text-2xl font-semibold text-gray-800 mb-6">Data Summary</h2>
          <div v-if="isLoading" class="flex justify-center items-center h-64">
            <Icon name="svg-spinners:3-dots-fade" class="w-12 h-12 text-blue-600" />
          </div>
          <div v-else-if="summaryData" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <div class="bg-blue-50 border-l-4 border-blue-500 p-6 rounded-lg">
              <h3 class="text-lg font-medium text-gray-700">Total Citizens</h3>
              <p class="text-4xl font-bold text-blue-900 mt-2">{{ summaryData.total_citizens }}</p>
            </div>
            <div class="bg-green-50 border-l-4 border-green-500 p-6 rounded-lg">
              <h3 class="text-lg font-medium text-gray-700">Total Houses</h3>
              <p class="text-4xl font-bold text-green-900 mt-2">{{ summaryData.houses }}</p>
            </div>
            <div class="bg-indigo-50 border-l-4 border-indigo-500 p-6 rounded-lg">
              <h3 class="text-lg font-medium text-gray-700">Verified Persons</h3>
              <p class="text-4xl font-bold text-indigo-900 mt-2">{{ summaryData.verified_persons }}</p>
            </div>
            <div class="bg-red-50 border-l-4 border-red-500 p-6 rounded-lg">
              <h3 class="text-lg font-medium text-gray-700">Unverified Persons</h3>
              <p class="text-4xl font-bold text-red-900 mt-2">{{ summaryData.unverified_persons }}</p>
            </div>
            <div class="bg-purple-50 border-l-4 border-purple-500 p-6 rounded-lg">
              <h3 class="text-lg font-medium text-gray-700">Verified Houses</h3>
              <p class="text-4xl font-bold text-purple-900 mt-2">{{ summaryData.verified_houses }}</p>
            </div>
            <div class="bg-orange-50 border-l-4 border-orange-500 p-6 rounded-lg">
              <h3 class="text-lg font-medium text-gray-700">Unverified Houses</h3>
              <p class="text-4xl font-bold text-orange-900 mt-2">{{ summaryData.unverified_houses }}</p>
            </div>
            <div class="bg-yellow-50 border-l-4 border-yellow-500 p-6 rounded-lg">
              <h3 class="text-lg font-medium text-gray-700">Owner Houses</h3>
              <p class="text-4xl font-bold text-yellow-900 mt-2">{{ summaryData.owner_houses }}</p>
            </div>
            <div class="bg-cyan-50 border-l-4 border-cyan-500 p-6 rounded-lg">
              <h3 class="text-lg font-medium text-gray-700">Tenant Houses</h3>
              <p class="text-4xl font-bold text-cyan-900 mt-2">{{ summaryData.tenant_houses }}</p>
            </div>
            <div class="bg-lime-50 border-l-4 border-lime-500 p-6 rounded-lg">
              <h3 class="text-lg font-medium text-gray-700">Houses with Tenants</h3>
              <p class="text-4xl font-bold text-lime-900 mt-2">{{ summaryData.have_tenant_houses }}</p>
            </div>
            <div class="bg-blue-100 border-l-4 border-blue-600 p-6 rounded-lg">
              <h3 class="text-lg font-medium text-gray-700">Houses without Tenants</h3>
              <p class="text-4xl font-bold text-blue-900 mt-2">{{ summaryData.houses_without_tenants }}</p>
            </div>
            <div class="bg-green-100 border-l-4 border-green-600 p-6 rounded-lg">
              <h3 class="text-lg font-medium text-gray-700">Number of Tenants (Persons)</h3>
              <p class="text-4xl font-bold text-green-900 mt-2">{{ summaryData.num_tenants_persons }}</p>
            </div>
            <div class="bg-purple-100 border-l-4 border-purple-600 p-6 rounded-lg">
              <h3 class="text-lg font-medium text-gray-700">Average Household Size</h3>
              <p class="text-4xl font-bold text-purple-900 mt-2">{{ summaryData.average_household_size }}</p>
            </div>
            <div class="bg-red-100 border-l-4 border-red-600 p-6 rounded-lg">
              <h3 class="text-lg font-medium text-gray-700">Street with Most Houses</h3>
              <p class="text-4xl font-bold text-red-900 mt-2">{{ summaryData.street_with_most_houses }}</p>
            </div>
          </div>

          
        </div>

        <!-- Persons Report -->
        <div v-if="activeReport === 'persons'">
          <h2 class="text-2xl font-semibold text-gray-800 mb-6">Persons Report</h2>

          <!-- Filters -->
          <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            <!-- Geography -->
            <details class="group" open>
              <summary class="flex justify-between items-center font-medium text-gray-800 cursor-pointer py-2">
                Geography
                <Icon name="heroicons:chevron-down" class="w-5 h-5 transform transition-transform group-open:rotate-180" />
              </summary>
              <div class="pt-2">
                <label class="block text-sm font-medium text-gray-700">Veng</label>
                <select v-model="personFilters.veng_id" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500">
                  <option value="">All</option>
                  <option v-for="v in vengs" :key="v.id" :value="v.id">{{ v.name }}</option>
                </select>
                <label class="block text-sm font-medium text-gray-700 mt-2">Street</label>
                <input v-model="personFilters.street" placeholder="Street name" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500" />
              </div>
            </details>

            <!-- Demographic -->
            <details class="group" open>
              <summary class="flex justify-between items-center font-medium text-gray-800 cursor-pointer py-2">
                Demographics
                <Icon name="heroicons:chevron-down" class="w-5 h-5 transform transition-transform group-open:rotate-180" />
              </summary>
              <div class="pt-2">
                <label class="block text-sm font-medium text-gray-700">Gender</label>
                <select v-model="personFilters.gender" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500">
                  <option value="">All</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
                <label class="block text-sm font-medium text-gray-700 mt-2">Age Group</label>
                <div class="flex gap-2">
                  <input v-model.number="personFilters.min_age" type="number" placeholder="Min" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500" />
                  <input v-model.number="personFilters.max_age" type="number" placeholder="Max" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500" />
                </div>
                <label class="block text-sm font-medium text-gray-700 mt-2">Marital Status</label>
                <select v-model="personFilters.marital_status" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500">
                  <option value="">All</option>
                  <option value="Single">Single</option>
                  <option value="Married">Married</option>
                  <option value="Widowed">Widowed</option>
                  <option value="Divorced">Divorced</option>
                </select>
                <label class="block text-sm font-medium text-gray-700 mt-2">Blood Group</label>
                <select v-model="personFilters.blood_group" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500">
                  <option value="">All</option>
                  <option v-for="bg in bloodGroups" :key="bg" :value="bg">{{ bg }}</option>
                </select>
              </div>
            </details>

            <!-- Religion -->
            <details class="group" open>
              <summary class="flex justify-between items-center font-medium text-gray-800 cursor-pointer py-2">
                Religion
                <Icon name="heroicons:chevron-down" class="w-5 h-5 transform transition-transform group-open:rotate-180" />
              </summary>
              <div class="pt-2">
                <label class="block text-sm font-medium text-gray-700">Religion</label>
                <select v-model="personFilters.religion_id" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500">
                  <option value="">All</option>
                  <option v-for="r in religions" :key="r.id" :value="r.id">{{ r.name }}</option>
                </select>
                <label class="block text-sm font-medium text-gray-700 mt-2">Denomination</label>
                <select v-model="personFilters.denomination_id" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500">
                  <option value="">All</option>
                  <option v-for="d in denominations" :key="d.id" :value="d.id">{{ d.name }}</option>
                </select>
              </div>
            </details>

            <!-- Other -->
            <details class="group" open>
              <summary class="flex justify-between items-center font-medium text-gray-800 cursor-pointer py-2">
                Other
                <Icon name="heroicons:chevron-down" class="w-5 h-5 transform transition-transform group-open:rotate-180" />
              </summary>
              <div class="pt-2">
                <label class="block text-sm font-medium text-gray-700">Education</label>
                <select v-model="personFilters.education_id" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500">
                  <option value="">All</option>
                  <option v-for="e in educations" :key="e.id" :value="e.id">{{ e.name }}</option>
                </select>
                <label class="block text-sm font-medium text-gray-700 mt-2">Occupation</label>
                <select v-model="personFilters.occupation_id" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500">
                  <option value="">All</option>
                  <option v-for="o in occupations" :key="o.id" :value="o.id">{{ o.name }}</option>
                </select>
                <label class="block text-sm font-medium text-gray-700 mt-2">Verification</label>
                <select v-model="personFilters.is_verified" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500">
                  <option :value="null">All</option>
                  <option :value="true">Verified</option>
                  <option :value="false">Not Verified</option>
                </select>
              </div>
            </details>

            <div class="col-span-full flex justify-end space-x-4">
              <button @click="resetPersonFilters" class="bg-gray-300 text-gray-800 px-6 py-2.5 rounded shadow hover:bg-gray-400 flex items-center">
                <Icon name="heroicons:arrow-path" class="w-5 h-5 mr-2" /> Reset Filters
              </button>
              <button @click="fetchPersonsReport" class="bg-blue-600 text-white px-6 py-2.5 rounded shadow hover:bg-blue-700 flex items-center">
                <Icon name="heroicons:magnifying-glass" class="w-5 h-5 mr-2" /> Generate Report
              </button>
            </div>
          </div>

          <!-- Table -->
          <div v-if="isLoading" class="flex justify-center items-center h-64">
            <Icon name="svg-spinners:3-dots-fade" class="w-12 h-12 text-blue-600" />
          </div>
          <div v-else-if="personsReportData.length > 0" class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Gender</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">DOB</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Qualifications</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Occupations</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="p in personsReportData" :key="p.id">
                  <td class="px-6 py-4">{{ p.first_name }} {{ p.hnam_hming }}</td>
                  <td class="px-6 py-4">{{ p.gender }}</td>
                  <td class="px-6 py-4">{{ p.dob }}</td>
                  <td class="px-6 py-4">{{ p.qualifications.map(q => q.education).join(', ') }}</td>
                  <td class="px-6 py-4">{{ p.occupations.map(o => o.occupation).join(', ') }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="text-center py-16">
            <Icon name="heroicons:document-magnifying-glass" class="w-12 h-12 mx-auto text-gray-400" />
            <h3 class="mt-2 text-sm font-medium text-gray-900">No Data</h3>
            <p class="mt-1 text-sm text-gray-500">Adjust filters or try again.</p>
          </div>

          <!-- Persons Report Summary Statistics -->
          <div v-if="personsReportData.length > 0" class="mt-8 p-6 bg-white rounded-lg shadow-lg border border-gray-200">
            <h3 class="text-xl font-semibold text-gray-800 mb-4">Filtered Persons Statistics</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div class="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-lg">
                <h4 class="text-lg font-medium text-gray-700">Total Filtered Citizens</h4>
                <p class="text-3xl font-bold text-blue-900 mt-1">{{ totalFilteredCitizens }}</p>
              </div>

              <div class="bg-green-50 border-l-4 border-green-500 p-4 rounded-lg">
                <h4 class="text-lg font-medium text-gray-700">Gender Distribution</h4>
                <ul class="list-disc list-inside text-gray-800 mt-1">
                  <li v-for="(count, gender) in genderDistribution" :key="gender">{{ gender }}: {{ count }}</li>
                </ul>
              </div>

              <div class="bg-purple-50 border-l-4 border-purple-500 p-4 rounded-lg">
                <h4 class="text-lg font-medium text-gray-700">Religion Distribution</h4>
                <ul class="list-disc list-inside text-gray-800 mt-1">
                  <li v-for="(count, religion) in religionDistribution" :key="religion">{{ religion }}: {{ count }}</li>
                </ul>
              </div>

              <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded-lg">
                <h4 class="text-lg font-medium text-gray-700">Denomination Distribution</h4>
                <ul class="list-disc list-inside text-gray-800 mt-1">
                  <li v-for="(count, denomination) in denominationDistribution" :key="denomination">{{ denomination }}: {{ count }}</li>
                </ul>
              </div>

              <div class="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
                <h4 class="text-lg font-medium text-gray-700">Education Distribution</h4>
                <ul class="list-disc list-inside text-gray-800 mt-1">
                  <li v-for="(count, education) in educationDistribution" :key="education">{{ education }}: {{ count }}</li>
                </ul>
              </div>

              <div class="bg-indigo-50 border-l-4 border-indigo-500 p-4 rounded-lg">
                <h4 class="text-lg font-medium text-gray-700">Occupation Distribution</h4>
                <ul class="list-disc list-inside text-gray-800 mt-1">
                  <li v-for="(count, occupation) in occupationDistribution" :key="occupation">{{ occupation }}: {{ count }}</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <!-- Houses Report -->
        <div v-if="activeReport === 'houses'">
          <h2 class="text-2xl font-semibold text-gray-800 mb-6">Houses Report</h2>
          <!-- Filters -->
          <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            <details class="group" open>
              <summary class="flex justify-between items-center font-medium text-gray-800 cursor-pointer py-2">
                House Details
                <Icon name="heroicons:chevron-down" class="w-5 h-5 transform transition-transform group-open:rotate-180" />
              </summary>
              <div class="pt-2">
                <label class="block text-sm font-medium text-gray-700">House No. Search</label>
                <input v-model="houseFilters.house_number_search" placeholder="House Number" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500" />

                <label class="block text-sm font-medium text-gray-700 mt-2">Landlord Name Search</label>
                <input v-model="houseFilters.landlord_name_search" placeholder="Landlord Name" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500" />

                <label for="house_veng_filter" class="block text-sm font-medium text-gray-700 mt-2">Veng</label>
                <select id="house_veng_filter" v-model="houseFilters.veng_id" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500">
                  <option value="">All</option>
                  <option v-for="v in vengs" :key="v.id" :value="v.id">{{ v.name }}</option>
                </select>

                <label class="block text-sm font-medium text-gray-700 mt-2">Street</label>
                <input v-model="houseFilters.street" placeholder="Street name" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500" />
              </div>
            </details>

            <details class="group" open>
              <summary class="flex justify-between items-center font-medium text-gray-800 cursor-pointer py-2">
                Household & Tenancy
                <Icon name="heroicons:chevron-down" class="w-5 h-5 transform transition-transform group-open:rotate-180" />
              </summary>
              <div class="pt-2">
                <label class="block text-sm font-medium text-gray-700">Household Size</label>
                <input v-model.number="houseFilters.household_size" type="number" placeholder="Size" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500" />

                <label class="block text-sm font-medium text-gray-700 mt-2">Establish Date (Rent Start)</label>
                <input v-model="houseFilters.rent_start_date" type="date" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500" />

                <label class="block text-sm font-medium text-gray-700 mt-2">Ownership</label>
                <select v-model="houseFilters.is_owner" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500">
                  <option :value="null">Any</option>
                  <option :value="true">Owner</option>
                  <option :value="false">Not Owner</option>
                </select>

                <label class="block text-sm font-medium text-gray-700 mt-2">Has Tenants</label>
                <select v-model="houseFilters.have_tenant" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500">
                  <option :value="null">Any</option>
                  <option :value="true">Yes</option>
                  <option :value="false">No</option>
                </select>

                <label class="block text-sm font-medium text-gray-700 mt-2">Is Tenant</label>
                <select v-model="houseFilters.is_tenant" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500">
                  <option :value="null">Any</option>
                  <option :value="true">Yes</option>
                  <option :value="false">No</option>
                </select>

                <label class="block text-sm font-medium text-gray-700 mt-2">Landlord Veng</label>
                <input v-model="houseFilters.landlord_veng" placeholder="Landlord Veng" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500" />

                <label class="block text-sm font-medium text-gray-700 mt-2">Verification Status</label>
                <select v-model="houseFilters.is_verified" class="mt-1 block w-full p-2 border border-gray-400 rounded-md focus:ring-blue-500 focus:border-blue-500">
                  <option :value="null">All</option>
                  <option :value="true">Verified</option>
                  <option :value="false">Not Verified</option>
                </select>
              </div>
            </details>

            <div class="col-span-full flex justify-end space-x-4">
              <button @click="resetHouseFilters" class="bg-gray-300 text-gray-800 px-4 py-2 rounded-md shadow-sm hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 flex items-center">
                <Icon name="heroicons:arrow-path" class="w-5 h-5 mr-2" /> Reset Filters
              </button>
              <button @click="fetchHousesReport" class="bg-blue-600 text-white px-4 py-2 rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 flex items-center">
                <Icon name="heroicons:magnifying-glass" class="w-5 h-5 mr-2" />
                Generate
              </button>
            </div>
          </div>

          <!-- Table -->
          <div v-if="isLoading" class="flex justify-center items-center h-64">
            <Icon name="svg-spinners:3-dots-fade" class="w-12 h-12 text-blue-600" />
          </div>
          <div v-else-if="housesReportData.length > 0" class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">House No.</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Street</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Veng</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Landlord</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Household Size</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Awmtan Kum</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Has Tenants</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">No. of Tenants</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="house in housesReportData" :key="house.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ house.house_number }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ house.street || 'N/A' }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ house.veng }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ house.landlord_name || 'N/A' }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ house.household_size || 'N/A' }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ house.awmtan_kum || 'N/A' }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ house.have_tenant ? 'Yes' : 'No' }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ house.tenants.length }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <span :class="[house.is_verified ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800', 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium']">
                      {{ house.is_verified ? 'Verified' : 'Not Verified' }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="text-center py-16">
            <Icon name="heroicons:document-magnifying-glass" class="w-12 h-12 mx-auto text-gray-400" />
            <h3 class="mt-2 text-sm font-medium text-gray-900">No Data</h3>
            <p class="mt-1 text-sm text-gray-500">Adjust your filters or generate a new report.</p>
          </div>

          <!-- Houses Report Summary Statistics -->
          <div v-if="housesReportData.length > 0" class="mt-8 p-6 bg-white rounded-lg shadow-lg border border-gray-200">
            <h3 class="text-xl font-semibold text-gray-800 mb-4">Filtered Houses Statistics</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div class="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-lg">
                <h4 class="text-lg font-medium text-gray-700">Total Filtered Houses</h4>
                <p class="text-3xl font-bold text-blue-900 mt-1">{{ totalFilteredHouses }}</p>
              </div>

              <div class="bg-green-50 border-l-4 border-green-500 p-4 rounded-lg">
                <h4 class="text-lg font-medium text-gray-700">Veng Distribution</h4>
                <ul class="list-disc list-inside text-gray-800 mt-1">
                  <li v-for="(count, veng) in vengDistributionHouses" :key="veng">{{ veng }}: {{ count }}</li>
                </ul>
              </div>

              <div class="bg-purple-50 border-l-4 border-purple-500 p-4 rounded-lg">
                <h4 class="text-lg font-medium text-gray-700">Ownership Distribution</h4>
                <ul class="list-disc list-inside text-gray-800 mt-1">
                  <li v-for="(count, ownership) in ownershipDistribution" :key="ownership">{{ ownership }}: {{ count }}</li>
                </ul>
              </div>

              <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded-lg">
                <h4 class="text-lg font-medium text-gray-700">Tenancy Status</h4>
                <ul class="list-disc list-inside text-gray-800 mt-1">
                  <li v-for="(count, tenancy) in tenancyDistribution" :key="tenancy">{{ tenancy }}: {{ count }}</li>
                </ul>
              </div>

              <div class="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
                <h4 class="text-lg font-medium text-gray-700">Average Household Size</h4>
                <p class="text-3xl font-bold text-red-900 mt-1">{{ averageHouseholdSize }}</p>
              </div>
            </div>
          </div>
        </div>


      </div>
    </div>
    </div>
</template>

<script setup>
import { ref, onMounted, reactive, watch, computed } from 'vue';
import { useNuxtApp } from '#app';

 

const { $api } = useNuxtApp()

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
});

const activeReport = ref('persons');
const isLoading = ref(false);

// Data stores
const summaryData = ref(null);
const personsReportData = ref([]);
const personsStatistics = ref(null);
const housesReportData = ref([]);
const housesStatistics = ref(null);
const vengs = ref([]);
const religions = ref([]);
const denominations = ref([]);
const educations = ref([]);
const occupations = ref([]);

const bloodGroups = [
  'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'
];

// Filter models
const personFilters = reactive({
  gender: '',
  min_age: null,
  max_age: null,
  street: '',
  marital_status: '',
  blood_group: '',
  religion_id: '',
  denomination_id: '',
  education_id: '',
  occupation_id: '',
  is_verified: null,
  veng_id: ''
});

const initialPersonFilters = { ...personFilters }; // Store initial state

const houseFilters = reactive({
  is_verified: null, // null for all, true for verified, false for not
  veng_id: '',
  street: '',
  is_owner: null,
  have_tenant: null,
  is_tenant: null,
  house_number_search: '',
  landlord_name_search: '',
  household_size: null,
  rent_start_date: '',
  landlord_veng: '',
});

const initialHouseFilters = { ...houseFilters }; // Store initial state

const resetPersonFilters = () => {
  Object.assign(personFilters, initialPersonFilters);
  fetchPersonsReport();
};

const resetHouseFilters = () => {
  Object.assign(houseFilters, initialHouseFilters);
  fetchHousesReport();
};

const setActiveReport = (reportName) => {
  activeReport.value = reportName;
  // Reset data when switching tabs
  personsReportData.value = [];
  housesReportData.value = [];
  // Fetch summary data if that tab is selected
  if (reportName === 'summary' && !summaryData.value) {
    fetchSummaryReport();
  }
};

const fetchSummaryReport = async () => {
  isLoading.value = true;
  try {
    const response = await $api.get('/reports/summary');
    summaryData.value = response.data;
  } catch (error) {
    console.error('Failed to fetch summary report:', error);
    // Handle error display to user
  } finally {
    isLoading.value = false;
  }
};

const fetchPersonsReport = async () => {
  isLoading.value = true;
  personsReportData.value = [];
  personsStatistics.value = null;
  try {
    const params = new URLSearchParams();
    Object.entries(personFilters).forEach(([key, value]) => {
      if (value !== null && value !== '') {
        params.append(key, value);
      }
    });
    
    const response = await $api.get(`/reports/persons?${params.toString()}`);
    personsReportData.value = response.data.persons;
    personsStatistics.value = response.data.statistics;
  } catch (error)
{
    console.error('Failed to fetch persons report:', error);
  } finally {
    isLoading.value = false;
  }
};

const fetchHousesReport = async () => {
  isLoading.value = true;
  housesReportData.value = [];
  housesStatistics.value = null;
  try {
    const params = new URLSearchParams();
    Object.entries(houseFilters).forEach(([key, value]) => {
      if (value !== null && value !== '') {
        params.append(key, value);
      }
    });

    const response = await $api.get(`/reports/houses?${params.toString()}`);
    housesReportData.value = response.data.houses;
    housesStatistics.value = response.data.statistics;
  } catch (error) {
    console.error('Failed to fetch houses report:', error);
  } finally {
    isLoading.value = false;
  }
};

const fetchDropdownData = async () => {
  try {
    const [vengRes, religionRes, denominationRes, educationRes, occupationRes] = await Promise.all([
      $api.get('/veng/'),
      $api.get('/religion/'),
      $api.get('/denomination/'),
      $api.get('/qualifications/'),
      $api.get('/occupations/')
    ]);
    vengs.value = vengRes.data;
    religions.value = religionRes.data;
    denominations.value = denominationRes.data;
    educations.value = educationRes.data;
    occupations.value = occupationRes.data;
  } catch (error) {
    console.error('Failed to fetch dropdown data:', error);
  }
};

const totalFilteredCitizens = computed(() => personsStatistics.value?.total_citizens || 0);

const genderDistribution = computed(() => {
  return personsStatistics.value?.gender_distribution || {};
});

const religionDistribution = computed(() => {
  return personsStatistics.value?.religion_distribution || {};
});

const denominationDistribution = computed(() => {
  return personsStatistics.value?.denomination_distribution || {};
});

const educationDistribution = computed(() => {
  return personsStatistics.value?.education_distribution || {};
});

const occupationDistribution = computed(() => {
  return personsStatistics.value?.occupation_distribution || {};
});

// Houses Report Computed Properties
const totalFilteredHouses = computed(() => housesStatistics.value?.total_houses || 0);

const vengDistributionHouses = computed(() => {
  return housesStatistics.value?.veng_distribution || {};
});

const ownershipDistribution = computed(() => {
  return housesStatistics.value?.ownership_distribution || {};
});

const tenancyDistribution = computed(() => {
  return housesStatistics.value?.tenancy_distribution || {};
});

const averageHouseholdSize = computed(() => {
  return housesStatistics.value?.average_household_size || 0;
});

onMounted(() => {
  // fetchSummaryReport();
  fetchDropdownData();
});
// Watch for changes in summaryData to update chart options



</script>

<style scoped>
/* Using Tailwind CSS utility classes, so limited custom CSS is needed. */
/* Minor tweaks for better form element alignment if necessary */
.self-end {
  align-self: flex-end;
}
</style>


