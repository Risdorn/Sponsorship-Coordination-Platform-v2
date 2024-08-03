<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light fixed-top">
        <a class="navbar-brand" href="#">Welcome {{ name }}</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav mr-auto">
            <li class="nav-item active">
                <a class="nav-link" :href="'/' + role + '#Profile'">Profile</a>
            </li>
            <li v-if="role != 'influencer'" class="nav-item">
                <a class="nav-link" :href="'/' + role + '#Campaigns'">Campaigns</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" :href="'/' + role + '#Ad_Requests'">Ad Requests</a>
            </li>
            <li v-if="role == 'admin'" class="nav-item">
                    <a class="nav-link" :href="'/' + role + '#Flagged'">Flagged Users</a>
            </li>
            <li v-if="role == 'sponsor'" class="nav-item">
                <a  v-if="flag" class="nav-link" disabled>Find Influencers</a>
                <a v-else class="nav-link" href="/search">Find Influencers</a>
            </li>
            <li v-if="role == 'influencer'" class="nav-item">
                <a v-if="flag" class="nav-link" disabled>Find Campaigns</a>
                <a v-else class="nav-link" href="/search">Find Campaigns</a>
            </li>
            <li class="nav-item">
                <a v-if="flag" class="nav-link" disabled>Stats</a>
                <a v-else class="nav-link" href="/stats">Stats</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" @click="logout">Logout</a>
            </li>
            </ul>
        </div>
    </nav>
</template>

<script>
export default {
    name: 'NavBar',
    props: {
        name: String,
        role: String,
        flag: Boolean
    },
    methods: {
        logout(event) {
            event.preventDefault();
            localStorage.removeItem('token');
            localStorage.removeItem('email');
            localStorage.removeItem('role');
            this.$router.push('/login');
        }
    }
};
</script>