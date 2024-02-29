<script setup>
import { useTheme } from 'vuetify'
import VerticalNavLayout from '@layouts/components/VerticalNavLayout.vue'
import VerticalNavLink from '@layouts/components/VerticalNavLink.vue'
import VerticalNavSectionTitle from '@/@layouts/components/VerticalNavSectionTitle.vue'

// Components
import Footer from '@/layouts/components/Footer.vue'
import NavbarThemeSwitcher from '@/layouts/components/NavbarThemeSwitcher.vue'
import UserProfile from '@/layouts/components/UserProfile.vue'

const vuetifyTheme = useTheme()
</script>

<template>
  <VerticalNavLayout>
    <!-- 👉 navbar -->
    <template #navbar="{ toggleVerticalOverlayNavActive }">
      <div class="d-flex h-100 align-center">
        <!-- 👉 Vertical nav toggle in overlay mode -->

        <IconBtn
          class="ms-n3 d-lg-none"
          @click="toggleVerticalOverlayNavActive(true)"
        >
          <VIcon icon="mdi-menu" />
        </IconBtn>

        <!-- 👉 Search 
        <div
          class="d-flex align-center cursor-pointer"
          style="user-select: none;"
        >          
          <IconBtn>
            <VIcon icon="mdi-magnify" />
          </IconBtn>

          <span class="d-none d-md-flex align-center text-disabled">
            <span class="me-3">Search</span>
            <span class="meta-key">&#8984;K</span>
          </span>
        </div>
        -->

        <VSpacer />

        <IconBtn
          class="me-2"
          href="https://github.com/IRT-SystemX/faireexplo"
          target="_blank"
          rel="noopener noreferrer"
        >
          <VIcon icon="mdi-github" />
        </IconBtn>

        <RouterLink to="/about">
          <IconBtn class="me-2">
            <VIcon icon="mdi-help-circle-outline" />
          </IconBtn>
        </RouterLink>

        <!--
        <NavbarThemeSwitcher class="me-2" />
        <IconBtn class="me-2">
          <VIcon icon="mdi-bell-outline" />
        </IconBtn>
        <UserProfile />
        -->
      </div>
    </template>

    <template #vertical-nav-content>
      <VerticalNavSectionTitle
        :item="{
          heading: '',
        }"
      />

      <VerticalNavLink
        :item="{
          title: 'Benchmark',
          icon: 'mdi-chart-bar',
          to: '/benchmark',
        }"
      />

      <!--
      <VerticalNavLink
        :item="{
          title: 'Workspace',
          icon: 'mdi-home',
          to: '/dashboard',
        }"
      />
      
      <VerticalNavLink
        :item="{
          title: 'Reports',
          icon: 'mdi-chart-line',
          to: '/account-settings',
        }"
      />
      -->
    
    </template>
    
    <!--
    <template #after-vertical-nav-items> 
       <VerticalNavLink
        :item="{
          title: 'About',
          icon: 'mdi-information-outline',
          to: '/about',
        }"
      />
    </template>
    -->

    <!-- 👉 Pages -->
    <slot />

    <!-- 👉 Footer -->
    <template #footer>
      <Footer />
    </template>
  </VerticalNavLayout>
</template>

<style lang="scss" scoped>
.meta-key {
  border: thin solid rgba(var(--v-border-color), var(--v-border-opacity));
  border-radius: 6px;
  block-size: 1.5625rem;
  line-height: 1.3125rem;
  padding-block: 0.125rem;
  padding-inline: 0.25rem;
}
</style>
