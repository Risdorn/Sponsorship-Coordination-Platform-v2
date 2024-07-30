<template>
    <div id="Flagged">
        <h3>Flagged Users</h3>
        <p v-if="flags.items.length == 0">No User Flagged.</p>
        <br v-else>
        <div v-for="user in flags.items">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">{{ user.name }}</h5>
                    <p class="card-text"><b>Email</b>: {{ user.email }}</p>
                    <p class="card-text"><b>Role</b>: {{ user.role }}</p>
                    <p v-if="user.role=='Influencer'" class="card-text"><b>Reach</b>: {{ user.reach }}</p>
                    <p v-if="user.role=='Influencer'" class="card-text"><b>Category</b>: {{ user.category }}</p>
                    <p v-if="user.role=='Sponsor'" class="card-text"><b>Industry</b>: {{ user.industry }}</p>
                    <button type="button" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#unflagUser" :id="user.id" onclick="changeId">
                        Unflag User
                    </button>
                    <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteUser" :id="user.id" onclick="changeId">
                        Delete User
                    </button>
                </div>
            </div>
            <br>
        </div>

        <!-- Unflag User Modal -->
        <div class="modal fade" id="unflagUser" tabindex="-1" role="dialog" aria-labelledby="unflagUser" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <form id="unflag">
                        <div class="modal-header">
                            <h5 class="modal-title" id="editProfileModalLabel">Unflag User</h5>
                        </div>
                        <div class="modal-body">
                            <p>Removing Flag, Are you sure?</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button class="btn btn-success" onclick="unflagUser">Unflag User</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <!-- Delete User Modal -->
        <div class="modal fade" id="deleteUser" tabindex="-1" role="dialog" aria-labelledby="deleteUser" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <form id="delete">
                        <div class="alert alert-danger" role="alert">
                            Deleting User will remove all associated data.
                        </div>
                        <div class="modal-header">
                            <h5 class="modal-title" id="editProfileModalLabel">Delete User</h5>
                        </div>
                        <div class="modal-body">
                            <p>Are you sure?</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button class="btn btn-danger" onclick="deleteUser">Delete User</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <!-- Navigation section for pagination controls -->
        <nav aria-label="Flag Page navigation">
            <ul class="pagination">
                <!-- Check if there is a previous page -->
                <li v-if="flags.has_prev" class="page-item">
                    <!-- If there is, create a link to the previous page -->
                    <a class="page-link" @click="handlePageChange(flags.prev_num)">Previous</a>
                </li>
                <!-- If not, show a disabled 'Previous' button -->
                <li v-else class="page-item disabled"><span class="page-link">Previous</span></li>

                <!-- Loop through each page number provided by pagination.iter_pages() -->
                <div v-for="page_num in flags.iter_pages()">
                    <!-- Check if the page number exists (not None) -->
                    <li v-if="page_num" class="page-item">
                        <!-- Check if the current page is not the active page -->
                        <a v-if="page_num != flags.page" class="page-link" @click="handlePageChange(page_num)">{{ page_num }}</a>
                        <!-- Highlight the current page as active and not clickable -->
                        <span v-else class="page-link">{{ page_num }}</span>
                    </li>
                    <!-- For gaps in the pagination links, show ellipsis -->
                    <li v-else class="page-item disabled"><span class="page-link">...</span></li>
                </div>

                <!-- Check if there is a next page -->
                <li v-if="flags.has_next" class="page-item">
                    <!-- If there is, create a link to the next page -->
                    <a class="page-link" @click="handlePageChange(flags.next_num)">Next</a>
                </li>
                <!-- If not, show a disabled 'Next' button -->
                <li v-else class="page-item disabled"><span class="page-link">Next</span></li>
            </ul>
        </nav>
    </div>
</template>

<script>
export default {
    name: 'FlaggedList',
    props: {
        flaggedPage: Function,
    },
    data() {
        return {
            flagged: null,
            reason: '',
            id: ''
        };
    },
    methods: {
        async handlePageChange(page_num) {
            this.flagged = await this.flaggedPage(page_num);
        },
        async unflagUser() {
            try {
                const response = await fetch('http://localhost:5000/api/unflag', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization-Token': localStorage.getItem('token')
                    },
                    body: JSON.stringify({
                        user_id: this.id
                    })
                });
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.message || 'Failed to unflag user');
                }
                console.log(data);
                this.$router.go();
            } catch (error) {
                console.error(error);
            }
        },
        async deleteUser() {
            try {
                const response = await fetch('http://localhost:5000/api/delete', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization-Token': localStorage.getItem('token')
                    },
                    body: JSON.stringify({
                        user_id: this.id
                    })
                });
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.message || 'Failed to delete user');
                }
                console.log(data);
                this.$router.go();
            } catch (error) {
                console.error(error);
            }
        },
        changeId(event) {
            this.id = event.target.id;
        },
    },
    created() {
        this.handlePageChange(1);
    }
};
</script>