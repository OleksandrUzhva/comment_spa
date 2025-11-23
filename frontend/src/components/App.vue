<template>
  <div id="app">
    <h1>Comments SPA</h1>
    <CommentForm @submitted="onSubmitted" />
    <CommentsTable :comments="comments" @load-more="loadMore" />
  </div>
</template>

<script>
import axios from "axios";
import CommentForm from "./components/CommentForm.vue";
import CommentsTable from "./components/CommentsTable.vue";

export default {
  components: { CommentForm, CommentsTable },
  data() {
    return {
      comments: [],
      ws: null,
      nextUrl: null
    };
  },
  mounted() {
    this.fetchComments();
    this.initWebSocket();
  },
  methods: {
    async fetchComments() {
      try {
        const res = await axios.get("/api/comments/");
        this.comments = res.data.results || res.data;
        this.nextUrl = res.data.next || null;
      } catch (e) {
        console.error("Fetch comments error", e);
      }
    },
    async loadMore() {
      if (!this.nextUrl) return;
      const res = await axios.get(this.nextUrl);
      const more = res.data.results || res.data;
      this.comments.push(...more);
      this.nextUrl = res.data.next || null;
    },
    onSubmitted() {
      // optional: re-fetch page 1
      this.fetchComments();
    },
    initWebSocket() {
      const protocol = window.location.protocol === "https:" ? "wss" : "ws";
      const host = window.location.hostname;
      const port = window.location.port ? `:${window.location.port}` : "";
      const url = `${protocol}://${host}${port}/ws/comments/`;
      const ws = new WebSocket(url);
      ws.onopen = () => console.log("WS connected");
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          // insert on top (LIFO)
          this.comments.unshift(data);
        } catch (err) {
          console.error("WS parse error", err);
        }
      };
      ws.onclose = () => {
        console.log("WS closed, reconnecting in 1s");
        setTimeout(this.initWebSocket, 1000);
      };
      ws.onerror = (err) => console.error("WS error", err);
      this.ws = ws;
    },
  },
};
</script>