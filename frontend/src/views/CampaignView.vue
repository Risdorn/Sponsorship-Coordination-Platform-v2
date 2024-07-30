<template>
    <!-- Navigation bar -->
    <NavBar :name="user.name" :role="user.role" :flag="flag" />

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
        {% if ad_requests.items | length == 0 %}
        <div class="alert alert-warning" role="alert">
            No Ad Requests sent yet.<br>
            Campaign will not show up on search results.
        </div>
        {% endif %}
        <p><b>Category</b>: {{ campaign.category }}</p>
        <p><b>Description</b>: {{ campaign.description }}</p>
        <p><b>Goals</b>: {{ campaign.goals }}</p>
        <p><b>Visibility</b>: {{ campaign.visibility }}</p>
        <p><b>Budget</b>: {{ campaign.budget }}</p>
        <p>Active from <b>{{ campaign.start_date }}</b> to <b>{{ campaign.end_date }}</b></p>
        <p><b>Remaining Budget</b>: {{ campaign.remaining }}</p>
        {% if user.role == "Sponsor" or user.role == "Admin" %}
        <p><b>Total Ad Requests</b>: {{ ad_requests.total }}</p>
        {% endif %}
        <div class="progress">
            <div class="progress-bar" role="progressbar" style="width: {{ ((campaign.budget - campaign.remaining)/campaign.budget * 100)|round(2) }}%;" 
            aria-valuenow="{{ ((campaign.budget - campaign.remaining)/campaign.budget * 100)|round(2) }}" aria-valuemin="0" aria-valuemax="100">{{ ((campaign.budget - campaign.remaining)/campaign.budget * 100)|round(2) }}%</div>
        </div>
    </div>

    <!-- Ad Requests -->
    <AdRequestList :adRequestPage="adRequestPage" campaigns="" :role="user.role" /> 

    </div>
</template>

<script>
import AdRequestList from '@/components/AdRequestList.vue';


export default {
  name: 'CampaignView',
  data() {
    return {
      campaign: null,
    };
  },
  async created() {
    const campaignId = this.$route.params.id;
    const response = await fetch(`/api/campaigns/${campaignId}`);
    this.campaign = await response.json();
  },
};
</script>