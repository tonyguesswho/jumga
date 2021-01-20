<template>
  <c-flex width="full" align="center" justifyContent="center">
    <c-box p="{2}">
      <c-box textAlign="center">
        <c-heading as="h2">Login</c-heading>
        <c-box my="{4}" textAlign="left">
          <form @submit.prevent="submit">
            <c-form-control>
              <c-form-label for="email">Email address</c-form-label>
              <c-input type="email" id="email"  />
            </c-form-control>
            <c-form-control>
              <c-form-label for="first_name">password</c-form-label>
              <c-input type="text" id="first_name"  />
            </c-form-control>
            <c-button my="5" variant-color="blue" size="md" type="submit">Submit</c-button>
          </form>
        </c-box>
      </c-box>
    </c-box>
  </c-flex>
</template>

<script>
</script>

<style>
</style>