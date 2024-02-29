<template>
  <div class="h-100 d-flex align-center justify-space-between">
    <!-- 👉 Footer: left content -->
    <span class="d-flex align-center">
      <router-link to="/legal">
        <a class="text-primary ms-1">Legal notice </a>
      </router-link>
      - All rights reserved &copy; 2023      
      <a
        href="https://www.irt-systemx.fr/"
        target="_blank"
        rel="noopener noreferrer"
        class="text-primary ms-1"
      >IRT SystemX</a>
<!--
      &copy;
      {{ new Date().getFullYear() }}
      Made With
      <VIcon
        icon="mdi-heart-outline"
        color="error"
        size="1.25rem"
        class="mx-1"
      />
      By <a
        href="https://www.irt-systemx.fr/"
        target="_blank"
        rel="noopener noreferrer"
        class="text-primary ms-1"
      >IRT SystemX</a>
-->
    </span>
    <!-- 👉 Footer: right content -->
    <span class="d-md-flex gap-x-4 text-primary d-none">
    <!--
      <router-link to="/about">
        <a>About</a>
      </router-link>
      <a
        href="https://themeselection.com/license/"
        target="noopener noreferrer"
      >License</a>
      <a
        href="https://themeselection.com/"
        target="noopener noreferrer"
      >More Themes</a>
      <a
        href="https://demos.themeselection.com/materio-vuetify-vuejs-admin-template/documentation/"
        target="noopener noreferrer"
      >Documentation</a>
    -->
    </span>
  </div>
</template>
