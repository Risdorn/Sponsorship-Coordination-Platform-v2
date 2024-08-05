<template>
    <div id="Campaigns">
        <h3>Published Campaigns
            <button v-if="role=='sponsor'" type="button" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addCampaign">
                Add Campaign
            </button>
        </h3>
            <!-- Add Campaign Modal -->
            <div v-if="role=='sponsor'" class="modal fade" id="addCampaign" tabindex="-1" role="dialog" aria-labelledby="addCampaignLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <form id="add_campaign">
                        <div class="modal-header">
                            <h5 class="modal-title" id="addCampaignLabel">Add Campaign</h5>
                        </div>
                        <div class="modal-body">
                            <input type="hidden" name="form_id" value="add_campaign">
                            <!-- Name input -->
                            <div data-mdb-input-init class="form-outline mb-4">
                                <input type="text" name="name" id="name" v-model="name" class="form-control" required maxlength=45/>
                                <label class="form-label" for="name">Campaign Name</label>
                            </div>

                            <!-- Description input -->
                            <div data-mdb-input-init class="form-outline mb-4">
                                <input type="text" id="Description" name="description" v-model="description" class="form-control" required maxlength=250/>
                                <label class="form-label" for="description">Description</label>
                            </div>

                            <!-- Goals input -->
                            <div data-mdb-input-init class="form-outline mb-4">
                                <input type="text" id="Goals" name="goals" v-model="goals" class="form-control" required maxlength=250/>
                                <label class="form-label" for="goals">Goals</label>
                            </div>

                            <!-- category input -->
                            <div data-mdb-input-init class="form-outline mb-4" required>
                                <select id="category" name="category" v-model="category" class="form-control" required>
                                    <option value = "" disabled selected>Select a Category</option>
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

                            <!-- Budget input -->
                            <div data-mdb-input-init class="form-outline mb-4">
                                <input type="number" id="Budget" name="budget" v-model="budget" class="form-control" required pattern="^[0-9]+" min=0/>
                                <label class="form-label" for="budget">Budget</label>
                            </div>

                            <!-- Visibility input -->
                            <div data-mdb-input-init class="form-outline mb-4">
                                <select id="Visibility" name="visibility" v-model="visibility" class="form-control" required>
                                    <option value="Public" selected>Public</option>
                                    <option value="Private">Private</option>
                                </select>
                                <label class="form-label" for="visibility">Visibility</label>
                            </div>

                            <!-- Start Date input -->
                            <div data-mdb-input-init class="form-outline mb-4">
                                <input type="date" id="Start_date" name="start_date" v-model="start_date" class="form-control" required/>
                                <label class="form-label" for="start_date">Start Date</label>
                            </div>

                            <!-- End Date input -->
                            <div data-mdb-input-init class="form-outline mb-4">
                                <input type="date" id="End_date" name="end_date" v-model="end_date" class="form-control" required/>
                                <label class="form-label" for="end_date">End Date</label>
                            </div>
                        
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button class="btn btn-success" @click="addCampaign">Add Campaign</button>
                        </div>
                    </form>
                </div>
                </div>
            </div><br>
            <p v-if="!campaigns || campaigns.items.length==0">No campaigns published yet.</p>
            <div v-else v-for="campaign in campaigns.items" :key="campaign.id">
                <div class="card">
                    <div class="card-header">
                        <h5>{{ campaign.name }} <a :href="'/campaign/' + campaign.id"  class="btn btn-info">View Campaign</a></h5>
                    </div>
                    <div class="card-body">
                        <div v-if="campaign.length==0 && role=='sponsor'" class="alert alert-warning" role="alert">
                            No Ad Requests sent yet.<br>
                            Campaign will not show up on search results.
                        </div>
                        <p class="card-text"><b>Description</b>: {{ campaign.description }}</p>
                        <p class="card-text"><b>Goals</b>: {{ campaign.goals }}</p>
                        <p class="card-text"><b>Category</b>: {{ campaign.category }}</p>
                        <p class="card-text"><b>Visibility</b>: {{ campaign.visibility }}</p>
                        <p class="card-text"><b>Budget</b>: {{ campaign.budget }}</p>
                        <p class="card-text"><b>Remaining Budget</b>: {{ campaign.remaining }}</p>
                        <p class="card-text">Active from <b>{{ campaign.start_date }}</b> to <b>{{ campaign.end_date }}</b></p>
                        <div class="progress">
                            <div class="progress-bar" role="progressbar" :style="{ width: campaign.progress + '%' }" 
                            :aria-valuenow="campaign.progress" aria-valuemin="0" aria-valuemax="100">{{ campaign.progress }}%</div>
                        </div><br>
                        <div v-if="role=='sponsor'">
                            <!-- Edit Campaign Button -->
                            <button type="button" class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#editCampaign" :id="campaign.id" @click="ChangeCampaign">
                                Edit Campaign
                            </button>
                            <!-- Delete Campaign Button -->
                            <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteCampaign" :id="campaign.id" @click="ChangeId">
                                Delete Campaign
                            </button>
                        </div>
                    </div>
                </div><br>
            </div>

            <!-- Edit Campaign Modal -->
            <div v-if="role=='sponsor' && campaign" class="modal fade" id="editCampaign" tabindex="-1" role="dialog" aria-labelledby="editCampaignLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <form id="edit_campaign">
                        <div class="modal-header">
                            <h5 class="modal-title" id="editCampaignLabel">Edit Campaign</h5>
                        </div>
                        <div class="modal-body">
                            <!-- Name input -->
                            <div data-mdb-input-init class="form-outline mb-4">
                                <p><b>Cuurent Name</b>: {{ campaign.name }}</p>
                                <input type="text" name="name" id="name" v-model="name" class="form-control" maxlength=45/>
                                <label class="form-label" for="name">Campaign Name</label>
                            </div>

                            <!-- Description input -->
                            <div data-mdb-input-init class="form-outline mb-4">
                                <p><b>Cuurent Description</b>: {{ campaign.description }}</p>
                                <input type="text" id="Description" name="description" v-model="description" class="form-control" maxlength=250/>
                                <label class="form-label" for="description">Description</label>
                            </div>

                            <!-- Goals input -->
                            <div data-mdb-input-init class="form-outline mb-4">
                                <p><b>Cuurent Goals</b>: {{ campaign.goals }}</p>
                                <input type="text" id="Goals" name="goals" v-model="goals" class="form-control" maxlength=250/>
                                <label class="form-label" for="goals">Goals</label>
                            </div>

                            <!-- category input -->
                            <div data-mdb-input-init class="form-outline mb-4">
                                <p><b>Cuurent Category</b>: {{ campaign.category }}</p>
                                <select id="category" name="category" v-model="category" class="form-control">
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

                            <!-- Budget input -->
                            <div data-mdb-input-init class="form-outline mb-4">
                                <p><b>Cuurent Budget</b>: {{ campaign.budget }}</p>
                                <input type="number" id="Budget" name="budget" v-model="budget" class="form-control" pattern="^\d+$"/>
                                <label class="form-label" for="budget">Budget</label>
                            </div>

                            <!-- Visibility input -->
                            <div data-mdb-input-init class="form-outline mb-4">
                                <p><b>Cuurent Visibility</b>: {{ campaign.visibility }}</p>
                                <select id="Visibility" name="visibility" v-model="visibility" class="form-control">
                                    <option value="Public" selected>Public</option>
                                    <option value="Private">Private</option>
                                </select>
                                <label class="form-label" for="visibility">Visibility</label>
                            </div>

                            <!-- Start Date input -->
                            <div data-mdb-input-init class="form-outline mb-4">
                                <p><b>Cuurent Start Date</b>: {{ campaign.start_date }}</p>
                                <input type="date" id="Start_date" name="start_date" v-model="start_date" class="form-control"/>
                                <label class="form-label" for="start_date">Start Date</label>
                            </div>

                            <!-- End Date input -->
                            <div data-mdb-input-init class="form-outline mb-4">
                                <p><b>Cuurent End Date</b>: {{ campaign.end_date }}</p>
                                <input type="date" id="End_date" name="end_date" v-model="end_date" class="form-control"/>
                                <label class="form-label" for="end_date">End Date</label>
                            </div>
                        
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button class="btn btn-success" @click="editCampaign">Save changes</button>
                        </div>
                    </form>
                </div>
                </div>
            </div>

            <!-- Delete Campaign Modal -->
            <div v-if="role=='sponsor'" class="modal fade" id="deleteCampaign" tabindex="-1" role="dialog" aria-labelledby="deleteCampaignLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <div class="alert alert-warning" role="alert">
                        This action will delete the campaign and all associated ad requests.
                    </div>
                    <form id="delete_campaign">
                        <div class="modal-header">
                            <h5 class="modal-title" id="deleteCampaignLabel">Delete Campaign</h5>
                        </div>
                        <div class="modal-body">
                            <label class="form-label">Are you sure?</label>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button class="btn btn-danger" @click="deleteCampaign">Delete Campaign</button>
                        </div>
                    </form>
                </div>
                </div>
            </div>

            <!-- Navigation section for pagination controls -->
            <nav aria-label="Campaign Page navigation">
                <ul class="pagination">
                    <!-- Check if there is a previous page -->
                    <li v-if="campaigns.has_prev" class="page-item">
                        <!-- If there is, create a link to the previous page -->
                        <a class="page-link" @click="handlePageChange(campaigns.prev_num)">Previous</a>
                    </li>
                    <!-- If not, show a disabled 'Previous' button -->
                    <li v-else class="page-item disabled"><span class="page-link">Previous</span></li>

                    <!-- Loop through each page number provided by pagination.iter_pages() -->
                    <div v-for="(page_num, index) in campaigns.pages_iter" :key="index">
                        <!-- Check if the page number exists (not None) -->
                        <li v-if="page_num" class="page-item">
                            <!-- Check if the current page is not the active page -->
                            <a v-if="page_num != campaigns.page" class="page-link" @click="handlePageChange(page_num)">{{ page_num }}</a>
                            <!-- Highlight the current page as active and not clickable -->
                            <span v-else class="page-link disabled">{{ page_num }}</span>
                        </li>
                        <!-- For gaps in the pagination links, show ellipsis -->
                        <li v-else class="page-item disabled"><span class="page-link">...</span></li>
                    </div>

                    <!-- Check if there is a next page -->
                    <li v-if="campaigns.has_next" class="page-item">
                        <!-- If there is, create a link to the next page -->
                        <a class="page-link" @click="handlePageChange(campaigns.next_num)">Next</a>
                    </li>
                    <!-- If not, show a disabled 'Next' button -->
                    <li v-else class="page-item disabled"><span class="page-link">Next</span></li>
                </ul>
            </nav>
        </div>
</template>

<script>
export default {
  name: 'CampaignList',
  props: {
    role: String,
    sponsor_id: Number,
    campaigns: Object,
    campaign: Object
  },
    data() {
        return {
            name: null,
            description: null,
            goals: null,
            category: null,
            budget: null,
            visibility: 'Public',
            start_date: null,
            end_date: null,
            id: null,
        };
    },
    methods: {
        async addCampaign(event) {
            event.preventDefault();
            try {
                console.log("Adding campaign");
                const response = await fetch('http://localhost:5000/api/campaign', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': localStorage.getItem('token')
                    },
                    body: JSON.stringify({
                        name: this.name,
                        description: this.description,
                        goals: this.goals,
                        category: this.category,
                        budget: this.budget,
                        visibility: this.visibility,
                        start_date: this.start_date,
                        end_date: this.end_date,
                        sponsor_id: this.sponsor_id
                    })
                });
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.message || 'Failed to add campaign');
                }
                this.$router.go();
                this.$emit('success', 'Campaign added successfully');
            } catch (error) {
                this.$emit('error', error.message);
            }
        },
        async editCampaign(event) {
            event.preventDefault();
            try {
                const response = await fetch('http://localhost:5000/api/campaign/' + this.id, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': localStorage.getItem('token')
                    },
                    body: JSON.stringify({
                        name: this.name,
                        description: this.description,
                        goals: this.goals,
                        category: this.category,
                        budget: this.budget,
                        visibility: this.visibility,
                        start_date: this.start_date,
                        end_date: this.end_date
                    })
                });
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.message || 'Failed to edit campaign');
                }
                this.$emit('success', 'Campaign edited successfully');
                this.$router.go();
            } catch (error) {
                this.$emit('error', error.message);
            }
        },
        async deleteCampaign(event) {
            event.preventDefault();
            try {
                const response = await fetch('http://localhost:5000/api/campaign/' + this.id, {
                    method: 'DELETE',
                    headers: {
                        'Authorization-Token': localStorage.getItem('token')
                    }
                });
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.message || 'Failed to delete campaign');
                }
                this.$emit('success', 'Campaign deleted successfully');
                this.$router.go();
            } catch (error) {
                this.$emit('error', error.message);
            }
        },
        ChangeId(event) {
            this.id = event.target.id;
        },
        async ChangeCampaign(event){
            this.id = event.target.id;
            this.$emit('update-campaign', this.id)
        },
        async handlePageChange(page_num) {
            this.$emit('update-campaigns', page_num);
        }
    },
}
</script>