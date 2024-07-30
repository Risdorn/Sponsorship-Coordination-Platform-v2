<template>
  <section class="vh-100">
      <div class="container-fluid h-custom">
          <div class="row d-flex justify-content-center align-items-center h-100">
              <div class="col-md-9 col-lg-6 col-xl-5">
                  <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/draw2.webp"
                  class="img-fluid" alt="Sample image">
              </div>
              <div class="col-md-9 col-lg-6 col-xl-5 offset-xl-1">
                  <div v-if="error" class="alert alert-danger" role="alert">
                      {{ error }}
                  </div>
                  <h1 class="mt-5 mb-4" >{{ text }}</h1>
                  <form>
                      
                      <ul>
                          <li><label class="form-label">Only Alphabets, Numbers and Underscore allowed in Name</label></li>
                          <li><label class="form-label">Password must be at least 8 characters long</label></li>
                          <li><label class="form-label">Password must contain at least 1 Uppercase and Lowercase letter</label></li>
                          <li><label class="form-label">Password must contain at least 1 Number and a Special character</label></li>
                          <li v-if="role == 'Influencer'"><label class="form-label">Reach must be a number greater than 0</label></li>
                      </ul>
                      
                      <!-- Name input -->
                      <div data-mdb-input-init class="form-outline mb-4">
                          <input type="text" name="name" id="Full_Name" v-model="name" class="form-control" required maxlength="45" pattern="^[a-zA-Z0-9_]+"/>
                          <label class="form-label" for="Full_Name">Full Name</label>
                      </div>
                      
                      <!-- Email input -->
                      <div data-mdb-input-init class="form-outline mb-4">
                          <input type="email" id="Email" name="email" v-model="email" class="form-control" />
                          <label class="form-label" for="Email">Email address</label>
                      </div>
                  
                      <!-- Password input -->
                      <div data-mdb-input-init class="form-outline mb-4">
                          <input type="password" id="Pass" name="pass" v-model="password" class="form-control" required minlength="8" pattern="^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*\W)(?!.* ).{8,}$"/>
                          <label class="form-label" for="Pass">Password</label>
                      </div>

                      <!-- Password input -->
                      <div data-mdb-input-init class="form-outline mb-4">
                          <input type="password" id="Con_Pass" name="con_pass" v-model="confirm_password" class="form-control" required minlength="8"/>
                          <label class="form-label" for="con_pass">Confirm Password</label>
                      </div>
                      
                      <!-- Category input -->
                      <div v-if="role == 'Influencer'" data-mdb-input-init class="form-outline mb-4">
                          <select id="category" name="category" v-model="category" class="form-control" required>
                              <option value="" disabled selected>Choose your Category</option>
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
                      <div v-if="role == 'Influencer'" data-mdb-input-init class="form-outline mb-4">
                          <input type="number" id="Reach" name="reach" v-model="reach" class="form-control" required maxlength="45" pattern="^[0-9]+$"/>
                          <label class="form-label" for="Reach">Reach</label>
                      </div>

                      <!-- Industry input -->
                      <div v-if="role == 'Sponsor'" data-mdb-input-init class="form-outline mb-4">
                          <select id="Industry" name="industry" v-model="industry" class="form-control" required>
                              <option value="" disabled selected>Choose your Industry</option>
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

                      <!-- Submit button -->
                      <button data-mdb-button-init data-mdb-ripple-init class="btn btn-primary btn-block mb-4" onclick="registerUser">Sign up</button>
                  
                      <!-- Login buttons -->
                      <div class="text-center">
                      <p>Already Registered? <a href="/login">Sign In</a></p>
                      <p>Register as <a v-if="role == 'Sponsor'" onclick="changeRole">Influencer</a><a v-if="role == 'Influencer'" onclick="changeRole">Sponsor</a></p>
                      </div>
                  </form>
              </div>
          </div>
      </div>
  </section>
</template>

<script>
export default {
name: 'RegisterView',
data() {
  return {
    name: '',
    email: '',
    password: '',
    confirm_password: '',
    category: '',
    industry: '',
    reach: '',
    error: '',
    role: 'Sponsor',
    text: 'Register as Sponsor'
  }
}, methods: {
    changeRole() {
        if (this.role == 'Sponsor') {
            this.role = 'Influencer';
            this.text = 'Register as Influencer';
        } else {
            this.role = 'Sponsor';
            this.text = 'Register as Sponsor';
        }
    },
    async registerUser() {
        if (this.password != this.confirm_password) {
            this.error = 'Passwords do not match';
            return;
        }
        const response = await fetch('http://localhost:5000/api/auth/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: this.name,
                email: this.email,
                password: this.password,
                role: this.role,
                category: this.category,
                industry: this.industry,
                reach: this.reach
            })
        });
        const data = await response.json();
        if (data.message) {
            this.error = data.message;
        } else {
            data.role = data.role.toLowerCase();
            localStorage.setItem('token', data.token);
            localStorage.setItem('role', data.role);
            localStorage.setItem('email', data.email);
            this.$router.push('/role');
        }
    },
},
metaInfo: {
    title: 'Register Page',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { name: 'description', content: 'Register Page' }
    ]
  }
}
</script>