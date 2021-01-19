<template>
  <c-theme-provider>
    <c-reset />
    <!--Your application goes here -->
    <Nav />
  </c-theme-provider>
</template>

<script>
import Nav from './components/Nav.vue';

export default {
  name: 'App',
  components: {
    Nav,
  },
};
</script>
