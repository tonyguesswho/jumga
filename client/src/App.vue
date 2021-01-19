<template>
  <c-theme-provider>
    <c-reset />
    <!--Your application goes here -->
    <Nav />
    <router-view/>
    <!-- <Register /> -->
    <!-- <Body /> -->
    
  </c-theme-provider>
</template>

<script>
import Nav from "./components/Nav.vue";
import Body from "./components/Body.vue";
// import Register from "./components/Register.vue";

export default {
  name: "App",
  components: {
    Nav,
    Body,
    // Register
  }
};
</script>
