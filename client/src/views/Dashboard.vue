<template>
  <div>
    <c-heading width="100" textAlign="center" bg="green.50" my="5">Seller's Dashboard</c-heading>
    <c-text>Store name: {{seller.name}}</c-text>
    <c-flex justify="center">
		<router-link to="/addaccount"><c-button v-if="active">Add Account</c-button></router-link>
      <router-link to="/addproduct"><c-button v-if="account">Add Product</c-button></router-link>
      <c-button v-if="!active" @click="pay">
        <p v-if="loading">Loading</p>
        {{ loading ? "" : "Activate Store" }}
      </c-button>
    </c-flex>
  </div>
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
	this.settings();
	this.getUser()
	this.getaccount()
  },
  data() {
    return {
      active: false,
	  seller: {},
	  account:null,
      loading: false
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
          {},
          { headers: { Authorization: `Token ${this.$root.user.token}` } }
        );
        if ((data.status = 200)) {
          this.submitted = true;
          this.loading = false;
          window.location.href = data["data"]["link"];
          this.$noty.success("Redirecting");
        }
      } catch (error) {
        this.loading = false;
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
        }
      } catch (error) {
        this.loading = false;
        this.$noty.error("Oops Something went wrong");
      }
	},
	    async getaccount() {
      try {
        const { data } = await Axios.get(`${process.env.VUE_APP_API_URL}/account/${this.$root.user.user_id}`, {
          headers: { Authorization: `Token ${this.$root.user.token}` }
        });
        if ((data.status = 200)) {
          if (data) {
            localStorage.setItem("account", JSON.stringify(data));
			this.$root.account = data;
			this.account = this.$root.account
          }
        }
      } catch (error) {
        this.loading = false;	
      }
    }
  }
};
</script>


<style>
</style>