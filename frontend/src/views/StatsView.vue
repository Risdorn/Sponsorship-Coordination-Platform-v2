<template>
    <div v-if="loading" class="text-center">
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>
    <div v-else>
            <NavBar :name="user.name" :role="user.role" :flag="user.flag"/>
        <div style="margin-top: 56px;">
          <!-- Flag message display -->
          <div v-if="user.flag" class="alert alert-danger" role="alert">
              You have been flagged, kindly make the below changes before your profile can be activated again.<br>
              Reason: {{ user.reason }}
          </div>
          <div v-else>
            <div v-if="user.role == 'admin'" id="User_Graph">
                <img :src="'data:image/png;base64,' + user_over_time" alt="Users Over Time">
            </div>
            <div v-if="user.role != 'influencer'" id="Campaign_Graph">
                <img :src="'data:image/png;base64,' + campaigns_over_time" alt="Campaigns Over Time">
            </div>

            <div id="Ad_Request_Graph">
                <img :src="'data:image/png;base64,' + ad_requests_over_time" alt="Ad Requests Over Time">
            </div>

            <div>
                <img :src="'data:image/png;base64,' + ad_request_status" alt="Ad Request Status">
                <img :src="'data:image/png;base64,' + payment_distribution" alt="Payment Amount Distribution">
            </div>
          </div>
        </div>
    </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';

export default {
  name: 'StatsView',
  data() {
    return {
        user: null,
        user_over_time: null,
        campaigns_over_time: null,
        ad_requests_over_time: null,
        ad_request_status: null,
        payment_distribution: null,
        loading: true
    }
  },
  methods: {
    async fetchStats() {
      try {
        const email = localStorage.getItem('email');
        const response = await fetch('http://localhost:5000/api/user/stats/' + email, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('token')
          }
        });
        const data = await response.json();
        if(!response.ok) {
          throw new Error(`${data.detail}`);
        }
        this.user = data.user;
        this.user.role = this.user.role.toLowerCase();
        this.user_over_time = data.user_over_time;
        this.campaigns_over_time = data.campaigns_over_time;
        this.ad_requests_over_time = data.ad_requests_over_time;
        this.ad_request_status = data.ad_request_status;
        this.payment_distribution = data.payment_distribution;
        } catch (error) {
            console.error(error);
        } finally {
            this.loading = false;
        }
    },
  },
  created() {
    this.fetchStats();
  },
  components: {
    NavBar
  }
}
</script>