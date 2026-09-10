<script setup lang="ts"></script>

<template>
  <v-app>
    <v-app-bar>
      <v-app-bar-title>Application Bar</v-app-bar-title>
    </v-app-bar>

    <v-navigation-drawer>
      <v-list>
        <v-list-item to="/" title="Home" />
        <v-list-item to="/book" title="Book" />
        <v-list-item to="/work" title="Work" />
        <v-list-item to="/publisher" title="Pubilsher" />
        <v-list-item to="/author" title="Author" />
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
