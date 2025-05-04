<template>
  <div id="app" :class="currentTheme">
    <router-view />
  </div>
</template>

<script>
import { provide } from 'vue'
export default {
  data() {
    return {
      currentTheme: localStorage.getItem('theme') || 'light-theme',
    };
  },
  methods: {
    toggleTheme() {
      this.currentTheme = this.currentTheme === 'light-theme' ? 'dark-theme' : 'light-theme';
      localStorage.setItem('theme', this.currentTheme);
      document.body.className = this.currentTheme === 'dark-theme' ? 'dark-mode' : '';
    },
  },
  mounted() {
    // 初始化时同步body的class
    if (this.currentTheme === 'dark-theme') {
      document.body.className = 'dark-mode';
    } else {
      document.body.className = '';
    }
  },
  provide() {
    return {
      toggleTheme: this.toggleTheme,
      currentTheme: this.currentTheme
    }
  }
};
</script>

<style>
#app {
  font-family: 'PingFang SC', 'Helvetica Neue', Arial, sans-serif;
  text-align: center;
  margin-top: 0;
  padding: 0;
  min-height: 100vh;
  transition: background-color 0.3s, color 0.3s;
}

.light-theme {
  color: #333;
  background-color: #f8f8f8;
}

.dark-theme {
  color: #f0f0f0;
  background-color: #1a1a1a;
}

@media (max-width: 768px) {
  #app {
    padding: 0;
  }
}

@media (max-width: 480px) {
  #app {
    font-size: 15px;
  }
}

/* 删除.theme-toggle-button相关样式 */
</style>
