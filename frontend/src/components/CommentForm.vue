<template>
  <form @submit.prevent="submit">
    <label>User name</label>
    <input v-model="form.user_name" required />
    <label>Email</label>
    <input v-model="form.email" type="email" required />
    <label>Home page</label>
    <input v-model="form.homepage" type="url" />
    <label>Text</label>
    <textarea v-model="form.text" required></textarea>
    <!-- captcha: show image and input -->
    <img :src="captcha.image" alt="captcha" />
    <input v-model="form.captcha_value" required />
    <button type="submit">Send</button>
  </form>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      form: {
        user_name: "",
        email: "",
        homepage: "",
        text: "",
        captcha_value: "",
        captcha_key: "",
        parent: null,
      },
      captcha: { image: null, key: null },
    };
  },
  async created() {
    await this.loadCaptcha();
  },
  methods: {
    async loadCaptcha() {
      const res = await axios.get("/api/captcha/"); // реализуйте endpoint
      this.captcha = res.data;
      this.form.captcha_key = res.data.key;
    },
    async submit() {
      try {
        const payload = { ...this.form };
        await axios.post("/api/comments/", payload);
        this.$emit("submitted");
        await this.loadCaptcha();
      } catch (err) {
        alert("Error: " + err);
      }
    },
  },
};
</script>