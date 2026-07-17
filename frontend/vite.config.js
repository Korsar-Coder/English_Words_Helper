import { defineConfig } from "vite";
import { resolve } from "path";

export default defineConfig({
  server: {
    open: "/auth.html",
  },
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, "auth.html"),
        homepage: resolve(__dirname, "homepage.html"),
      },
    },
  },
});
