<script setup lang="ts">
const groups = [
  {
    title: '書籍',
    items: [
      { to: '/book', title: 'Book', icon: 'mdi-book-open-variant' },
      { to: '/work', title: 'Work', icon: 'mdi-bookshelf' },
      { to: '/publisher', title: 'Publisher', icon: 'mdi-office-building' },
      { to: '/author', title: 'Author', icon: 'mdi-account-edit' },
    ],
  },
  {
    title: '公共料金',
    items: [
      { to: '/bill/electric', title: 'Electric Bill', icon: 'mdi-flash' },
      { to: '/bill/gas', title: 'Gas Bill', icon: 'mdi-fire' },
      { to: '/bill/water', title: 'Water Bill', icon: 'mdi-water' },
    ],
  },
  {
    title: '収入',
    items: [
      { to: '/payslip', title: 'Payslip', icon: 'mdi-cash-multiple' },
      { to: '/subsidy', title: 'Subsidy', icon: 'mdi-hand-coin' },
      { to: '/subsidy/tax', title: 'Tax', icon: 'mdi-calculator' },
    ],
  },
  {
    title: '資産',
    items: [
      { to: '/asset', title: 'Asset', icon: 'mdi-safe-square-outline' },
      { to: '/account', title: '勘定項目一覧', icon: 'mdi-format-list-bulleted' },
      { to: '/holding', title: '銘柄一覧', icon: 'mdi-chart-line' },
      { to: '/transaction', title: '取引一覧', icon: 'mdi-swap-horizontal' },
      { to: '/asset/kakeibo', title: '家計簿', icon: 'mdi-notebook' },
    ],
  },
  {
    title: '健康',
    items: [
      { to: '/daily', title: 'Daily Log', icon: 'mdi-chart-timeline-variant' },
      { to: '/health', title: '健康診断', icon: 'mdi-clipboard-pulse-outline' },
    ],
  },
]
</script>

<template>
  <v-app>
    <v-navigation-drawer>
      <v-list nav density="compact">
        <v-list-item to="/" exact title="Home" prepend-icon="mdi-home" />

        <template v-for="group in groups" :key="group.title">
          <v-divider class="my-2" />
          <v-list-subheader>{{ group.title }}</v-list-subheader>
          <v-list-item
            v-for="item in group.items"
            :key="item.to"
            :to="item.to"
            :title="item.title"
            :prepend-icon="item.icon"
            exact
          />
        </template>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container>
        <RouterView />
      </v-container>
    </v-main>
  </v-app>
</template>

<style scoped></style>
