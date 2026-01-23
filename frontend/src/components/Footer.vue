<template>
    <footer class="site-footer">
      <div class="footer-content">
        <p>&copy; 2025 Kumajala | <span class="text-gradient">Prototype v0.1</span></p>
        <p class="credits">Développé par VFC Crew</p>
        <ul class="social-links">
          <li>
            <a href="https://github.com/Frejuste26" target="_blank" class="hover-neon">Kei Prince Frejuste</a>
          </li>
          <li>
            <a href="https://github.com/EbroVital" target="_blank" class="hover-neon">Nango Ebrottié Vital</a>
          </li>
          <li>
            <a href="https://github.com/sannetia" target="_blank" class="hover-neon">Sanné-Tia Chrys</a>
          </li>
        </ul>
      </div>
    </footer>
</template>

<style scoped>
.site-footer {
  padding: var(--space-8) var(--space-4);
  background-color: var(--cl-bg-dark);
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  text-align: center;
  color: var(--cl-gray-500);
  font-size: var(--fs-sm);
  position: relative;
  z-index: 10;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-4);
}

.text-gradient {
  background: linear-gradient(90deg, var(--cl-primary), var(--cl-secondary));
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: bold;
}

.social-links {
  list-style: none;
  padding: 0;
  display: flex;
  justify-content: center;
  gap: var(--space-6);
  flex-wrap: wrap;
}

.social-links a {
  color: var(--cl-gray-400);
  text-decoration: none;
  transition: all 0.3s ease;
  position: relative;
}

.hover-neon:hover {
  color: var(--cl-primary);
  text-shadow: 0 0 8px rgba(0, 240, 255, 0.5);
}

@media (min-width: 768px) {
  .footer-content {
    flex-direction: row;
    justify-content: space-between;
  }
}
</style>
