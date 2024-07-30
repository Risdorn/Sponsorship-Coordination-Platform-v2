<template>
    <NavBar :name="user.name" role="sponsor" :flag="flag"/>
        
    <div style="margin-top: 56px;">
        <!-- Error message display -->
        <div v-if="success" class="alert alert-success" role="alert">
            {{ success }}
        </div>
        <div v-else-if="error" class="alert alert-danger" role="alert">
            {{ error }}
        </div>
        <!-- Flag message display -->
        <div v-if="flag" class="alert alert-danger" role="alert">
            You have been flagged, kindly make the below changes before your profile can be activated again.<br>
            Reason: {{ flag.reason }}
        </div>

        <div v-if="loading" class="text-center">
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
        <div v-else>
            <!-- Profile Page -->
            <ProfilePage :user="user" :flag="flag"/>

            <div v-if="!flag">
                <!-- Campaigns Page -->
                <CampaignList role="sponsor" :campaignPage="campaignPage" :sponsor_id="user.id" :campaigns="campaigns" @update-campaigns="updateCampaigns"/>
            </div>            
        </div>
    </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import ProfilePage from '../components/ProfilePage.vue';
import CampaignList from '../components/CampaignList.vue';

export default {
name: 'SponsorView',
data() {
    return {
        user: null,
        flag: null,
        success: null,
        error: null,
        loading: true,
        campaigns: [],
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
        } catch (error) {
            this.error = error.message;
        } finally {
            this.loading = false;
        }
    },
    async campaignPage(page) {
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
            return data;
        } catch (error) {
            this.error = error.message;
        }
    },
    async adRequestPage(page) {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:5000/api/ad_requests', {
                method: 'GET',
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
            return data;
        } catch (error) {
            this.error = error.message;
        }
    },
    updateCampaigns(updatedCampaigns) {
        this.campaigns = updatedCampaigns;
        console.log(this.campaigns);
    }
},
components: {
    NavBar,
    ProfilePage,
    CampaignList,
},
created() {
    this.user = this.getUser();
    console.log(this.user);
}
}
</script>