<template>
  <c-flex width="full" align="center" justifyContent="center">
    <c-box p="{2}">
      <c-box textAlign="center">
        <c-heading as="h2">Become a seller</c-heading>
        <c-box my="{4}" textAlign="left">
          <form @submit.prevent="submit"></form>
            <c-form-control is-required>
              <c-form-label for="url">Url</c-form-label>
              <c-input type="text" id="url" v-model="url" isRequired />
			  <c-form-helper-text id="email-helper-text">
    			one word e.g mystore
  				</c-form-helper-text>
            </c-form-control>
            <c-form-control is-required>
              <c-form-label for="name"> Name</c-form-label>
              <c-input type="text" id="name" v-model="name" isRequired />
            </c-form-control>
			<c-form-control is-required>
              <c-form-label for="mobile">Country</c-form-label>
              <c-box mb="3" w="300px">
                <c-select v-model="country_code" placeholder="Select Country">
                  <option value="NG">Nigeriar</option>
                  <option value="KE">Kenya</option>
				  <option value="GH">Ghana</option>
                  <option value="UK">United Kingdom</option>
                </c-select>
              </c-box>
            </c-form-control>
            <c-form-control>
              <c-form-label for="description">Description</c-form-label>
              <c-input type="description" id="description" v-model="description" />
            </c-form-control>
            <c-button
			  my="5"
              variant-color="blue"
              size="md"
              type="submit"
              @click="CreateSeller"
              :disabled="loading"
            >
              <p v-if="loading">Loading</p>
              {{ loading ? "" : "Submit" }}
            </c-button>
          </form>
        </c-box>
      </c-box>
    </c-box>
  </c-flex>
</template>

<script>
import Axios from "axios";
export default {
beforeRouteEnter(to, from, next) {
	if (localStorage.getItem("seller")) {
      return next({ path: "/dashboard" });
    }
    if (localStorage.getItem("user")) {
      return next();
	} 
    return next({ path: "/login" });

  },
  data() {
    return {
      url: "",
	  name: "",
	  country_code:"",
      description: "",
      password: "",
      errors: {},
      submitted: false,
      loading: false
    };
  },
  methods: {
    async CreateSeller() {
      try {
		this.loading = true;
		
        const { data } = await Axios.post(
          `${process.env.VUE_APP_API_URL}/seller/`,
          {
            name: this.name,
            url: this.url,
			description: this.description,
			country_code:this.country_code
		  },
		  { headers: { Authorization: `Token ${this.$root.user.token}` } }
        );
        if ((data.status = 201)) {
          localStorage.setItem("seller", JSON.stringify(data));
          this.$root.seller = data;
          this.submitted = true;
          this.loading = false;
          this.$noty.success("Seller Registration Successful");
          this.$router.push("/dashboard");
        }
      } catch (error) {
        this.loading = false;
        this.$noty.error("Oops Something went wrong");
      }
    }
  }
};
</script>


<style>
</style>