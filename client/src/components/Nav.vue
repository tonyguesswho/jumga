<template>
  <c-flex mx="20" my="10" justify="space-between" bg="blue.50" p="10">
    <c-flex>
      <router-link to="/">
        <c-text fontWeight="bold">Jumga</c-text>
      </router-link>
    </c-flex>
    <c-flex>
      <router-link to="/login" v-if="!isAuth">
        <c-button marginRight="10" variant="outline" color="gray.700" size="sm">login</c-button>
      </router-link>
      <router-link to="/register" v-if="!isAuth">
        <c-button variant="outline" color="gray.700" size="sm">Register</c-button>
      </router-link>
      <router-link to="/dashboard" v-if="isAuth">
        <c-button marginRight="10" variant="outline" color="gray.700" size="sm">Dashboard</c-button>
      </router-link>

      <!-- <c-text paddingRight="10">Menu 3</c-text> -->
      <!-- <c-text>Menu 4</c-text> -->
    </c-flex>
    <c-flex>
      <c-button variant="outline" color="gray.700" size="sm" v-if="isAuth" @click="logout">Logout</c-button>
    </c-flex>
  </c-flex>
</template>

<script>
export default {
  computed: {
    isAuth() {
      return this.$root.user;
    }
  },
  methods: {
    logout() {
      localStorage.removeItem("user");
      localStorage.removeItem("seller");
      this.$root.user = {};
      this.$root.seller = {};
      this.$noty.success("Successful Logged Out");
      this.$router.push("/");
    }
  }
};
</script>

<style>
</style>
