<template>
    <div v-if="!loading">

        <!-- Navigation Bar -->
        <NavBar :name="user.name" role="influencer" :flag="flag"/>

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

            <!-- Profile Page -->
            <ProfilePage :user="user" :flag="flag"/>

            <div v-if="!flag">
            <!-- Ad Requests Page -->
            <AdRequestList role="influencer" :adRequestPage="adRequestPage" :ad_requests="adRequests" :ad_request="ad_request" 
            @update-adRequests="updateAdRequests" @update-adRequest="updateAdRequest"/>
            </div>

        </div>
    </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import ProfilePage from '../components/ProfilePage.vue';
import AdRequestList from '../components/AdRequestList.vue';

export default {
name: 'InfluencerView',
data() {
    return {
        user: null,
        flag: null,
        success: null,
        error: null,
        loading: true,
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
        } catch (error) {
            this.error = error.message;
        } finally {
            this.loading = false;
        }
    },
    async adRequestPage(page) {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:5000/api/ad_requests', {
                method: 'POST',
                headers: {
                    'Authentication-Token': token,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    influencer_id: this.user.id, 
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
    async updateAdRequests(data) {
        this.adRequests = data;
    },
    async updateAdRequest(id) {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:5000/api/ad_request/' + id, {
                method: 'GET',
                headers: {
                    'Authentication-Token': token
                }
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Failed to fetch ad request');
            }
            this.ad_request = data;
        } catch (error) {
            this.error = error.message;
        }
    }
},
created() {
    this.getUser();
    this.ad_request = {'messages':'', 'requirements':'', 'payment_amount':-1, 'campaign':{'name':''}, 'influencer':{'name':''}};
},
components: {
    NavBar,
    ProfilePage,
    AdRequestList
}
}
</script>