<template>
    <div id="Profile">
        <h1>Welcome, {{ user.name }}</h1>
        <p v-if="user.role=='Sponsor'"><b>Industry</b>: {{ user.industry }}</p>
        <p v-if="user.role=='Influencer'"><b>Reach</b>: {{ user.reach }}</p>
        <p v-if="user.role=='Influencer'"><b>Category</b>: {{ user.category }}</p>
        <p><b>Email</b>: {{ user.email }}</p>
        <!-- Edit Profile modal -->
        <button type="button" class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#editProfileModal">
            Edit Profile
        </button>
            
        <!-- Edit Profile Modal -->
        <div class="modal fade" id="editProfileModal" tabindex="-1" role="dialog" aria-labelledby="editProfileModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <form method="POST" id="edit_profile">
                    <div class="modal-header">
                        <h5 class="modal-title" id="editProfileModalLabel">Edit Profile</h5>
                    </div>
                    <div class="modal-body">
                        <input type="hidden" name="form_id" value="edit_profile">
                        <!-- Name input -->
                        <div data-mdb-input-init class="form-outline mb-4">
                            <p><b>Current Name</b>: {{ user.name }}</p>
                            <input type="text" name="name" id="Full_Name" v-model="name" class="form-control" maxlength="45" pattern="^[\w\-\s]+$"/>
                            <label class="form-label" for="Full_Name">Full Name</label>
                        </div>

                        <!-- Industry input -->
                        <div v-if="user.role=='Sponsor'" data-mdb-input-init class="form-outline mb-4">
                            <p><b>Current Industry</b>: {{ user.industry }}</p>
                            <select id="Industry" name="industry" v-model="industry" class="form-control">
                                <option disabled selected>{{ user.industry }}</option>
                                <option value="Technology">Technology</option>
                                <option value="Finance">Finance</option>
                                <option value="Healthcare">Healthcare</option>
                                <option value="Education">Education</option>
                                <option value="Manufacturing">Manufacturing</option>
                                <option value="Retail">Retail</option>
                                <option value="Real-Estate">Real Estate</option>
                                <option value="Entertainment">Entertainment</option>
                                <option value="Transportation">Transportation</option>
                                <option value="Agriculture">Agriculture</option>
                                <option value="Automotive">Automotive</option>
                                <option value="Construction">Construction</option>
                                <option value="Energy">Energy</option>
                                <option value="Food-and-Beverage">Food and Beverage</option>
                                <option value="Hospitality">Hospitality</option>
                                <option value="Insurance">Insurance</option>
                                <option value="Media">Media</option>
                                <option value="Pharmaceuticals">Pharmaceuticals</option>
                                <option value="Professional-Services">Professional Services</option>
                                <option value="Public-Sector">Public Sector</option>
                                <option value="Telecommunications">Telecommunications</option>
                                <option value="Utilities">Utilities</option>
                                <option value="Logistics">Logistics</option>
                                <option value="Mining">Mining</option>
                                <option value="Non-Profit">Non-Profit</option>
                                <option value="Aerospace">Aerospace</option>
                                <option value="Biotechnology">Biotechnology</option>
                                <option value="Chemicals">Chemicals</option>
                                <option value="Consulting">Consulting</option>
                                <option value="Defense">Defense</option>
                                <option value="Fashion">Fashion</option>
                                <option value="Furniture">Furniture</option>
                                <option value="Human-Resources">Human Resources</option>
                                <option value="Legal">Legal</option>
                                <option value="Luxury-Goods">Luxury Goods</option>
                                <option value="Packaging">Packaging</option>
                                <option value="Publishing">Publishing</option>
                                <option value="Recreation">Recreation</option>
                                <option value="Security">Security</option>
                                <option value="Sports">Sports</option>
                                <option value="Tourism">Tourism</option>
                                <option value="Waste-Management">Waste Management</option>
                                <option value="Wholesale">Wholesale</option>
                            </select>
                            <label class="form-label" for="Industry">Industry</label>
                        </div>

                        <!-- Category input -->
                        <div v-if="user.role=='Influencer'" data-mdb-input-init class="form-outline mb-4">
                            <p><b>Current Category</b>: {{ user.category }}</p>
                            <select id="category" name="category" v-model="category" class="form-control">
                                <option disabled selected>{{ user.category }}</option>
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
                            <label class="form-label" for="category">Category</label>
                        </div>

                        <!-- Reach input -->
                        <div v-if="user.role=='Influencer'" data-mdb-input-init class="form-outline mb-4">
                            <p><b>Current Reach</b>: {{ user.reach }}</p>
                            <input type="number" id="Reach" name="reach" v-model="reach" class="form-control" pattern="^\d+$" min=0/>
                            <label class="form-label" for="Reach">Reach</label>
                        </div>
                    
                        <!-- Password input -->
                        <div data-mdb-input-init class="form-outline mb-4">
                            <input type="password" id="Pass" name="pass" v-model="password" class="form-control" minlength="8" pattern="^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*\W)(?!.* ).{8,}$"/>
                            <label class="form-label" for="Pass">Change Password</label>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button class="btn btn-success" @click="editProfile">Save changes</button>
                    </div>
                </form>
            </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ProfilePage',
    props: {
    user: Object,
    flag: Boolean
    },
    data() {
    return {
        name: '',
        industry: '',
        category: '',
        reach: 0,
        password: ''
    }
    },
    methods: {
    async editProfile(event) {
        event.preventDefault();
        try {
        const token = localStorage.getItem('token');
        const email = localStorage.getItem('email');
        const response = await fetch('http://localhost:5000/api/user/' + email, {
            method: 'PUT',
            headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': token
            },
            body: JSON.stringify({
            name: this.name,
            industry: this.industry,
            category: this.category,
            reach: this.reach,
            password: this.password
            })
        });
        const data = await response.json();
        if(!response.ok) {
            throw new Error(data.message || 'Failed to edit profile');
        }
        this.$router.go();
        } catch (error) {
        console.error('Error:', error);
        }
    }
    }
}
</script>