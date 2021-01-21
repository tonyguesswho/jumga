<template>
  <div>
    <c-box v-if="cart">
      <c-heading width="100" textAlign="center" bg="green.50" my="5">My cart</c-heading>
      <c-box>
        <c-flex my="12" justify="center">
          <c-flex v-for="product in cart" :key="product.title">
            <c-text>{{product.title}}------{{product.price}}</c-text>
          </c-flex>
        </c-flex>
        <form @submit.prevent="submit">
          <c-form-control is-required>
            <c-form-label for="email">Email address</c-form-label>
            <c-input type="email" id="email" v-model="email" />
          </c-form-control>
          <c-button
            my="5"
            variant-color="blue"
            size="md"
            type="submit"
            @click="pay"
            :disabled="loading"
          >
            <p v-if="loading">Loading</p>
            {{ loading ? "" : "Pay" }}
          </c-button>
        </form>
      </c-box>
    </c-box>
    <c-box v-else textAlign="center">No product in cart</c-box>
  </div>
</template>
<script>
import Axios from "axios";
export default {
  mounted() {
    this.getCart();
  },
  data() {
    return {
      cart: null,
      email: ""
    };
  },
  methods: {
    getCart() {
      const cart_values = JSON.parse(localStorage.getItem("cart"));
      this.cart = Object.values(cart_values);
    },
    async pay() {
      try {
        this.loading = true;
        const { data } = await Axios.post(
          `${process.env.VUE_APP_API_URL}/order/payment/`,
          {
            cart: JSON.parse(localStorage.getItem("cart_id")),
            email: this.email,
            seller: JSON.parse(localStorage.getItem("seller")).id
          }
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
    }
  }
};
</script>


<style>
</style>