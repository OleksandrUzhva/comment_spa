<template>
  <div>
    <table>
      <thead>
        <tr>
          <th @click="changeOrder('user_name')">User Name</th>
          <th @click="changeOrder('email')">E-mail</th>
          <th @click="changeOrder('created_at')">Added at</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="c in comments" :key="c.id">
          <td>{{ c.user_name }}</td>
          <td>{{ c.email }}</td>
          <td>{{ c.created_at }}</td>
        </tr>
      </tbody>
    </table>

    <div style="margin-top:12px;">
      <button v-if="nextUrl" @click="loadMore">Load more</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  props: ["comments"],
  data() {
    return {
      ordering: "-created_at",
      nextUrl: null,
    };
  },
  methods: {
    async changeOrder(field) {
      if (this.ordering === field) this.ordering = "-" + field;
      else this.ordering = field;
      const res = await axios.get(`/api/comments/?ordering=${this.ordering}`);
      this.$emit("update:comments", res.data.results || res.data);
      this.nextUrl = res.data.next || null;
    },
    async loadMore() {
      if (!this.nextUrl) return;
      const res = await axios.get(this.nextUrl);
      this.$emit("update:comments", [...(this.comments || []), ...(res.data.results || res.data)]);
      this.nextUrl = res.data.next || null;
    },
  },
};
</script>