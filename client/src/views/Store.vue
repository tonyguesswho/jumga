<template>
  <div>
    <c-box v-if="active">
      <c-heading width="100" textAlign="center" bg="green.50" my="5">Store</c-heading>
      <c-flex justify="space-between">
        <c-text>Welcome to {{store.name}}</c-text>
        <c-button @click="goToCart">Go to Cart -- {{cart_count}} product(s) added</c-button>
      </c-flex>
      <c-box v-if="isProducts">
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
            <c-button @click="add(product)">{{ cart[product.id] ? "Added to cart" : "Add To Cart" }}</c-button>
          </c-flex>
        </c-flex>
      </c-box>
    </c-box>
    <c-box v-else textAlign="center">Store Does not exist</c-box>
  </div>
</template>
<script>
import Axios from "axios";
export default {
  mounted() {
    this.getStore();
    this.getProducts();
    this.createCart();
  },
  data() {
    return {
      active: false,
      store: {},
      loading: false,
      storeUrl: "",
      products: [],
      isProducts: false,
      cart_count: 0,
      cart: {},
      cart_id: null
    };
  },
  methods: {
    async getStore() {
      try {
        const { data } = await Axios.get(
          `${process.env.VUE_APP_API_URL}/seller/${this.$route.params.pathMatch}/`,
          {
            headers: { Authorization: `Token ${this.$root.user.token}` }
          }
        );
        if ((data.status = 200)) {
          this.store = data;
          this.active = data["is_active"];
          localStorage.setItem("store", JSON.stringify(data));
        }
      } catch (error) {
        this.loading = false;
        this.$noty.error("Oops Something went wrong");
      }
    },
    async getProducts() {
      try {
        const { data } = await Axios.get(
          `${process.env.VUE_APP_API_URL}/product/${this.$route.params.pathMatch}/`,
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
    },
    async createCart() {
      try {
        const { data } = await Axios.post(
          `${process.env.VUE_APP_API_URL}/cart/`,
          {}
        );
        if ((data.status = 200)) {
          this.cart_id = data.id;
          localStorage.setItem("cart_id", JSON.stringify(this.cart_id));
        }
      } catch (error) {
        this.loading = false;
        // this.$noty.error("Oops Something went wrong");
      }
    },
    async add(product) {
      if (this.cart[product.id]) {
        return;
      } else {
        this.cart[product.id] = product;
        this.cart_count += 1;
        localStorage.setItem("cart", JSON.stringify(this.cart));
        const { data } = await Axios.post(
          `${process.env.VUE_APP_API_URL}/cart/add/`,
          {
			  cart_id: this.cart_id,
			  product_id:product.id
		  }
        );
      }
    },
    goToCart() {
      this.$router.push("/order");
    }
  }
};
</script>


<style>
</style>