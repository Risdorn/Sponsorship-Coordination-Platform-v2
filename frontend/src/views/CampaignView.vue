<template>
  <div v-if="!loading">
    <!-- Navigation bar -->
    <NavBar :name="user.name" :role="user.role" :flag="flag"/>

    <div style="margin-top: 56px;">
    
    <!-- Error message display -->
    <div v-if="success" class="alert alert-success" role="alert">
        {{ success }}
    </div>
    <div v-if="error" class="alert alert-danger" role="alert">
        {{ error }}
    </div>

    <!-- Campaign details -->
    <div class="Campaign">
        <h3>{{ campaign.name }}</h3>
        <div v-if="campaign.length == 0" class="alert alert-warning" role="alert">
            No Ad Requests sent yet.<br>
            Campaign will not show up on search results.
        </div>
        <p><b>Category</b>: {{ campaign.category }}</p>
        <p><b>Description</b>: {{ campaign.description }}</p>
        <p><b>Goals</b>: {{ campaign.goals }}</p>
        <p><b>Visibility</b>: {{ campaign.visibility }}</p>
        <p><b>Budget</b>: {{ campaign.budget }}</p>
        <p>Active from <b>{{ campaign.start_date }}</b> to <b>{{ campaign.end_date }}</b></p>
        <p><b>Remaining Budget</b>: {{ campaign.remaining }}</p>
        <div class="progress">
            <div class="progress-bar" role="progressbar" :style="{ width: campaign.progress + '%' }" 
            :aria-valuenow="campaign.progress" aria-valuemin="0" aria-valuemax="100">{{ campaign.progress }}%</div>
        </div>
    </div><br>

    <button type="button" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addAdRequest">
      Add Ad Request
    </button>
    <!-- Add Ad Request Modal -->
    <div class="modal fade" id="addAdRequest" tabindex="-1" role="dialog" aria-labelledby="addAdRequestLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <form id="add_ad_request">
                    <div class="modal-header">
                        <h5 class="modal-title" id="addAdRequestLabel">Add Ad Request</h5>
                    </div>
                    <div class="modal-body">
                        <input type="hidden" name="form_id" value="add_ad_request">
                        <!-- Messages input -->
                        <div data-mdb-input-init class="form-outline mb-4">
                            <input type="text" name="messages" id="messages" v-model="messages" class="form-control" required maxlength=250/>
                            <label class="form-label" for="messages">Messages</label>
                        </div>

                        <!-- Requirements input -->
                        <div data-mdb-input-init class="form-outline mb-4">
                            <input type="text" id="requirements" name="requirements" v-model="requirements" class="form-control" required maxlength=250/>
                            <label class="form-label" for="requirements">Requirements</label>
                        </div>

                        <!-- Payment Amount input -->
                        <div data-mdb-input-init class="form-outline mb-4">
                            <input type="number" id="payment_amount" name="payment_amount" v-model="payment_amount" class="form-control" required min=0/>
                            <label class="form-label" for="payment_amount">Payment Amount</label>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button class="btn btn-success" @click="addAdRequest">Add Ad Request</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- Ad Requests -->
    <AdRequestList :role="user.role" :adRequestPage="adRequestPage" :ad_requests="adRequests" :ad_request="ad_request" 
    @update-adRequests="updateAdRequests" @update-adRequest="updateAdRequest"/>

    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import AdRequestList from '../components/AdRequestList.vue';

export default {
  name: 'CampaignView',
  data() {
    return {
      campaign: null,
      user: null,
      messages: '',
      requirements: '',
      payment_amount: -1,
      loading: true,
      error: null,
      success: null,
      flag: null,
      adRequests: [],
      ad_request: null,
    };
  },
  methods: {
    async getUser() {
      const email = localStorage.getItem('email');
      const response = await fetch('http://localhost:5000/api/user/' + email, {
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('token'),
        },
      });
      this.user = await response.json();
    },
    async getCampaign() {
      const campaignId = this.$route.params.id;
      const response = await fetch('http://localhost:5000/api/campaign/' + campaignId, {
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('token'),
        },
      });
      this.campaign = await response.json();
    },
    async addAdRequest(event){
      event.preventDefault();
      try {
        const response = await fetch('http://localhost:5000/api/ad_request', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('token'),
          },
          body: JSON.stringify({
            campaign_id: this.campaign.id,
            messages: this.messages,
            requirements: this.requirements,
            payment_amount: this.payment_amount
          })
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.message || 'Failed to add ad request');
        }
        this.success = 'Ad request added successfully';
        this.messages = '';
        this.requirements = '';
        this.payment_amount = -1;
        this.$router.go();
      } catch (error) {
        this.error = error.message;
      }
    },
    async adRequestPage(page){
      try {
        console.log("adRequestPage");
        const response = await fetch('http://localhost:5000/api/ad_requests', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('token'),
          },
          body: JSON.stringify({
            campaign_id: this.campaign.id,
            page: page
          })
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.message || 'Failed to fetch ad requests');
        }
        return data;
      } catch (error) {
        this.error = error.message;
      }
    },
    updateAdRequests(adRequests) {
      this.adRequests = adRequests;
    },
    async updateAdRequest(id) {
      try {
        const response = await fetch('http://localhost:5000/api/ad_request/' + id, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('token'),
          },
        });
        this.ad_request = await response.json();
      } catch (error) {
        this.error = error.message;
      }
    }
  },
  async created() {
    await this.getUser();
    this.user.role = this.user.role.toLowerCase();
    await this.getCampaign();
    this.ad_request = {'messages':'', 'requirements':'', 'payment_amount':-1, 'campaign':{'name':''}, 'influencer':{'name':''}};
    console.log(this.campaign);
    console.log(this.user);
    this.loading = false;
  },
  components: {
    NavBar,
    AdRequestList,
  },
};
</script>