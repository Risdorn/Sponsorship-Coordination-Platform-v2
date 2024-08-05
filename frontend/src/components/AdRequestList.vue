<template>
    <div id="Ad_Requests">
        <h3>Ad Requests</h3>
        <div v-if="!ad_requests || ad_requests.items.length==0">
            <p v-if="role=='sponsor'">No Ad Requests sent yet.</p>
            <p v-else-if="role=='influencer'">No Ad Requests received yet.</p>
        </div>
        <div v-else v-for="ad_request in ad_requests.items" :key="ad_request.id">
            <div class="card">
                <div v-if="type!='campaign'" class="card-header">
                    <h5>{{ ad_request.campaign.name }} <a :href="'/campaign/' + ad_request.campaign.id"  class="btn btn-info">View Campaign</a></h5>
                </div>
                <div class="card-body">
                    <p class="card-text"><b>Messages</b>: {{ ad_request.messages }}</p>
                    <p class="card-text"><b>Requirements</b>: {{ ad_request.requirements }}</p>
                    <p class="card-text"><b>Payment Amount</b>: {{ ad_request.payment_amount }}</p>
                    <div v-if="type=='campaign' || role!='influencer'">
                        <p v-if="!ad_request.influencer.name" class="card-text"><b>Influencer Not Assigned</b></p>
                        <p v-else class="card-text">Assigned to <b>{{ ad_request.influencer.name }}</b></p>
                    </div>
                    <div v-if="role=='sponsor' && ad_request.status=='Pending' && !ad_request.negotiate">
                        <p><b>Status</b>: {{ ad_request.status }}</p>
                        <!-- Edit Ad Request Button -->
                        <button type="button" class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#editAd" :id="ad_request.id" @click="changeAd">
                            Edit
                        </button>
                        <!-- Withdraw Ad Request Button -->
                        <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#withdrawAd" :id="ad_request.id" @click="changeId">
                            Withdraw
                        </button>
                    </div>
                    <div v-else-if="role=='sponsor' && ad_request.status=='Pending' && ad_request.negotiate">
                        <!-- Revert Ad Request Button -->
                        <button type="button" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#revertAd" :id="ad_request.id" @click="changeAd">
                            Revert
                        </button>
                    </div>
                    <div v-else-if="role=='influencer' && !ad_request.negotiate && (ad_request.influencer.id == user_id || !ad_request.influencer.id)">
                        <div v-if="ad_request.influencer.name">
                            <button type="button" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#revertAd" :id="ad_request.id" @click="changeAd">
                                Revert
                            </button>
                            <button type="button" class="btn btn-info" data-bs-toggle="modal" data-bs-target="#negotiateAd" :id="ad_request.id" @click="changeAd">
                                Negotiate
                            </button>
                        </div>
                        <button v-else type="button" class="btn btn-info" data-bs-toggle="modal" data-bs-target="#negotiateAd" :id="ad_request.id" @click="changeAd">
                                Request
                        </button>
                    </div>
                    <p v-else-if="ad_request.status=='Pending'"><b>Status</b>: {{ ad_request.status }}</p>
                    <p v-else><b>Status</b>: {{ ad_request.status }}ed</p>
                </div>
            </div>
            <br>
        </div>

        <!-- Revert Ad Request Modal -->
        <div v-if="ad_request" class="modal fade" id="revertAd" tabindex="-1" role="dialog" aria-labelledby="revertAd" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <form id="revert_ad">
                    <div class="modal-header">
                        <h5 class="modal-title" id="revertAd">Revert to Ad Request</h5>
                    </div>
                    <div class="modal-body">
                        <label class="form-label">Would you like to Accept or Reject?</label><br>
                        <label class="form-label"><b>{{ ad_request.campaign.name }}</b></label><br>
                        <label class="form-label"><b>Messages</b>: {{ ad_request.messages }}</label><br>
                        <label class="form-label"><b>Requirements</b>: {{ ad_request.requirements }}</label><br>
                        <label class="form-label"><b>Payment Amount</b>: {{ ad_request.payment_amount }}</label><br>
                        <label v-if="role=='sponsor'" class="form-label">Assigned to <b>{{ ad_request.influencer.name }}</b></label>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button class="btn btn-success" @click="revertAd($event, 'Accept')">Accept</button>
                        <button  class="btn btn-danger" @click="revertAd($event, 'Reject')">Reject</button>
                    </div>
                </form>
            </div>
            </div>
        </div>

        <!-- Negotiate Ad Request Modal -->
        <div v-if="ad_request" class="modal fade" id="negotiateAd" tabindex="-1" role="dialog" aria-labelledby="negotiateAd" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <form id="revert_ad">
                    <div class="modal-header">
                        <h5 class="modal-title" id="negotiateAd">Revert to Ad Request</h5>
                    </div>
                    <div class="modal-body">
                        <label class="form-label"><b>{{ ad_request.campaign.name }}</b></label><br>
                        <label class="form-label"><b>Messages</b>: {{ ad_request.messages }}</label><br>
                        <label class="form-label"><b>Requirements</b>: {{ ad_request.requirements }}</label><br>
                        <label class="form-label"><b>Payment Amount</b>: {{ ad_request.payment_amount }}</label><br>
                        <input type="number" name="payment_amount" id="Payment_Amount" v-model="payment_amount" class="form-control" min=0 pattern="^\d+$"/>
                        <label class="form-label" for="Payment_Amount">Payment Amount</label><br>

                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button class="btn btn-success" @click="negotiateAd">Send</button>
                    </div>
                </form>
            </div>
            </div>
        </div>

        <!-- Edit Ad Request Modal -->
        <div v-if="ad_request" class="modal fade" id="editAd" tabindex="-1" role="dialog" aria-labelledby="editAd" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <form id="edit_ad">
                    <div class="modal-header">
                        <h5 class="modal-title" id="editAd">Editting Ad Request</h5>
                    </div>
                    <div class="modal-body">
                        <label class="form-label">Ad Request for <b>{{ ad_request.campaign.name }}</b></label>

                        <p><b>Current Messages</b>: {{ ad_request.messages }}</p>
                        <input type="text" name="message" id="Messages" v-model="messages" class="form-control" maxlength=250/>
                        <label class="form-label" for="Messages">Messages</label>

                        <p><b>Current Requirements</b>: {{ ad_request.requirements }}</p>
                        <input type="text" name="requirement" id="Requirements" v-model="requirements" class="form-control" maxlength=250/>
                        <label class="form-label" for="Requirements">Requirements</label>

                        <p><b>Current Payment Amount</b>: {{ ad_request.payment_amount }}</p>
                        <input type="number" name="payment_amount" id="Payment_Amount" v-model="payment_amount" class="form-control" min=0 pattern="^\d+$"/>
                        <label class="form-label" for="Payment_Amount">Payment Amount</label><br>
                        
                        <label v-if="!ad_request.influencer.name" class="form-label"><b>Influencer Not Assigned</b></label>
                        <label v-else class="form-label">Assigned to <b>{{ ad_request.influencer.name }}</b></label>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button class="btn btn-success" @click="editAd">Save Changes</button>
                    </div>
                </form>
            </div>
            </div>
        </div>

        <!-- Withdraw Ad Request Modal -->
        <div v-if="ad_request" class="modal fade" id="withdrawAd" tabindex="-1" role="dialog" aria-labelledby="withdrawAd" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <form id="withdraw_ad">
                    <div class="modal-header">
                        <h5 class="modal-title" id="withdrawAd">Withdrawing Ad Request</h5>
                    </div>
                    <div class="modal-body">
                        <label class="form-label">Are you sure, you want to withdraw?</label>
                        <br>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button class="btn btn-danger" @click="deleteAd">Withdraw</button>
                    </div>
                </form>
            </div>
            </div>
        </div>

        <!-- Navigation section for pagination controls -->
        <nav aria-label="Ad Request Page navigation">
            <ul class="pagination">
                <!-- Check if there is a previous page -->
                <li v-if="ad_requests.has_prev" class="page-item">
                    <!-- If there is, create a link to the previous page -->
                    <a class="page-link" @click="handlePageChange(ad_requests.prev_num)">Previous</a>
                </li>
                <!-- If not, show a disabled 'Previous' button -->
                <li v-else class="page-item disabled"><span class="page-link">Previous</span></li>

                <!-- Loop through each page number provided by pagination.iter_pages() -->
                <div v-for="(page_num, index) in ad_requests.pages_iter" :key="index">
                    <!-- Check if the page number exists (not None) -->
                    <li v-if="page_num" class="page-item">
                        <!-- Check if the current page is not the active page -->
                        <a v-if="page_num != ad_requests.page" class="page-link" @click="handlePageChange(page_num)">{{ page_num }}</a>
                        <!-- Highlight the current page as active and not clickable -->
                        <span v-else class="page-link disabled">{{ page_num }}</span>
                    </li>
                    <!-- For gaps in the pagination links, show ellipsis -->
                    <li v-else class="page-item disabled"><span class="page-link">...</span></li>
                </div>

                <!-- Check if there is a next page -->
                <li v-if="ad_requests.has_next" class="page-item">
                    <!-- If there is, create a link to the next page -->
                    <a class="page-link" @click="handlePageChange(ad_requests.next_num)">Next</a>
                </li>
                <!-- If not, show a disabled 'Next' button -->
                <li v-else class="page-item disabled"><span class="page-link">Next</span></li>
            </ul>
        </nav>
            
    </div>
</template>

<script>
export default {
    name: 'AdRequestList',
    props: {
        role: String,
        ad_requests: Object,
        ad_request: Object,
        user_id: String,
        type: String
    },
    data() {
        return {
            id: '',
            messages: '',
            requirements: '',
            payment_amount: 0,
        };
    },
    methods: {
        async revertAd(event, action) {
            event.preventDefault();
            try {
                const response = await fetch('http://localhost:5000/api/ad_request/revert/' + this.id, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': localStorage.getItem('token')
                    },
                    body: JSON.stringify({
                        status: action
                    })
                });
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.message || 'Failed to revert');
                }
                this.$emit('success', 'Reverted successfully');
                this.$router.go();
            } catch (error) {
                this.$emit('error', error.message);
            }
        },
        async negotiateAd(event){
            event.preventDefault();
            try {
                const response = await fetch('http://localhost:5000/api/ad_request/negotiate/' + this.id, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': localStorage.getItem('token')
                    },
                    body: JSON.stringify({
                        payment_amount: this.payment_amount,
                        influencer_email: localStorage.getItem('email')
                    })
                });
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.message || 'Failed to negotiate');
                }
                this.$emit('success', 'Negotiated successfully');
                this.$router.go();
            } catch (error) {
                this.$emit('error', error.message);
            }
        },
        async editAd(event) {
            event.preventDefault();
            try {
                const response = await fetch('http://localhost:5000/api/ad_request/' + this.id, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': localStorage.getItem('token')
                    },
                    body: JSON.stringify({
                        messages: this.messages,
                        requirements: this.requirements,
                        payment_amount: this.payment_amount
                    })
                });
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.message || 'Failed to edit');
                }
                this.$emit('success', 'Edited successfully');
                this.$router.go();
            } catch (error) {
                this.$emit('error', error.message);
            }
        },
        async deleteAd(event) {
            event.preventDefault();
            try {
                const response = await fetch('http://localhost:5000/api/ad_request/' + this.id, {
                    method: 'DELETE',
                    headers: {
                        'Authentication-Token': localStorage.getItem('token')
                    }
                });
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.message || 'Failed to delete');
                }
                this.$emit('success', 'Deleted successfully');
                this.$router.go();
            } catch (error) {
                this.$emit('error', error.message);
            }
        },
        async handlePageChange(page_num) {
            this.$emit('update-adRequests', page_num);
        },
        async changeAd(event) {
            this.id = event.target.id;
            this.$emit('update-adRequest', this.id);
        },
        changeId(event) {
            this.id = event.target.id;
        }
    },
};
</script>