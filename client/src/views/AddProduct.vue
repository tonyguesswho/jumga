<template>
  <c-flex width="full" align="center" justifyContent="center">
    <c-box p="{2}">
      <c-box textAlign="center">
        <c-heading as="h2">Add Product</c-heading>
        <c-box my="{4}" textAlign="left">
          <form @submit.prevent="submit">
            <c-form-control>
              <c-form-label for="title">Product Name</c-form-label>
              <c-input type="title" id="title" v-model="title" />
            </c-form-control>
            <c-form-control>
              <c-form-label for="price">Price</c-form-label>
              <c-input type="price" id="price" v-model="price" />
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
  data() {
    return {
      title: "",
      price: "",
      errors: {},
      submitted: false,
      loading: false
    };
  },
  methods: {
    async add() {
      try {
        this.loading = true;
        const { data } = await Axios.post(
          `${process.env.VUE_APP_API_URL}/product/`,
          {
            title: this.title,
			price: this.price,
			seller:this.$root.seller.id
          },
          { headers: { Authorization: `Token ${this.$root.user.token}` } }
        );
        if ((data.status = 201)) {
          this.submitted = true;
          this.loading = false;
		  this.$router.push("/dashboard");
		  this.$noty.success("Product added");
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