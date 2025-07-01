<template>
  <div class="min-h-screen bg-gray-50 font-sans text-gray-800">
    <!-- Hero Section -->
    <section class="relative bg-gradient-to-r from-blue-600 to-purple-700 text-white py-20 md:py-32 overflow-hidden">
      <div class="absolute inset-0 z-0 opacity-10">
        <svg class="w-full h-full" viewBox="0 0 1440 320" preserveAspectRatio="none" fill="currentColor">
          <path d="M0,160L48,176C96,192,192,224,288,208C384,192,480,128,576,106.7C672,85,768,107,864,133.3C960,160,1056,192,1152,192C1248,192,1344,160,1392,144L1440,128L1440,0L1392,0C1344,0,1248,0,1152,0C1056,0,960,0,864,0C768,0,672,0,576,0C480,0,384,0,288,0C192,0,96,0,48,0L0,0Z"></path>
        </svg>
      </div>
      <div class="container mx-auto px-6 relative z-10 text-center">
        <h1 class="text-4xl md:text-6xl font-extrabold leading-tight mb-4 animate-fade-in-up">
          AMC Citizen Management System: Empowering Local Councils
        </h1>
        <p class="text-lg md:text-xl mb-8 max-w-3xl mx-auto opacity-90 animate-fade-in-up animation-delay-200">
          Efficiently manage citizen data for Local Councils and AMC Wards with our secure and comprehensive platform.
        </p>
        <button class="bg-white text-blue-700 hover:bg-blue-100 transition duration-300 ease-in-out font-bold py-3 px-8 rounded-full shadow-lg transform hover:scale-105 animate-fade-in-up animation-delay-400">
          Learn More
        </button>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-16 md:py-24 bg-white">
      <div class="container mx-auto px-6">
        <h2 class="text-3xl md:text-4xl font-bold text-center mb-12 text-gray-900">
          Key Features for Comprehensive Citizen Management
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-10">
          <div class="bg-white p-8 rounded-lg shadow-md hover:shadow-xl transition duration-300 ease-in-out transform hover:-translate-y-2">
            <div class="text-blue-500 mb-4 text-5xl text-center">
              <i class="fas fa-users"></i> <!-- Icon for Citizen Data -->
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-3 text-center">Centralized Citizen Data</h3>
            <p class="text-gray-600 text-center">
              Maintain a single, secure repository for all citizen information and interactions.
            </p>
          </div>
          <div class="bg-white p-8 rounded-lg shadow-md hover:shadow-xl transition duration-300 ease-in-out transform hover:-translate-y-2">
            <div class="text-green-500 mb-4 text-5xl text-center">
              <i class="fas fa-cogs"></i> <!-- Icon for Workflow Automation -->
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-3 text-center">Streamlined Workflows</h3>
            <p class="text-gray-600 text-center">
              Automate administrative tasks and improve the efficiency of public services.
            </p>
          </div>
          <div class="bg-white p-8 rounded-lg shadow-md hover:shadow-xl transition duration-300 ease-in-out transform hover:-translate-y-2">
            <div class="text-purple-500 mb-4 text-5xl text-center">
              <i class="fas fa-chart-bar"></i> <!-- Icon for Reporting & Analytics -->
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-3 text-center">Advanced Reporting & Analytics</h3>
            <p class="text-gray-600 text-center">
              Gain valuable insights into citizen demographics and service utilization with robust reporting.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonial Section -->
    <section class="py-16 md:py-24 bg-gray-100">
      <div class="container mx-auto px-6 text-center">
        <h2 class="text-3xl md:text-4xl font-bold mb-12 text-gray-900">
          What Our Local Councils Say
        </h2>
        <div class="max-w-2xl mx-auto bg-white p-8 rounded-lg shadow-lg">
          <p class="text-xl italic text-gray-700 mb-6">
            "The AMC Citizen Management System has transformed how we interact with our citizens, making our services more responsive and effective. A vital tool for modern governance."
          </p>
          <p class="font-semibold text-gray-800">- Local Council Administrator</p>
        </div>
      </div>
    </section>

    <!-- Call to Action Section -->
    <section class="py-16 md:py-24 bg-gradient-to-r from-blue-700 to-purple-800 text-white text-center">
      <div class="container mx-auto px-6">
        <h2 class="text-3xl md:text-4xl font-bold mb-6">Ready to Optimize Citizen Services?</h2>
        <p class="text-lg md:text-xl mb-8 opacity-90">
          Join other Local Councils and AMC Wards in modernizing your citizen management.
        </p>
        <button class="bg-white text-blue-700 hover:bg-blue-100 transition duration-300 ease-in-out font-bold py-3 px-8 rounded-full shadow-lg transform hover:scale-105">
          Get Started Today
        </button>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-800 text-gray-300 py-8">
      <div class="container mx-auto px-6 text-center">
        <p>&copy; 2025 AMC Citizen Management System. All rights reserved.</p>
        <div class="flex justify-center space-x-6 mt-4">
          <a href="#" class="hover:text-white transition duration-300">Privacy Policy</a>
          <a href="#" class="hover:text-white transition duration-300">Terms of Service</a>
          <a href="#" class="hover:text-white transition duration-300">Contact Us</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'LandingPage',
  head() {
    return {
      title: 'AMC Citizen Management System',
      meta: [
        {
          hid: 'description',
          name: 'description',
          content: 'Secure and efficient Citizen Management System for Local Councils and AMC Wards.'
        }
      ]
    }
  }
}
</script>

<style scoped>
/* Add any custom styles here if needed, though Tailwind should handle most. */
/* Example for animations */
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fade-in-up 0.6s ease-out forwards;
}

.animation-delay-200 {
  animation-delay: 0.2s;
}

.animation-delay-400 {
  animation-delay: 0.4s;
}
</style>
