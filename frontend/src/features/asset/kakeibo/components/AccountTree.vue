<script setup lang="ts">
    import type { AccountNode } from "../types"

    defineProps<{
    nodes: AccountNode[]
    }>()

    const formatMoney = (value: number) =>
    new Intl.NumberFormat("ja-JP", {
        style: "currency",
        currency: "JPY",
        maximumFractionDigits: 0,
    }).format(value)
</script>

<template>
  <div class="account-list">
    <details
      v-for="node in nodes"
      :key="node.id"
      class="account-item"
      :open="false"
    >
      <summary class="account-row">
        <span class="account-name">
          {{ node.name }}
          <span v-if="node.children.length" class="child-count">
            {{ node.children.length }}
          </span>
        </span>

        <span class="account-amount">
          {{ formatMoney(node.total_quantity) }}
        </span>
      </summary>

      <AccountTree
        v-if="node.children.length"
        :nodes="node.children"
        class="nested-tree"
      />

      <div
        v-if="!node.children.length"
        class="leaf-spacer"
      />
    </details>
  </div>
</template>

<style scoped>
    .account-list {
    display: flex;
    flex-direction: column;
    }

    .account-item {
    border-bottom: 1px solid var(--border-color, #e5e7eb);
    }

    .account-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 13px 14px;
    cursor: pointer;
    list-style: none;
    }

    .account-row::-webkit-details-marker {
    display: none;
    }

    .account-row::before {
    content: "›";
    color: #888;
    font-size: 20px;
    transition: transform 0.15s;
    }

    .account-item[open] > .account-row::before {
    transform: rotate(90deg);
    }

    .account-name {
    flex: 1;
    min-width: 0;
    overflow-wrap: anywhere;
    }

    .account-amount {
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
    text-align: right;
    font-weight: 600;
    }

    .child-count {
    margin-left: 6px;
    color: #888;
    font-size: 0.8rem;
    }

    .nested-tree {
    padding-left: 18px;
    background: var(--nested-background, #f8fafc);
    }

    .leaf-spacer {
    display: none;
    }
</style>
