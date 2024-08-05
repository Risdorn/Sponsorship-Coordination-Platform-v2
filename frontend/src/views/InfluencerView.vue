<template>
    <div v-if="!loading">

        <!-- Navigation Bar -->
        <NavBar :name="user.name" role="influencer" :flag="user.flag"/>

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

            <!-- Profile Page -->
            <ProfilePage :user="user" @error="error_message" @success="success_message"/>

            <div v-if="!user.flag">

                <div v-if="!flag">
                <!-- Ad Requests Page -->
                <AdRequestList v-if="!ad_loading" role="influencer" :ad_requests="adRequests" :ad_request="ad_request" 
                @update-adRequests="adRequestPage" @update-adRequest="updateAdRequest" @error="error_message" @success="success_message"/>
                </div>
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
        success: null,
        error: null,
        loading: true,
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
        } catch (error) {
            this.error = error.message;
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
                    influencer_id: this.user.id, 
                    page: page
                })
            });
            //console.log(response.json());
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Failed to fetch ad requests');
            }
            this.adRequests = data;
        } catch (error) {
            console.log(error);
        } finally {
            this.ad_loading = false;
        }
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
    },
    async initializePage(){
        await this.getUser();
        await this.adRequestPage(1);
        console.log(this.adRequests);
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
created() {
    this.initializePage();
},
components: {
    NavBar,
    ProfilePage,
    AdRequestList
}
}
</script>