import { Bar, Line, Pie, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  RadialLinearScale // For RadarChart if needed later
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  RadialLinearScale
)

export default defineNuxtPlugin(nuxtApp => {
  nuxtApp.vueApp.component('BarChart', Bar)
  nuxtApp.vueApp.component('LineChart', Line)
  nuxtApp.vueApp.component('PieChart', Pie)
  nuxtApp.vueApp.component('DoughnutChart', Doughnut)
})
