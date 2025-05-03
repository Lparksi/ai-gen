<template>
  <div id="app">
    <router-view />
  </div>
</template>

<style>
#app {
  font-family: 'PingFang SC', 'Helvetica Neue', Arial, sans-serif;
  text-align: center;
  color: #333;
  margin-top: 0;
  padding: 0;
  background-color: #f8f8f8;
  min-height: 100vh;
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
</style>

@media (max-width: 480px) {
  h1 {
    font-size: 1.5rem;
  }
  h2 {
    font-size: 1.2rem;
  }
  p {
    line-height: 1.4;
    margin-bottom: 0.8em;
  }
}
