<script setup lang="ts">
// Un singolo posto auto: riceve id, stato (free/busy/unknown) e se e' per disabili
defineProps<{
  id: string
  status: string
  disabled: boolean
}>()
</script>

<template>
  <div class="spot" :class="status">
    <span class="id">{{ id }}</span>
    <span class="icon">{{ disabled ? "DISAB." : "AUTO" }}</span>
    <span class="badge">{{ status === "free" ? "LIBERO" : status === "busy" ? "OCCUPATO" : "N/D" }}</span>
  </div>
</template>

<style scoped>
  .spot {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    padding: 8px 2px;
    border: 2px solid;
    border-radius: 6px;
    font-size: 11px;
    font-weight: bold;
  }

  .icon {
    font-size: 10px;
  }

  .badge {
    color: white;
    font-size: 9px;
    padding: 1px 6px;
    border-radius: 3px;
  }

  .free { color: #10b981; border-color: #10b981; background-color: #ecfdf5; }
  .free .badge { background-color: #10b981; }

  .busy { color: #ef4444; border-color: #ef4444; background-color: #fef2f2; }
  .busy .badge { background-color: #ef4444; }

  .unknown { color: #94a3b8; border-color: #cbd5e1; background-color: #f8fafc; }
  .unknown .badge { background-color: #94a3b8; }
</style>