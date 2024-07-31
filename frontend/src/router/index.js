// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import SponsorView from '../views/SponsorView.vue'
import InfluencerView from '../views/InfluencerView.vue'
import AdminView from '../views/AdminView.vue'
import SearchView from '../views/SearchView.vue'
import CampaignView from '../views/CampaignView.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  {
    path: '/sponsor',
    name: 'sponsor',
    component: SponsorView
  },
  {
    path: '/influencer',
    name: 'influencer',
    component: InfluencerView
  },
  {
    path: '/campaign/:id',
    name: 'campaign',
    component: CampaignView
  },
  {
    path: '/search',
    name: 'search',
    component: SearchView
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminView
  },
  {
    path: '/:pathMatch(.*)*', // Catch-all route for undefined paths
    redirect: '/login'
  }
]

const baseUrl = process.env.BASE_URL || '/login'; // Fallback to '/' if BASE_URL is undefined
console.log('BASE_URL:', baseUrl);

const router = createRouter({
  history: createWebHistory(baseUrl),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const role = localStorage.getItem('role')
  const email = localStorage.getItem('email')

  if((!token || !role || !email) && to.name !== 'login' && to.name !== 'register'){
    localStorage.removeItem('token')
    localStorage.removeItem('role')
    localStorage.removeItem('email')
    next({ name: 'login' })
  }

  if (to.name === 'sponsor' && role !== 'sponsor') {
    // Wrong dashboard for role
    next({ name: role === 'influencer' ? 'influencer' : role === 'admin' ? 'admin' : 'login' })
  } else if (to.name === 'influencer' && role !== 'influencer') {
    // Wrong dashboard for role
    next({ name: role === 'sponsor' ? 'sponsor' : role === 'admin' ? 'admin' : 'login' })
  } else if (to.name === 'admin' && role !== 'admin') {
    // Wrong dashboard for role
    next({ name: role === 'sponsor' ? 'sponsor' : role === 'influencer' ? 'influencer' : 'login' })
  } else if(to.name === 'logout'){
    // Logout
    localStorage.removeItem('token')
    localStorage.removeItem('role')
    localStorage.removeItem('email')
    next({ name: 'login' })
  }else {
    // Continue to route
    next()
  }
})

export default router