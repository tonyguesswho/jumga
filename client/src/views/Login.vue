<template>
  <c-flex width="full" align="center" justifyContent="center">
    <c-box p="{2}">
      <c-box textAlign="center">
        <c-heading as="h2">Login</c-heading>
        <c-box my="{4}" textAlign="left">
          <form @submit.prevent="submit">
            <c-form-control>
              <c-form-label for="email">Email address</c-form-label>
              <c-input type="email" id="email" v-model="form.email" />
            </c-form-control>
            <c-form-control>
              <c-form-label for="first_name">password</c-form-label>
              <c-input type="text" id="first_name" v-model="form.password" />
            </c-form-control>
            <c-button my="2" variant-color="blue" size="md" type="submit">Submit</c-button>
          </form>
          <p v-if="showError" id="error">Username or Password is incorrect</p>
        </c-box>
      </c-box>
    </c-box>
  </c-flex>
</template>

<script>
import { mapActions } from "vuex";
export default {
  name: "Login",
  components: {},
  data() {
    return {
      form: {
        email: "",
        password: ""
      },
      showError: false
    };
  },
  methods: {
    ...mapActions(["LogIn"]),
    async submit() {
      const User = new FormData();
      User.append("email", this.form.email);
      User.append("password", this.form.password);
      try {
        await this.LogIn(User);
        this.$router.push("/seller");
        this.showError = false;
      } catch (error) {
        this.showError = true;
      }
    }
  }
};
</script>

<style>
</style>