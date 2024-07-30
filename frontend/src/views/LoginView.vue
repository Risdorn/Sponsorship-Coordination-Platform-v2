<template>
    <div v-if="error" class="alert alert-danger" role="alert">
        {{ error }}
    </div>
    <section class="vh-100">
    <div class="container-fluid h-custom">
        <div class="row d-flex justify-content-center align-items-center h-100">
            <div class="col-md-9 col-lg-6 col-xl-5">
                <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/draw2.webp"
                class="img-fluid" alt="Sample image">
            </div>
        <div class="col-md-9 col-lg-6 col-xl-5 offset-xl-1">
            <h1 class="mt-5 mb-4" >Sign In</h1>
            <form @submit.prevent="loginUser">
            <!-- Email input -->
            <div data-mdb-input-init class="form-outline mb-4">
                <input type="email" id="Email" name="email" class="form-control" v-model="email" required/>
                <label class="form-label" for="Email">Email address</label>
            </div>
                        
            <!-- Password input -->
            <div data-mdb-input-init class="form-outline mb-4">
                <input type="password" id="Pass" name="pass" class="form-control" required v-model="password" minlength="8"/>
                <label class="form-label" for="Pass">Password</label>
            </div>
                        
            <!-- Submit button -->
            <button type="submit" data-mdb-button-init data-mdb-ripple-init class="btn btn-primary btn-block mb-4">Sign In</button>
                        
            <!-- Login buttons -->
            <div class="text-center">
                <p>Not a member? <a href="/register">Sign Up</a></p>
            </div>
            </form>
        </div>
        </div>
    </div>
    </section>
</template>

<script>
export default {
name: 'LoginView',
data() {
    return {
        email: '',
        password: '',
        error: null
    };
},
methods: {
    async loginUser() {
        try {
            const response = await fetch('http://localhost:5000/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: this.email,
                    password: this.password
                })
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Failed to login');
            }
            this.error = null;
            localStorage.setItem('token', data.token);
            localStorage.setItem('role', data.role.toLowerCase());
            localStorage.setItem('email', data.email);
            console.log(data);
            var path = '/' + data.role.toLowerCase();
            this.$router.push(path);
        } catch (error) {
            this.error = error.message;
        }
    },
},
metaInfo: {
    title: 'Login Page',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { name: 'description', content: 'Login Page' }
    ]
  }
}
</script>