<script setup>
import { RouterLink, useRouter, useRoute } from 'vue-router'
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { Home as HomeIcon, Info as InfoIcon, Search as SearchIcon, Sun as SunIcon, Moon as MoonIcon, ArrowRight as ArrowRightIcon, Settings as SettingsIcon } from 'lucide-vue-next'; 
import logoImage from '@/assets/kumajala.jpg'
  
const props = defineProps({
  logoSrc: { type: String, default: logoImage },
  logoAlt: { type: String, default: 'Logo kumajala' },
  logoHeight: { type: String, default: '40px' },
  navItems: {
    type: Array,
    default: () => [
      { name: 'Accueil', path: '/', icon: HomeIcon },
      { name: 'À Propos', path: '/about', icon: InfoIcon },
      { name: 'Traducteur', path: '/translator', icon: null },
      { name: 'Contact', path: '/contact', icon: null },
      { name: 'Paramètres', path: '/settings', icon: SettingsIcon },
    ]
  },
  showActions: { type: Boolean, default: true },
  variant: { type: String, default: 'blur' },
  position: { type: String, default: 'sticky' },
  mobileBreakpoint: { type: Number, default: 768 },
  hideOnScroll: { type: Boolean, default: false },
  shrinkOnScroll: { type: Boolean, default: true }
})

const emit = defineEmits(['logo-click', 'nav-item-click', 'mobile-menu-toggle'])
const router = useRouter()
const route = useRoute()

const isMobileMenuOpen = ref(false)
const isScrolled = ref(false)
const isHidden = ref(false)
const isMobile = ref(false)
const lastScrollY = ref(0)

const headerClasses = computed(() => [
  'enhanced-header',
  `variant-${props.variant}`,
  `position-${props.position}`,
  {
    'is-scrolled': isScrolled.value,
    'is-hidden': isHidden.value && props.hideOnScroll,
    'is-shrunk': isScrolled.value && props.shrinkOnScroll,
    'mobile-menu-open': isMobileMenuOpen.value
  }
])

const logoClasses = computed(() => [
  'header-logo',
  { 'is-shrunk': isScrolled.value && props.shrinkOnScroll }
])

const handleScroll = () => {
  const currentScrollY = window.scrollY
  isScrolled.value = currentScrollY > 20
  if (props.hideOnScroll) {
    isHidden.value = currentScrollY > lastScrollY.value && currentScrollY > 100
  }
  lastScrollY.value = currentScrollY
}

const handleResize = () => {
  isMobile.value = window.innerWidth < props.mobileBreakpoint
  if (!isMobile.value && isMobileMenuOpen.value) {
    isMobileMenuOpen.value = false
  }
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
  emit('mobile-menu-toggle', isMobileMenuOpen.value)
  document.body.style.overflow = isMobileMenuOpen.value ? 'hidden' : ''
}

const handleLogoClick = () => {
  emit('logo-click')
  router.push('/')
}

const handleNavItemClick = (item) => {
  emit('nav-item-click', item)
  if (isMobileMenuOpen.value) {
    toggleMobileMenu()
  }
}

const isActiveRoute = (path) => {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('resize', handleResize, { passive: true })
  handleResize()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('resize', handleResize)
  document.body.style.overflow = ''
})

watch(() => route.path, () => {
  if (isMobileMenuOpen.value) toggleMobileMenu()
})
</script>

<template>
  <header :class="headerClasses">
    <div class="header-container">
      <!-- Logo -->
      <div class="header-brand">
        <button class="logo-button" @click="handleLogoClick">
          <img :src="logoSrc" :alt="logoAlt" :class="logoClasses" :style="{ height: logoHeight }" loading="lazy" />
          <span class="beta-badge">v0.1</span>
        </button>
      </div>

      <!-- Navigation Desktop -->
      <nav class="desktop-nav">
        <ul class="nav-list">
          <li v-for="item in navItems" :key="item.path" class="nav-item">
            <RouterLink
              :to="item.path"
              class="nav-link"
              :class="{ 'is-active': isActiveRoute(item.path) }"
              @click="handleNavItemClick(item)"
            >
              <component :is="item.icon" v-if="item.icon" class="nav-icon" />
              <span>{{ item.name }}</span>
              <span v-if="isActiveRoute(item.path)" class="active-indicator"></span>
            </RouterLink>
          </li>
        </ul>
      </nav>

      <!-- Actions -->
      <div v-if="showActions" class="header-actions">
        <slot name="actions">
          <RouterLink to="/translator" class="cta-button glow-effect">
            <span>Lancer l'App</span>
            <ArrowRightIcon width="16" height="16" />
          </RouterLink>
        </slot>
      </div>

      <!-- Bouton menu mobile -->
      <button class="mobile-menu-button" @click="toggleMobileMenu">
        <span class="hamburger-line" :class="{ 'is-open': isMobileMenuOpen }"></span>
        <span class="hamburger-line" :class="{ 'is-open': isMobileMenuOpen }"></span>
        <span class="hamburger-line" :class="{ 'is-open': isMobileMenuOpen }"></span>
      </button>
    </div>

    <!-- Menu Mobile -->
    <Transition name="mobile-menu">
      <div v-show="isMobileMenuOpen" class="mobile-menu">
        <div class="mobile-menu-backdrop" @click="toggleMobileMenu"></div>
        <nav class="mobile-nav">
          <ul class="mobile-nav-list">
            <li v-for="(item, index) in navItems" :key="item.path" class="mobile-nav-item" :style="{ animationDelay: `${index * 0.1}s` }">
              <RouterLink
                :to="item.path"
                class="mobile-nav-link"
                :class="{ 'is-active': isActiveRoute(item.path) }"
                @click="handleNavItemClick(item)"
              >
                <component :is="item.icon" v-if="item.icon" class="mobile-nav-icon" />
                <span>{{ item.name }}</span>
              </RouterLink>
            </li>
          </ul>
        </nav>
      </div>
    </Transition>
  </header>
</template>

<style scoped>
.enhanced-header {
  position: relative;
  width: 100%;
  z-index: 1000;
  transition: all var(--transition-base);
  font-family: var(--font-primary);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.position-sticky { position: sticky; top: 0; }
.position-fixed { position: fixed; top: 0; left: 0; right: 0; }

.header-container {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-6);
  transition: all var(--transition-base);
}

/* VARIANT BLUR (GLASSMORPHISM) */
.variant-blur {
  background-color: rgba(5, 5, 16, 0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.is-scrolled.variant-blur {
  background-color: rgba(5, 5, 16, 0.9);
  border-bottom: 1px solid var(--cl-primary);
  box-shadow: 0 4px 20px rgba(0, 240, 255, 0.1);
}

.logo-button {
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-logo {
  border-radius: 50%;
  border: 2px solid var(--cl-primary);
}

.beta-badge {
  background: rgba(0, 240, 255, 0.1);
  color: var(--cl-primary);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.7rem;
  border: 1px solid var(--cl-primary);
  font-family: var(--font-display);
}

/* NAVIGATION */
.desktop-nav { display: flex; align-items: center; }
.nav-list { display: flex; gap: var(--space-6); list-style: none; margin: 0; padding: 0; }

.nav-link {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  color: var(--cl-gray-400);
  text-decoration: none;
  font-weight: var(--fw-medium);
  transition: all 0.3s ease;
  position: relative;
  padding: 0.5rem 1rem;
}

.nav-link:hover, .nav-link.is-active {
  color: var(--cl-white);
  text-shadow: 0 0 8px rgba(255, 255, 255, 0.5);
}

.active-indicator {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 2px;
  background-color: var(--cl-primary);
  box-shadow: 0 0 10px var(--cl-primary);
}

/* CTA BUTTON */
.cta-button {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: 0.6rem 1.2rem;
  background: transparent;
  border: 1px solid var(--cl-primary);
  color: var(--cl-primary);
  border-radius: 4px;
  text-decoration: none;
  font-weight: var(--fw-bold);
  transition: all 0.3s ease;
  text-transform: uppercase;
  font-family: var(--font-display);
  letter-spacing: 1px;
}

.cta-button:hover {
  background: var(--cl-primary);
  color: var(--cl-bg-dark);
  box-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
}

/* MOBILE MENU */
.mobile-menu-button {
  display: none;
  flex-direction: column;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: none;
  border: 1px solid var(--cl-gray-700);
  border-radius: 4px;
  padding: 8px;
  cursor: pointer;
}

.hamburger-line {
  display: block;
  width: 100%;
  height: 2px;
  background-color: var(--cl-white);
  margin-bottom: 5px;
  transition: all 0.3s;
}

.mobile-menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  z-index: 999;
}

.mobile-menu-backdrop {
  position: absolute;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
}

.mobile-nav {
  position: absolute;
  right: 0;
  width: 300px;
  height: 100%;
  background: var(--cl-bg-panel);
  border-left: 1px solid var(--cl-gray-700);
  padding: 2rem;
}

.mobile-nav-link {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: var(--cl-gray-400);
  text-decoration: none;
  font-size: 1.2rem;
  padding: 1rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.mobile-nav-link.is-active {
  color: var(--cl-primary);
}

@media (max-width: 768px) {
  .desktop-nav, .header-actions { display: none; }
  .mobile-menu-button { display: flex; }
}
</style>
