<template>
  <c-flex width="full" align="center" justifyContent="center">
    <c-box p="{2}">
      <c-box textAlign="center">
        <c-heading as="h2">Login</c-heading>
        <c-box my="{4}" textAlign="left">
          <form @submit.prevent="submit">
            <c-form-control>
              <c-form-label for="email">Email address</c-form-label>
              <c-input type="email" id="email" v-model="email" />
            </c-form-control>
            <c-form-control>
              <c-form-label for="password">password</c-form-label>
              <c-input type="text" id="password" v-model="password" />
            </c-form-control>
            <c-button
              my="5"
              variant-color="blue"
              size="md"
              type="submit"
              @click="loginUser"
              :disabled="loading"
            >
              <p v-if="loading">Loading</p>
              {{ loading ? "" : "Login" }}
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
      email: "",
      password: "",
      errors: {},
      submitted: false,
      loading: false
    };
  },
  methods: {
    async loginUser() {
      try {
        this.loading = true;
        const { data } = await Axios.post(
          `${process.env.VUE_APP_API_URL}/login/`,
          {
            username: this.email,
            password: this.password
          }
        );
        if ((data.status = 200)) {
          localStorage.setItem("user", JSON.stringify(data));
          this.$root.user = data;
          this.submitted = true;
          this.getUser();
          this.loading = false;
          this.$router.push("/dashboard");
        }
      } catch (error) {
        this.loading = false;
        // this.errors = error.response.data.errors;
        this.$noty.error("Oops Something went wrong");
      }
    },
    async getUser() {
      try {
        const { data } = await Axios.get(`${process.env.VUE_APP_API_URL}/me/`, {
          headers: { Authorization: `Token ${this.$root.user.token}` }
        });
        if ((data.status = 200)) {
          if (data.seller) {
            localStorage.setItem("seller", JSON.stringify(data.seller));
            this.$root.seller = data.seller;
          }
          this.$noty.success("Successful Login");
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