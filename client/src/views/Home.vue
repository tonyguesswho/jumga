<template>
  <c-box>
    <c-text fontSize="5xl" textAlign="center" fontWeight="bold">Top jumga stores</c-text>
    <c-flex my="12" justify="center">
      <c-flex
        v-for="store in stores"
        :key="store.name"
        flexDirection="column"
        bg="green.200"
        mx="4"
        p="10"
        w="sm"
        rounded="lg"
        align="center"
      >
        <c-text mt="6" textAlign="center" color="white" fontSize="xl">{{store.name}}</c-text>
        <router-link :to="{ path: `store/${store.url}`}">
          <c-button>Go To Store</c-button>
        </router-link>
      </c-flex>
    </c-flex>
  </c-box>
</template>

<script>
import Axios from "axios";
export default {
  mounted() {
    this.getStores();
  },
  data() {
    return {
      stores: [],
      isStores: false
    };
  },
  methods: {
    async getStores() {
      try {
        const { data } = await Axios.get(
          `${process.env.VUE_APP_API_URL}/stores/`
        );
        if ((data.status = 200)) {
          this.loading = false;
          this.stores = data;
          this.isStores = true;
        }
      } catch (error) {
        this.loading = false;
        this.$noty.error("Oops Something went wrong");
      }
    }
  }
};
</script>