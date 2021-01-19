<template>
  <c-flex width="full" align="center" justifyContent="center">
    <c-box p="{2}">
      <c-box textAlign="center">
        <c-heading as="h2">Become a seller</c-heading>
        <c-box my="{4}" textAlign="left">
          <form @submit.prevent="submit">
            <c-form-control>
              <c-form-label for="url">Store Url</c-form-label>
              <c-input type="text" id="url" v-model="form.url" />
            </c-form-control>
            <c-form-control>
              <c-form-label for="name">Display name</c-form-label>
              <c-input type="text" id="name" v-model="form.name" />
            </c-form-control>
            <c-button my="2" variant-color="blue" size="md" type="submit">Submit</c-button>
          </form>
          <p v-if="showError" id="error">Username or Password is incorrect</p>
        </c-box>
      </c-box>
    </c-box>
  </c-flex>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "Seller",
  components: {},
  data() {
    return {
      form: {
        url: "",
        name: ""
      }
    };
  },
  //   created: function() {
  //     // a function to call getposts action
  //     this.GetPosts();
  //   },
  computed: {
    ...mapGetters({ User: "StateUser" })
  },
  methods: {
    ...mapActions(["CreateSeeller"]),
    async submit() {
      try {
        await this.CreateSeller(this.form);
      } catch (error) {
        throw "error occured";
      }
    }
  }
};
</script>