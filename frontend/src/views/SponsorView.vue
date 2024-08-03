<template>
    <div v-if="loading" class="text-center">
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>
    <div v-else>
        <NavBar :name="user.name" role="sponsor" :flag="user.flag"/>
            
        <div style="margin-top: 56px;">
            <!-- Error message display -->
            <div v-if="success" class="alert alert-success" role="alert">
                {{ success }}
            </div>
            <div v-else-if="error" class="alert alert-danger" role="alert">
                {{ error }}
            </div>
            <!-- Flag message display -->
            <div v-if="user.flag" class="alert alert-danger" role="alert">
                You have been flagged, kindly make the below changes before your profile can be activated again.<br>
                Reason: {{ user.reason }}
            </div>

            <div v-else>
                <!-- Profile Page -->
                <ProfilePage :user="user" @error="error_message" @success="success_message"/>

                <div v-if="!flag">
                    <!-- Campaigns Page -->
                    <CampaignList v-if="!campaign_loading" role="sponsor" :sponsor_id="user.id" :campaigns="campaigns" :campaign="campaign" 
                    @update-campaigns="campaignPage" @update-campaign="updateCampaign" @error="error_message" @success="success_message"/>

                    <!-- Ad Requests Page -->
                    <AdRequestList v-if="!ad_loading" role="sponsor" :ad_requests="adRequests" :ad_request="ad_request" 
                    @update-adRequests="adRequestPage" @update-adRequest="updateAdRequest" @error="error_message" @success="success_message"/>
                </div>            
            </div>
        </div>
    </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import ProfilePage from '../components/ProfilePage.vue';
import CampaignList from '../components/CampaignList.vue';
import AdRequestList from '../components/AdRequestList.vue';

export default {
name: 'SponsorView',
data() {
    return {
        user: null,
        success: null,
        error: null,
        loading: true,
        campaign_loading: true,
        campaigns: [],
        campaign: null,
        ad_loading: true,
        adRequests: [],
        ad_request: null
    }
},
methods: {
    async getUser() {
        try {
            const token = localStorage.getItem('token');
            const email = localStorage.getItem('email');
            const response = await fetch('http://localhost:5000/api/user/' + email, {
                method: 'GET',
                headers: {
                    'Authentication-Token': token
                }
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Failed to fetch user');
            }
            this.user = data;
            console.log(this.user);
        } catch (error) {
            this.error = error.message;
        }
    },
    async campaignPage(page) {
        this.campaign_loading = true;
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:5000/api/campaign/search', {
                method: 'POST',
                headers: {
                    'Authentication-Token': token,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    sponsor_id: this.user.id,
                    page: page
                })
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Failed to fetch campaigns');
            }
            this.campaigns = data;
        } catch (error) {
            this.error = error.message;
        } finally {
            this.campaign_loading = false;
        }
    },
    async adRequestPage(page) {
        this.ad_loading = true;
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:5000/api/ad_requests', {
                method: 'POST',
                headers: {
                    'Authentication-Token': token,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    sponsor_id: this.user.id,
                    page: page
                })
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Failed to fetch ad requests');
            }
            this.adRequests = data;
        } catch (error) {
            this.error = error.message;
        } finally {
            console.log(this.adRequests);
            this.ad_loading = false;
        }
    },
    async updateCampaign(campaign_id) {
        const id = campaign_id;
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:5000/api/campaign/' + id, {
                method: 'GET',
                headers: {
                    'Authentication-Token': token
                }
            })
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Failed to fetch campaign');
            }
            this.campaign = data;
        } catch (error) {
            this.error = error.message;
        }
        console.log(this.campaign);
    },
    async updateAdRequest(ad_request_id) {
        const id = ad_request_id;
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:5000/api/ad_request/' + id, {
                method: 'GET',
                headers: {
                    'Authentication-Token': token
                }
            })
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Failed to fetch ad request');
            }
            this.ad_request = data;
        } catch (error) {
            this.error = error.message;
        }
    },
    async initializePage(){
        await this.getUser();
        await this.campaignPage(1);
        await this.adRequestPage(1);
        this.campaign = {'name': '', 'description': '', 'start_date': '', 'end_date': '', 'budget': -1, 'goals': '', 'visibility': ''};
        this.ad_request = {'messages':'', 'requirements':'', 'payment_amount':-1, 'campaign':{'name':''}, 'influencer':{'name':''}};
        this.loading = false;
    },
    error_message(message){
        this.error = message;
        this.success = null;
    },
    success_message(message){
        this.success = message;
        this.error = null;
    }
},
components: {
    NavBar,
    ProfilePage,
    CampaignList,
    AdRequestList
},
created() {
    this.initializePage();
}
}
</script>