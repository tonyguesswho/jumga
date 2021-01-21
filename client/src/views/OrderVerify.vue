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
        const {
          data
        } = await Axios.get(
		  `${process.env.VUE_APP_API_URL}/order-payment/${this.$route.query.transaction_id}/${this.$route.query.tx_ref}/`,
        );
        if ((data.status = 200)) {
          this.submitted = true;
          this.loading = false;
		  this.$noty.success("Payment Confirmed");
		  localStorage.removeItem('cart')
		  localStorage.removeItem('cart_id')
		  this.$router.push(`/store/${JSON.parse(localStorage.getItem("seller")).url}`);
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