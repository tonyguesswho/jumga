<template>
  <c-flex mx="20" my="10" justify="space-between" bg="blue.50" p="10">
    <c-flex>
      <router-link to="/">
        <c-text fontWeight="bold">Jumga</c-text>
      </router-link>
    </c-flex>
    <c-flex>
      <router-link to="/login">
        <c-button marginRight="10" variant="outline" color="gray.700" size="sm">login</c-button>
      </router-link>
      <router-link to="/register">
        <c-button variant="outline" color="gray.700" size="sm">Register</c-button>
      </router-link>

      <!-- <c-text paddingRight="10">Menu 3</c-text> -->
      <!-- <c-text>Menu 4</c-text> -->
    </c-flex>
    <c-flex>
      <c-button
        v-if="isLoggedIn"
        @click="logout"
        variant="outline"
        color="gray.700"
        size="sm"
      >Logout</c-button>
    </c-flex>
  </c-flex>
</template>

<script>
export default {
  name: "NavBar",
  computed: {
    isLoggedIn: function() {
      return this.$store.getters.isAuthenticated;
    }
  },
  methods: {
    async logout() {
      await this.$store.dispatch("LogOut");
      this.$router.push("/login");
    }
  }
};
</script>

<style>
</style>
