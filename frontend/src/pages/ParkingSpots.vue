<script setup lang="ts">
import { spots, states, statusOf } from "../stato"

// trasforma lo stato in un testo leggibile
function testoStato(id: string): string {
  const s = statusOf(id)
  if (s === "free") return "Libero"
  if (s === "busy") return "Occupato"
  return "Nessun dato"
}

function distanza(id: string): string {
  const s = states[id]
  if (!s || s.distance === null || s.distance === undefined) return "-"
  return s.distance + " cm"
}

function ultimoAggiornamento(id: string): string {
  const s = states[id]
  if (!s) return "-"
  return new Date(s.time).toLocaleTimeString("it-IT")
}
</script>

<template>
  <h2>POSTI AUTO</h2>

  <div class="card">
    <table>
      <thead>
        <tr>
          <th>Posto</th>
          <th>Tipo</th>
          <th>Stato</th>
          <th>Distanza</th>
          <th>Ultimo aggiornamento</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="s in spots" :key="s.id">
          <td><b>{{ s.id }}</b></td>
          <td>{{ s.disabled ? "Disabili" : "Standard" }}</td>
          <td :class="statusOf(s.id)">{{ testoStato(s.id) }}</td>
          <td>{{ distanza(s.id) }}</td>
          <td>{{ ultimoAggiornamento(s.id) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
  h2 {
    margin: 0 0 24px 0;
    font-size: 20px;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }

  th, td {
    text-align: left;
    padding: 10px 8px;
    border-bottom: 1px solid #e2e8f0;
  }

  .free { color: #059669; font-weight: bold; }
  .busy { color: #dc2626; font-weight: bold; }
  .unknown { color: #64748b; }
</style>