<template>
  <div v-if="loading">Verifying payment .....</div>
</template>
<script>
import Axios from "axios";
export default {
  mounted() {
    this.verify();
  },
  data() {
    return {
      active: true,
      seller: {},
      loading: false
    };
  },
  methods: {
    async verify() {
      try {
		this.loading = true;
		console.log(this.$root.user.token, "ooooo")
        const {
          data
        } = await Axios.get(
		  `${process.env.VUE_APP_API_URL}/seller/confirm-payment/${this.$route.query.transaction_id}/${this.$route.query.tx_ref}/`,
          { headers: { Authorization: `Token ${this.$root.user.token}` } }
        );
        if ((data.status = 200)) {
          this.submitted = true;
          this.loading = false;
          this.$router.push("/dashboard");
          this.$noty.success("Payment Confirmed");
        }
      } catch (error) {
        this.loading = false;
        this.$noty.error("Oops Something went wrong/ Paymeent not verified");
      }
    }
  }
};
</script>


<style>
</style>