<template>
    <div v-if="loading" class="text-center">
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>
    <div v-else>
        <NavBar :name="user.name" role="admin"/>

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
            <UserList v-if="!user_loading" :users="users" :role="user.role"
            @update-users="userPage" @error="error_message" @success="success_message"/>

            <!-- Campaigns -->
            <CampaignList v-if="!campaign_loading" :campaigns="campaigns" :role="user.role"
            @update-campaigns="campaignPage" @error="error_message" @success="success_message"/>

            <!-- Ad Requests -->
            <AdRequestList v-if="!ad_request_loading" :ad_requests="adRequests" :role="user.role"
            @update-adRequests="adRequestPage" @error="error_message" @success="success_message"/>

            <!-- Flagged User -->
            <FlaggedList v-if="!flagged_loading" :flagged="flagged" @update-flagged="flaggedPage"
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
        user: null,
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
        await this.getUser();
        await this.userPage(1);
        await this.campaignPage(1);
        await this.adRequestPage(1);
        await this.flaggedPage(1);
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