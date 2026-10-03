<script setup lang="ts">
import { onMounted } from "vue"
import { start } from "./stato"

// all'avvio carico i posti e mi collego al broker MQTT
onMounted(() => {
  start()
})
</script>

<template>
  <div class="layout">
    <aside>
      <h1>S_PARK</h1>
      <nav>
        <ul>
          <li><router-link to="/">Dashboard</router-link></li>
          <li><router-link to="/spots">Posti auto</router-link></li>
        </ul>
      </nav>
    </aside>

    <div class="content">
      <main>
        <router-view />
      </main>
      <footer>
        <p> IoT e Sistemi Embedded - A.A. 2026/2027</p>
      </footer>
    </div>
  </div>
</template>

<style scoped>
  .layout {
    display: flex;
    min-height: 100vh;
  }

  aside {
    width: 190px;
    background-color: #0f172a;
    color: white;
    padding: 16px;
  }

  aside h1 {
    font-size: 20px;
    margin: 0 0 24px 0;
  }

  ul {
    list-style: none;
    margin: 0;
    padding: 0;
  }

  li {
    margin-bottom: 6px;
  }

  a {
    display: block;
    padding: 10px 12px;
    border-radius: 6px;
    color: #cbd5e1;
    text-decoration: none;
    font-size: 14px;
  }

  .router-link-exact-active {
    color: white;
    background-color: #1e293b;
  }

  .content {
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  main {
    flex: 1;
    padding: 24px;
  }

  footer {
    text-align: center;
    font-size: 12px;
    color: #64748b;
  }
</style>