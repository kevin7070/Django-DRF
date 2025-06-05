<template>
  <div class="flex h-screen flex-1">
    <NuxtRouteAnnouncer />
    <!-- test -->
    <div
      class="flex min-h-full flex-1 items-center justify-center px-4 py-12 sm:px-6 lg:px-8"
    >
      <div class="w-full max-w-sm space-y-10">
        <div>
          <h2
            class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-900"
          >
            Sign in to your account
          </h2>
        </div>
        <form
          @submit.prevent="handleLogin"
          class="space-y-6"
          action="#"
          method="POST"
        >
          <div>
            <div class="col-span-2">
              <input
                name="identifiers"
                type="text"
                autocomplete="off"
                required
                aria-label="Identifiers"
                class="block w-full rounded-t-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:relative focus:outline-2 focus:-outline-offset-2 focus:outline-lime-600 sm:text-sm/6"
                placeholder="Username or Email"
                v-model="identifier"
              />
            </div>
            <div class="-mt-px grid grid-cols-1 items-center">
              <input
                name="password"
                :type="show_password ? 'text' : 'password'"
                autocomplete="off"
                required
                aria-label="Password"
                class="col-start-1 row-start-1 block w-full rounded-b-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:relative focus:outline-2 focus:-outline-offset-2 focus:outline-lime-600 sm:text-sm/6"
                :class="error ? 'border-red-600' : ''"
                placeholder="Password"
                v-model="password"
              />
              <div
                @click="toglePasswordVisibility"
                class="col-start-1 row-start-1 mr-3 justify-self-end text-gray-300 hover:text-lime-600 hover:cursor-pointer"
              >
                <EyeIcon
                  v-if="show_password"
                  class="size-6 text-lime-600"
                  aria-hidden="true"
                />
                <EyeSlashIcon
                  v-else-if="!show_password"
                  class="size-6"
                  aria-hidden="true"
                />
              </div>
            </div>
          </div>

          <div v-if="error">
            <p class="text-sm/6 text-red-500 text-shadow-sm text-center">
              {{ error }}
            </p>
          </div>

          <div class="flex items-center justify-end">
            <div class="text-sm/6">
              <a
                href="#"
                class="font-semibold text-lime-600 hover:text-lime-500"
                >Forgot password?</a
              >
            </div>
          </div>

          <div>
            <button
              type="submit"
              class="cursor-pointer flex w-full justify-center rounded-md bg-lime-600 px-3 py-1.5 text-sm/6 font-semibold text-white hover:bg-lime-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-lime-600"
            >
              Sign in
            </button>
          </div>
        </form>

        <p class="text-center text-sm/6 text-gray-500">
          Not a member?
          {{ " " }}
          <a href="#" class="font-semibold text-lime-600 hover:text-lime-500"
            >Join now</a
          >
        </p>
      </div>
    </div>
    <!-- test end -->
  </div>
</template>

<script setup lang="ts">
// test
import { EyeIcon, EyeSlashIcon } from "@heroicons/vue/24/outline";

const identifier = ref("");
const password = ref("");
const show_password = ref<boolean>(false);
const error = ref<string>("");

const userStore = useUserStore();

const handleLogin = async () => {
  error.value = "";
  try {
    await userStore.login(identifier.value, password.value);
    if (userStore.user) {
      console.log("Login successful");
    }
  } catch (e: any) {
    const detail =
      e?.data?.non_field_errors?.[0] ??
      "Server is under maintenance, please try again later";
    error.value = detail;
    console.error("Login failed", e);
  }
};

const toglePasswordVisibility = () => {
  show_password.value = !show_password.value;
};
// test end
</script>
