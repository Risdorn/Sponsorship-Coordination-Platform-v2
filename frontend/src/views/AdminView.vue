<template>
    <div v-if="loading" class="text-center">
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>
    <div v-else>
        <NavBar name="Admin" role="admin"/>

        <div style="margin-top: 56px;">

            <!-- Error Message Display -->
            <div v-if="success" class="alert alert-success" role="alert">
                {{ success }}
            </div>
            <div v-else-if="error" class="alert alert-danger" role="alert">
                {{ error }}
            </div>

            <!-- Profile -->
            <div id="Profile">
                <h1>Welcome Admin</h1>
            </div>

            <!-- Users -->
            <UserList v-if="!user_loading" :users="users" role="admin"
            @update-users="userPage" @error="error_message" @success="success_message"/>

            <!-- Campaigns -->
            <CampaignList v-if="!campaign_loading" :campaigns="campaigns" role="admin"
            @update-campaigns="campaignPage" @error="error_message" @success="success_message"/>

            <!-- Ad Requests -->
            <AdRequestList v-if="!ad_request_loading" :ad_requests="adRequests" role="admin"
            @update-adRequests="adRequestPage" @error="error_message" @success="success_message"/>

            <!-- Flagged User -->
            <FlaggedList v-if="!flagged_loading" :flags="flagged" @update-flagged="flaggedPage"
            @error="error_message" @success="success_message"/>
        </div>
    </div>
</template>

<script>
import AdRequestList from '../components/AdRequestList.vue';
import CampaignList from '../components/CampaignList.vue';
import UserList from '../components/UserList.vue';
import NavBar from '../components/NavBar.vue';
import FlaggedList from '../components/FlaggedList.vue';

export default {
name: 'AdminView',
data() {
    return {
        users: [],
        campaigns: [],
        adRequests: [],
        flagged: [],
        success: null,
        error: null,
        loading: true,
        user_loading: true,
        campaign_loading: true,
        ad_request_loading: true,
        flagged_loading: true
    }
},
methods: {
    async userPage(page) {
        this.user_loading = true;
        try {
            const response = await fetch('http://localhost:5000/api/users', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('token'),
                },
                body: JSON.stringify({ page: page })
            });
            this.users = await response.json();
        } catch (error) {
            this.error = error.message;
        } finally {
            this.user_loading = false;
        }
    },
    async campaignPage(page) {
        this.campaign_loading = true;
        try {
            const response = await fetch('http://localhost:5000/api/campaigns', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('token'),
                },
                body: JSON.stringify({ page: page })
            });
            this.campaigns = await response.json();
        } catch (error) {
            this.error = error.message;
        } finally {
            this.campaign_loading = false;
        }
    },
    async adRequestPage(page) {
        this.ad_request_loading = true;
        try {
            const response = await fetch('http://localhost:5000/api/ad_requests', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('token'),
                },
                body: JSON.stringify({ page: page })
            });
            this.adRequests = await response.json();
        } catch (error) {
            this.error = error.message;
        } finally {
            this.ad_request_loading = false;
        }
    },
    async flaggedPage(page) {
        this.flagged_loading = true;
        try {
            const response = await fetch('http://localhost:5000/api/users/flagged', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('token'),
                },
                body: JSON.stringify({ page: page })
            });
            this.flagged = await response.json();
        } catch (error) {
            this.error = error.message;
        } finally {
            this.flagged_loading = false;
        }
    },
    async initializePage(){
        await this.userPage(1);
        await this.campaignPage(1);
        await this.adRequestPage(1);
        await this.flaggedPage(1);
        console.log(this.flagged);
        this.loading = false;
    },
    error_message(message) {
        this.error = message;
        this.success = null;
    },
    success_message(message) {
        this.success = message;
        this.error = null;
    }
},
components: {
    AdRequestList,
    CampaignList,
    UserList,
    NavBar,
    FlaggedList
},
created() {
    this.initializePage();
}
}
</script>