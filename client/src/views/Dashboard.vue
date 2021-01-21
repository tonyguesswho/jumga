<template>
  <div>
    <c-heading width="100" textAlign="center" bg="green.50" my="5">Seller's Dashboard</c-heading>
    <c-box v-if="!loading">
      <c-text>Store name: {{seller.name}}</c-text>
      <c-text>Store url: {{seller.url}}</c-text>
      <c-text>Dispatch Rider name: {{seller['rider'].name}}</c-text>
      <c-text>Dispatch Rider Email: {{seller['rider'].email}}</c-text>
    </c-box>

    <router-link :to="{ path: `store/${seller.url}`}">
      <c-button v-if="active && account">Go To Store</c-button>
    </router-link>
    <c-flex justify="center">
      <router-link to="/addproduct">
        <c-button v-if="account">Add Product</c-button>
      </router-link>
      <router-link to="/addaccount">
        <c-button v-if="active && !account">Add Account</c-button>
      </router-link>

      <c-button v-if="!active" @click="pay">
        <p v-if="loading">Loading</p>
        {{ loading ? "" : "Activate Store" }}
      </c-button>
    </c-flex>
    <c-box v-if="isProducts && account">
      <c-text fontSize="5xl" textAlign="center" fontWeight="bold">Products</c-text>
      <c-flex my="12" justify="center">
        <c-flex
          v-for="product in products"
          :key="product.title"
          flexDirection="column"
          bg="green.200"
          mx="4"
          p="10"
          w="sm"
          rounded="lg"
          align="center"
        >
          <c-text mt="6" textAlign="center" color="white" fontSize="xl">{{product.title}}</c-text>
          <c-text mt="6" textAlign="center" color="white" fontSize="xl">{{product.price}}</c-text>
        </c-flex>
      </c-flex>
    </c-box>
  </div>
</template>
<script>
import Axios from "axios";
export default {
  beforeRouteEnter(to, from, next) {
    if (localStorage.getItem("seller")) {
      return next();
    }
    return next({ path: "/seller" });
  },
  mounted() {
    this.settings();
    this.getUser();
    this.getaccount();
    this.getProducts();
  },
  data() {
    return {
      active: false,
      seller: {},
      account: null,
      loading: false,
      products: [],
      isProducts: false
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
        const { data } = await Axios.get(
          `${process.env.VUE_APP_API_URL}/account/${this.$root.user.user_id}`,
          {
            headers: { Authorization: `Token ${this.$root.user.token}` }
          }
        );
        if ((data.status = 200)) {
          if (data) {
            localStorage.setItem("account", JSON.stringify(data));
            this.$root.account = data;
            this.account = this.$root.account;
          }
        }
      } catch (error) {
        this.loading = false;
      }
    },
    async getProducts() {
      try {
        const { data } = await Axios.get(
          `${process.env.VUE_APP_API_URL}/product/${this.$root.seller.url}/`,
          {
            headers: { Authorization: `Token ${this.$root.user.token}` }
          }
        );
        if ((data.status = 200)) {
          this.loading = false;
          this.products = data;
          this.isProducts = true;
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