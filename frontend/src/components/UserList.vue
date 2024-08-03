<template>
    <div id="Users">
        <h3>Users</h3>
        <!-- In case no users are registered -->
        <p v-if="users.items.length == 0">No Users Registered.</p>
        <br v-else>
        <!-- Loop through each user in the users array -->
        <div v-for="user in users.items" :key="user.id">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">{{ user.name }}</h5>
                    <p class="card-text"><b>Email</b>: {{ user.email }}</p>
                    <p v-if="role=='admin'" class="card-text"><b>Role</b>: {{ user.role }}</p>
                    <p v-if="user.role=='Influencer'" class="card-text"><b>Reach</b>: {{ user.reach }}</p>
                    <p v-if="user.role=='Influencer'" class="card-text"><b>Category</b>: {{ user.category }}</p>
                    <p v-if="user.role=='Sponsor'" class="card-text"><b>Industry</b>: {{ user.industry }}</p>
                    <!-- Flag User modal -->
                    <button v-if="!user.flag && role=='admin'" type="button" class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#flagUser" :id="user.id" @click="changeId">
                        Flag User
                    </button>
                    <!-- Send Ad Request Button -->
                    <button v-if="role=='sponsor'" type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#requestAd" :id="user.id" @click="changeId">
                        Request
                    </button>
                </div>
            </div>
            <br>
        </div>

        <!-- Flag User Modal -->
        <div v-if="role=='admin'" class="modal fade" id="flagUser" tabindex="-1" role="dialog" aria-labelledby="flagUser" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <form id="flag">
                        <div class="modal-header">
                            <h5 class="modal-title" id="editProfileModalLabel">Flag User</h5>
                        </div>
                        <div class="modal-body">
                            <!-- Reason input -->
                            <div data-mdb-input-init class="form-outline mb-4">
                                <input type="text" name="reason" id="reason" v-model="reason" class="form-control" required maxlength=250/>
                                <label class="form-label" for="reason">Reason</label>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button class="btn btn-warning">Flag User</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <!-- Ad Request Modal -->
        <div v-if="role=='sponsor'" class="modal fade" id="requestAd" tabindex="-1" role="dialog" aria-labelledby="requestAd" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <form id="request_ad">
                        <div class="modal-header">
                            <h5 class="modal-title" id="requestAd">Send an Ad Request</h5>
                        </div>
                        <div class="modal-body">
                            <select class="form-select" name="campaign_id" id="Campaign" v-model="campaign_id" aria-label="Default select example" required>
                                <option v-for="campaign in campaigns" :key="campaign.id" :value="campaign.id">{{ campaign.name }}</option>
                            </select>
                            <label class="form-label" for="Campaign">Campaign</label>
                            <input type="text" name="message" id="Messages" v-model="messages" class="form-control" required maxlength=250/>
                            <label class="form-label" for="Messages">Messages</label>
                            <input type="text" name="requirement" id="Requirements" v-model="requirements" class="form-control" required maxlength=250/>
                            <label class="form-label" for="Requirements">Requirements</label>
                            <input type="number" name="payment_amount" id="Payment_Amount" v-model="payment_amount" class="form-control" required min=0 pattern="^\d+$"/>
                            <label class="form-label" for="Payment_Amount">Payment Amount</label>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button class="btn btn-primary" data-bs-dismiss="modal" @click="sendAdRequest">Request</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <!-- Navigation section for User page -->
        <nav aria-label="User Page navigation">
            <ul class="pagination">
                <!-- Check if there is a previous page -->
                <li v-if="users.has_prev" class="page-item">
                    <!-- If there is, create a link to the previous page -->
                    <a class="page-link" @click="handlePageChange(users.prev_num)">Previous</a>
                </li>
                <!-- If not, show a disabled 'Previous' button -->
                <li v-else class="page-item disabled"><span class="page-link">Previous</span></li>

                <!-- Loop through each page number provided by pagination.iter_pages() -->
                <div v-for="(page_num, index) in users.pages_iter" :key="index">
                    <!-- Check if the page number exists (not None) -->
                    <li v-if="page_num" class="page-item">
                        <!-- Check if the current page is not the active page -->
                        <a v-if="page_num != users.page" class="page-link" @click="handlePageChange(page_num)">{{ page_num }}</a>
                        <!-- Highlight the current page as active and not clickable -->
                        <span v-else class="page-link disabled">{{ page_num }}</span>
                    </li>
                    <!-- For gaps in the pagination links, show ellipsis -->
                    <li v-else class="page-item disabled"><span class="page-link">...</span></li>
                </div>

                <!-- Check if there is a next page -->
                <li v-if="users.has_next" class="page-item">
                    <!-- If there is, create a link to the next page -->
                    <a class="page-link" @click="handlePageChange(users.next_num)">Next</a>
                </li>
                <!-- If not, show a disabled 'Next' button -->
                <li v-else class="page-item disabled"><span class="page-link">Next</span></li>
            </ul>
        </nav>
    </div>
</template>

<script>
export default {
    name: 'UserList',
    props: {
        users: Object,
        role: String,
        campaigns: Array,
    },
    data() {
    return {
        reason: '',
        id: '',
        campaign_id: '',
        messages: '',
        requirements: '',
        payment_amount: 0,
    };
    },
    methods: {
        async sendAdRequest(event) {
            event.preventDefault();
            try {
                const response = await fetch('http://localhost:5000/api/ad_request', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': localStorage.getItem('token')
                    },
                    body: JSON.stringify({
                        influencer_id: this.id,
                        campaign_id: this.campaign_id,
                        messages: this.messages,
                        requirements: this.requirements,
                        payment_amount: this.payment_amount
                    })
                });
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.message || 'Failed to send ad request');
                }
                this.messages = '';
                this.requirements = '';
                this.payment_amount = 0;
                this.$emit('success', 'Ad request sent successfully');
                console.log(data);
            } catch (error) {
                this.$emit('error', error.message);
            }
        },
        async flagUser() {
            try {
                const response = await fetch('http://localhost:5000/api/user/flag', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': localStorage.getItem('token')
                    },
                    body: JSON.stringify({
                        user_id: this.id,
                        reason: this.reason
                    })
                });
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.message || 'Failed to flag user');
                }
                this.reason = '';
                this.$emit('success', 'User flagged successfully');
                this.$router.go();
            } catch (error) {
                this.$emit('error', error.message);
            }
        },
        async handlePageChange(page_num) {
            this.$emit('page-change', page_num);
        },
        changeId(event) {
            this.id = event.target.id;
        }
    },
};
</script>