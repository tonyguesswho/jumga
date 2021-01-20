<template>
  <c-flex width="full" align="center" justifyContent="center">
    <c-box p="{2}">
      <c-box textAlign="center">
        <c-heading as="h2">Register</c-heading>
        <c-box my="{4}" textAlign="left">
          <form @submit.prevent="submit">
            <c-form-control>
              <c-form-label for="email">Email address</c-form-label>
              <c-input type="email" id="email" v-model="email" />
            </c-form-control>
            <c-form-control>
              <c-form-label for="first_name">First Name</c-form-label>
              <c-input type="text" id="first_name" v-model="first_name" />
            </c-form-control>
            <c-form-control>
              <c-form-label for="last_name">Last Name</c-form-label>
              <c-input type="text" id="last_name" v-model="last_name" />
            </c-form-control>
            <c-form-control>
              <c-form-label for="password">Password</c-form-label>
              <c-input type="password" id="password" v-model="password" />
            </c-form-control>
            <c-button
              my="5"
              variant-color="blue"
              size="md"
              type="submit"
              @click="registerUser"
              :disabled="loading"
            >
              <p v-if="loading">Loading</p>
              {{ loading ? "" : "Signup" }}
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
    if (localStorage.getItem("user")) {
      return next({ path: "/" });
    }
    next();
  },
  data() {
    return {
      first_name: "",
      last_name: "",
      email: "",
      password: "",
      errors: {},
      submitted: false,
      loading: false
    };
  },
  methods: {
    async registerUser() {
      try {
        this.loading = true;
        const { data } = await Axios.post(
          `${process.env.VUE_APP_API_URL}/register/`,
          {
            first_name: this.first_name,
            last_name: this.last_name,
            email: this.email,
            password: this.password
          }
        );
        if ((data.status = 201)) {
          localStorage.setItem("user", JSON.stringify(data));
          this.$root.user = data;
          this.submitted = true;
          // this.authenticateUser();
          this.loading = false;
          this.$noty.success("Successful Registration");
          this.$router.push("/seller");
        }
      } catch (error) {
        this.loading = false;
        // this.errors = error.response.data.errors;
        this.$noty.error("Oops Something went wrong");
      }
    }
  }
};
</script>


<style>
</style>