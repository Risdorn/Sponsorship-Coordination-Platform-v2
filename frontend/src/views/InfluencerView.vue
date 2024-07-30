<template>

  <NavBar :name="user.name" role="sponsor" :flag="flag" /> 

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
    <AdRequestList role="sponsor" :adRequestPage="adRequestPage"/>
    </div>

  </div>
</template>

<script>

export default {
name: 'InfluencerView',
data() {
    return {
        user: null,
        flag: null,
        success: null,
        error: null,
    }
},
methods: {
    async getUser() {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:5000/api/influencer', {
                method: 'GET',
                headers: {
                    'Authorization-Token': token
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
    async adRequestPage() {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:5000/api/influencer/ad-requests', {
                method: 'GET',
                headers: {
                    'Authorization-Token': token
                }
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Failed to fetch ad requests');
            }
            this.adRequestPage = data;
        } catch (error) {
            this.error = error.message;
        }
    },
},
}
</script>