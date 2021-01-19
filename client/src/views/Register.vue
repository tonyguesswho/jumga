<template>
  <c-flex width="full" align="center" justifyContent="center">
    <c-box p="{2}">
      <c-box textAlign="center">
        <c-heading as="h2">Register</c-heading>
        <c-box my="{4}" textAlign="left">
          <form @submit.prevent="submit">
            <c-form-control>
              <c-form-label for="email">Email address</c-form-label>
              <c-input type="email" id="email" v-model="form.email" />
            </c-form-control>
            <c-form-control>
              <c-form-label for="first_name">First Name</c-form-label>
              <c-input type="text" id="first_name" v-model="form.first_name" />
            </c-form-control>
            <c-form-control>
              <c-form-label for="last_name">Last Name</c-form-label>
              <c-input type="text" id="last_name" v-model="form.last_name" />
            </c-form-control>
            <c-form-control>
              <c-form-label for="password">Password</c-form-label>
              <c-input type="password" id="password" v-model="form.password" />
            </c-form-control>
            <c-button variant-color="blue" size="md" type="submit">Submit</c-button>
          </form>
          <p v-if="showError" id="error">Username already exists</p>
        </c-box>
      </c-box>
    </c-box>
  </c-flex>
</template>

<script>
import { mapActions } from "vuex";
export default {
  name: "Register",
  components: {},
  data() {
    return {
      form: {
        email: "",
        first_name: "",
        last_name: "",
        password: ""
      },
      showError: false
    };
  },
  methods: {
    ...mapActions(["Register"]),
    async submit() {
      try {
        await this.Register(this.form);
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