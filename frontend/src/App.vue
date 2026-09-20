<template>
  <header>
    <h1> Smart parking </h1>
  </header>
  <nav>
    <ul>
      <li><router-link to="/">prova</router-link></li>
      <li><router-link to="/">prova</router-link></li>
      <li><router-link to="/">prova</router-link></li>
      <li><router-link to="/">prova</router-link></li>
    </ul>
  </nav>
  <main>
    <router-view />
  </main>
  <footer>
    <p> IoT e Sistemi Embedded - A.A. 2026/2027</p>
  </footer>
</template>

<style scoped>
  .router-link-exact-active {
    color: rgb(219, 69, 83);
    background-color: rgb(255, 255, 255);
  }
</style>
