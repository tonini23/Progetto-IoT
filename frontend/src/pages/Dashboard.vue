<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue"
import { spots, statusOf } from "../stato"
import SpotCard from "../components/SpotCard.vue"

// ---- orologio in alto a destra ----
const now = ref<Date>(new Date())
let timer = 0

onMounted(() => {
  timer = window.setInterval(() => { now.value = new Date() }, 1000)
})
onUnmounted(() => {
  clearInterval(timer)
})

// data e ora, es. "03/10/2026 - 14:32"
const dataOra = computed(() => {
  const data = now.value.toLocaleDateString("it-IT", { day: "2-digit", month: "2-digit", year: "numeric" })
  const ora = now.value.toLocaleTimeString("it-IT", { hour: "2-digit", minute: "2-digit" })
  return data + " - " + ora
})

// ---- posti divisi per fila ----
const rowA = computed(() => spots.value.filter(s => s.row === "A"))
const rowB = computed(() => spots.value.filter(s => s.row === "B"))

// ---- numeri delle card ----
const total = computed(() => spots.value.length)
const free = computed(() => spots.value.filter(s => statusOf(s.id) === "free").length)
const busy = computed(() => spots.value.filter(s => statusOf(s.id) === "busy").length)
const unknown = computed(() => spots.value.filter(s => statusOf(s.id) === "unknown").length)

const disabledSpots = computed(() => spots.value.filter(s => s.disabled))
const disabledFree = computed(() => disabledSpots.value.filter(s => statusOf(s.id) === "free").length)

function percent(n: number): number {
  if (total.value === 0) return 0
  return Math.round(n / total.value * 100)
}

// ciambella: gradiente conico rosso (occupati), verde (liberi), grigio (senza dati) 
const donutStyle = computed(() => {
  const b = percent(busy.value)
  const f = Math.min(100, b + percent(free.value))
  return {
    background: `conic-gradient(#ef4444 0 ${b}%, #10b981 ${b}% ${f}%, #cbd5e1 ${f}% 100%)`
  }
})
</script>

<template>
  <div class="top">
    <h2>DASHBOARD PARCHEGGIO INTELLIGENTE</h2>
    <div class="chip">
      {{ dataOra }}
    </div>
  </div>

  <!-- le 4 card con i numeri -->
  <div class="stats">
    <div class="card">
      <p class="label">CAPACITÀ TOTALE <span class="dot blue"></span></p>
      <p class="number">{{ total }}</p>
      <p class="sub">posti con un sensore</p>
    </div>
    <div class="card">
      <p class="label">POSTI LIBERI <span class="dot green"></span></p>
      <p class="number">{{ free }}</p>
      <p class="sub">{{ percent(free) }}% della capacità</p>
    </div>
    <div class="card">
      <p class="label">POSTI OCCUPATI <span class="dot red"></span></p>
      <p class="number">{{ busy }}</p>
      <p class="sub">{{ percent(busy) }}% della capacità</p>
    </div>
    <div class="card">
      <p class="label">POSTI PER DISABILI <span class="dot amber"></span></p>
      <p class="number">{{ disabledSpots.length }}</p>
      <p class="sub">{{ disabledFree }} liberi</p>
    </div>
  </div>

  <div class="panels">
    <!-- mappa del parcheggio -->
    <div class="card">
      <p class="legend">
        <span class="dot green"></span> Libero &nbsp;
        <span class="dot red"></span> Occupato
      </p>

      <div class="map">
        <div class="row">
          <SpotCard v-for="s in rowA" :key="s.id" :id="s.id" :status="statusOf(s.id)" :disabled="s.disabled" />
        </div>

        <p class="lane">&larr; INGRESSO - - - - - - - - - - - - USCITA &rarr;</p>

        <div class="row">
          <SpotCard v-for="s in rowB" :key="s.id" :id="s.id" :status="statusOf(s.id)" :disabled="s.disabled" />
        </div>
      </div>
    </div>

    <!-- ciambella con la percentuale -->
    <div class="card">
      <h3>TASSO DI OCCUPAZIONE</h3>
      <div class="donut" :style="donutStyle">
        <div class="donut-text">
          <p class="percent">{{ percent(busy) }}%</p>
          <p class="sub">OCCUPATO</p>
        </div>
      </div>
      <p class="line"><span class="dot green"></span> Posti liberi <b>{{ free }}</b></p>
      <p class="line"><span class="dot red"></span> Posti occupati <b>{{ busy }}</b></p>
      <p class="line"><span class="dot grey"></span> Non disponibili <b>{{ unknown }}</b></p>
    </div>
  </div>
</template>

<style scoped>
  .top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
  }

  h2 {
    margin: 0;
    font-size: 20px;
  }

  .chip {
    background-color: white;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 12px;
  }

  .stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 24px;
  }

  .label {
    margin: 0;
    font-size: 10px;
    color: #64748b;
    display: flex;
    justify-content: space-between;
  }

  .number {
    margin: 6px 0 2px 0;
    font-size: 28px;
    font-weight: bold;
  }

  .sub {
    margin: 0;
    font-size: 10px;
    color: #64748b;
  }

  .panels {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 16px;
    align-items: start;
  }

  .legend {
    margin: 0 0 12px 0;
    font-size: 12px;
  }

  .map {
    background-color: #f6f8fc;
    border-radius: 8px;
    padding: 12px;
  }

  .row {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    gap: 8px;
  }

  .lane {
    text-align: center;
    font-size: 10px;
    color: #94a3b8;
    margin: 16px 0;
  }

  h3 {
    margin: 0 0 16px 0;
    font-size: 13px;
  }

  .donut {
    position: relative;
    width: 150px;
    height: 150px;
    margin: 0 auto 16px auto;
    border-radius: 50%;
  }

  /* cerchio bianco al centro per fare il buco della ciambella */
  .donut::before {
    content: "";
    position: absolute;
    top: 22px;
    left: 22px;
    right: 22px;
    bottom: 22px;
    background-color: white;
    border-radius: 50%;
  }

  .donut-text {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .percent {
    margin: 0;
    font-size: 26px;
    font-weight: bold;
  }

  .line {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 8px 0;
    font-size: 12px;
  }

  .line b {
    margin-left: auto;
  }

  /* su schermi piccoli metto tutto in colonna */
  @media (max-width: 900px) {
    .stats { grid-template-columns: repeat(2, 1fr); }
    .panels { grid-template-columns: 1fr; }
    .row { grid-template-columns: repeat(4, 1fr); }
  }
</style>