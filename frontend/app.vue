<template>
  <div>
    <NuxtRouteAnnouncer />
    <!-- test -->
    <form @submit.prevent="submit">
      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <button type="submit">Login</button>
    </form>
    <p class="text-lg">Tailwindcss</p>
    <!-- test end -->
  </div>
</template>

<script setup lang="ts">
// test
const username = ref("");
const password = ref("");
const userStore = useUserStore();

const submit = async () => {
  try {
    await userStore.login(username.value, password.value);
    console.log("Login successful");
  } catch (e) {
    console.error("Login failed", e);
  }
};
// test end
</script>
