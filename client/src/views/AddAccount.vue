<template>
  <c-flex width="full" align="center" justifyContent="center">
    <c-box p="{2}">
      <c-box textAlign="center">
        <c-heading as="h2">Add Account</c-heading>
        <c-box my="{4}" textAlign="left">
          <form @submit.prevent="submit">
            <c-form-control is-required>
              <c-form-label for="account_number">Account Number</c-form-label>
              <c-input type="text" id="account_number" v-model="account_number" />
            </c-form-control>
            <c-form-control is-required>
              <c-form-label for="mobile">Mobile Number</c-form-label>
              <c-input type="text" id="mobile" v-model="mobile" />
            </c-form-control>
            <c-form-control is-required>
              <c-form-label for="mobile">Bank</c-form-label>
              <c-box mb="3" w="300px">
                <c-select v-model="bank_code" placeholder="Select Bank">
                  <option :value="bank.code" v-for="bank in banks" :key="bank.code">{{bank.name}}</option>    
                </c-select>
              </c-box>
            </c-form-control>
            <c-button
              my="5"
              variant-color="blue"
              size="md"
              type="submit"
              @click="add"
              :disabled="loading"
            >
              <p v-if="loading">Loading</p>
              {{ loading ? "" : "Add" }}
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
      return next();
    }
    return next({ path: "/" });
  },
  mounted() {
    this.getBanks();
  },
  data() {
    return {
      account_number: "",
      mobile: "",
      country_code: "",
      bank_code: "",
      errors: {},
      banks:[],
      submitted: false,
      loading: false
    };
  },
  methods: {
    async add() {
      try {
        this.loading = true;
        const { data } = await Axios.post(
          `${process.env.VUE_APP_API_URL}/account/`,
          {
            account_number: this.account_number,
            mobile: this.mobile,
            bank_code: this.bank_code,
            country_code: this.$root.seller.country_code
          },
          { headers: { Authorization: `Token ${this.$root.user.token}` } }
        );
        if ((data.status = 201)) {
          this.submitted = true;
          this.loading = false;
          this.$router.push("/dashboard");
          this.$noty.success("Account added");
        }
      } catch (error) {
        this.loading = false;
        this.$noty.error("Oops Something went wrong");
      }
    },
    async getBanks() {
      try {
        const { data } = await Axios.get(
          `${process.env.VUE_APP_API_URL}/getbanks/${this.$root.seller.country_code}/`,
          {
            headers: { Authorization: `Token ${this.$root.user.token}` }
          }
        );
        if ((data.status = 200)) {

          this.loading = false;
          this.banks = data.data
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