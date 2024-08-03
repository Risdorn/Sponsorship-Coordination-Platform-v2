<template>
    <div v-if="!loading">
        <!-- Navigation bar -->
        <NavBar :name="user.name" :role="user.role" :flag="user.flag"/>

        <div style="margin-top: 56px;">
            <!-- Error message display -->
            <div v-if="success" class="alert alert-success" role="alert">
                {{ success }}
            </div>
            <div v-if="error" class="alert alert-danger" role="alert">
                {{ error }}
            </div>

            <!-- Flag message display -->
            <div v-if="user.flag" class="alert alert-danger" role="alert">
                You have been flagged, kindly make the below changes before your profile can be activated again.<br>
                Reason: {{ user.reason }}
            </div>

            <div v-else class="Main Section">
                <div class="Search Params">
                    <form class="d-flex mr-auto">
                        <input type="hidden" name="form_id" value="search_name">
                        <input class="form-control me-2" type="search" name="search" v-model="name" placeholder="Search" aria-label="Search" style="width:200px">
                        <select class="form-select me-2" name="sort" id="sort" v-model="sort" aria-label="Sort" style="width:150px">
                            <option :value="null" selected>No Sorting</option>
                            <option value="Ascending">Ascending</option>
                            <option value="Descending">Descending</option>
                        </select>
                        <label v-if="user.role=='sponsor'" for="Search_Type" style="width:120px; align-content: center;">Sort By Reach</label>
                        <label v-if="user.role=='influencer'" for="Search_Type" style="width:120px; align-content: center;">Sort By Budget</label>
                        <select id="category" name="category" v-model="category" class="form-select me-2" style="width:200px">
                            <option :value="null" selected>No Categories</option>
                            <option value="Beauty">Beauty</option>
                            <option value="Fashion">Fashion</option>
                            <option value="Fitness">Fitness</option>
                            <option value="Health">Health</option>
                            <option value="Travel">Travel</option>
                            <option value="Food">Food</option>
                            <option value="Lifestyle">Lifestyle</option>
                            <option value="Gaming">Gaming</option>
                            <option value="Technology">Technology</option>
                            <option value="Photography">Photography</option>
                            <option value="Music">Music</option>
                            <option value="Parenting">Parenting</option>
                            <option value="Finance">Finance</option>
                            <option value="Education">Education</option>
                            <option value="Sports">Sports</option>
                            <option value="Art">Art</option>
                            <option value="Home-Decor">Home Decor</option>
                            <option value="Pets">Pets</option>
                            <option value="Automotive">Automotive</option>
                            <option value="Books">Books</option>
                            <option value="DIY">DIY</option>
                            <option value="Environment">Environment</option>
                            <option value="Entertainment">Entertainment</option>
                            <option value="Business">Business</option>
                            <option value="Spirituality">Spirituality</option>
                            <option value="Dating">Dating</option>
                            <option value="Career">Career</option>
                            <option value="Event-Planning">Event Planning</option>
                            <option value="Gaming-Cosplay">Gaming Cosplay</option>
                            <option value="Luxury">Luxury</option>
                            <option value="Outdoors">Outdoors</option>
                            <option value="Wellness">Wellness</option>
                            <option value="Mental-Health">Mental Health</option>
                            <option value="Non-Profit">Non-Profit</option>
                            <option value="Comedy">Comedy</option>
                            <option value="News">News</option>
                            <option value="Personal-Development">Personal Development</option>
                            <option value="Relationship">Relationship</option>
                            <option value="Social-Justice">Social Justice</option>
                            <option value="Sustainable-Living">Sustainable Living</option>
                            <option value="Tech-Gadgets">Tech Gadgets</option>
                            <option value="Videography">Videography</option>
                            <option value="Yoga">Yoga</option>
                            <option value="Crypto">Crypto</option>
                            <option value="Investment">Investment</option>
                            <option value="Real-Estate">Real Estate</option>
                        </select>
                        <label for="category" style="width:100px; align-content: center;">Category</label>
                        <button class="btn btn-outline-success" @click="search_param">Search</button>
                </form>
                </div>
                <h3>Search Results</h3>
                <div>
                    <div v-if="name">Search Term: {{ name }}</div>
                    <div v-if="sort">Sort: {{ sort }}</div>
                    <div v-if="category">Category: {{ category }}</div>
                </div>

                <!-- Users Page -->
                <UserList v-if="!result_loading && user.role=='sponsor'" :users="results" :role="user.role" :campaigns="campaigns"
                @page-change="search" @error="error_message" @success="success_message"/>
            
                <!-- Campaigns Page -->
                <CampaignList v-if="!result_loading && user.role=='influencer'" :role="user.role" :campaigns="results"
                @update-campaigns="search" @error="error_message" @success="success_message"/>
            </div>
        </div>
    </div>
</template>

<script>
import CampaignList from '../components/CampaignList.vue';
import NavBar from '../components/NavBar.vue';
import UserList from '../components/UserList.vue';

export default {
name: 'SearchView',
data() {
    return {
        user: null,
        success: null,
        error: null,
        loading: true,
        result_loading: true,
        results: [],
        campaigns: [],
        name: '',
        sort: '',
        category: '',
        path: 'http://localhost:5000/api/'
    };
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
            this.user.role = this.user.role.toLowerCase();
        } catch (error) {
            this.error = error.message;
        }
    },
    async getCampaigns(){
        try {
            const response = await fetch('http://localhost:5000/api/campaign/sponsor', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('token')
                },
                body: JSON.stringify({
                    sponsor_id: this.user.id,
                })
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Failed to fetch campaigns');
            }
            this.campaigns = data;
        } catch (error) {
            console.error(error);
        }
    },
    async search(page) {
        this.result_loading = true;
        console.log(this.path);
        try {
            const response = await fetch(this.path, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('token')
                },
                body: JSON.stringify({
                    name: this.name,
                    sort: this.sort,
                    category: this.category,
                    page: page
                })
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Failed to search');
            }
            this.results = data;
        } catch (error) {
            console.error(error);
        } finally {
            this.result_loading = false;
        }
    },
    async search_param(event) {
        event.preventDefault();
        await this.search(1);
    },
    async initializePage(){
        await this.getUser();
        if(this.user.role == 'sponsor') {
            this.path = 'http://localhost:5000/api/user/search';
            await this.getCampaigns();
        } else {
            this.path = 'http://localhost:5000/api/campaign/search';
        }
        await this.search(1);
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
    CampaignList,
    NavBar,
    UserList
},
created() {
    this.initializePage();
}
};
</script>