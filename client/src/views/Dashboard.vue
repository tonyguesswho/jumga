<template>
  <div>
    <c-heading width="100" textAlign="center" bg="green.50" my="5">Seller's Dashboard</c-heading>
    <c-text>Store name: {{seller.name}}</c-text>
    <c-flex justify="center">
      <c-button v-if="active">Add Product</c-button>
      <c-button v-if="!active" @click="pay"> <p v-if="loading">Loading</p>
              {{ loading ? "" : "Activate Store" }}</c-button>
    </c-flex>
  </div>
</template>
 <p v-if="loading">Loading</p>
              {{ loading ? "" : "Signup" }}
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
    this.settings();
  },
  data() {
    return {
      active: true,
	  seller: {},
	  loading:false
    };
  },
  methods: {
    settings() {
      (this.active = this.$root.seller.is_active),
        (this.seller = this.$root.seller);
    },
    async pay() {
      try {
        this.loading = true;
        const { data } = await Axios.post(
          `${process.env.VUE_APP_API_URL}/seller/payment/`,
          {
		  },
		  { headers: { Authorization: `Token ${this.$root.user.token}` } }
        );
        if ((data.status = 201)) {
          localStorage.setItem("userf", JSON.stringify(data));
        //   this.$root.user = data;
          this.submitted = true;
          // this.authenticateUser();
		  this.loading = false;
		  window.location.href = 'https://checkout-testing.herokuapp.com/v3/hosted/pay/55b21c221abf525f6323'
          this.$noty.success("Redirecting");
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