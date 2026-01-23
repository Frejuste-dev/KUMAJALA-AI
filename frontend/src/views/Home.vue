<script setup>
import { useRouter } from 'vue-router'; 
import TopBar from '@/components/topBar.vue'; 
import GetStartedButton from '@/components/getStartedButton.vue'; 
import AfricanPatterns from '@/components/AfricanPatterns.vue';
import { Home as HomeIcon, Info as InfoIcon, Languages as LanguagesIcon, Settings as SettingsIcon, Database, Cpu, Globe } from 'lucide-vue-next'; 
import Footer from '@/components/Footer.vue'; 

const router = useRouter();

const navigationItems = [
    { name: 'Accueil', path: '/', icon: HomeIcon }, 
    { name: 'À Propos', path: '/about', icon: InfoIcon },
    { name: 'Traducteur', path: '/translator', icon: LanguagesIcon },
    { name: 'Paramètres', path: '/settings', icon: SettingsIcon }
];

const handleLogoClick = () => {
    router.push('/'); 
};

const handleNavClick = (item) => {
    console.log('Nav item clicked:', item.name);
};

const handleGetStarted = () => {
    router.push('/translator'); 
};
</script>

<template>
  <div class="page-wrapper">
    <TopBar
      :nav-items="navigationItems"
      variant="blur"
      position="sticky"
      :shrink-on-scroll="true"
      @logo-click="handleLogoClick"
      @nav-item-click="handleNavClick"
    />

    <!-- SECTION HERO -->
    <section class="hero">
      <!-- African Patterns Background -->
      <AfricanPatterns type="africa-map" />
      <AfricanPatterns type="adinkra" />
      
      <div class="hero-bg-glow"></div>
      <div class="hero-content">
        <div class="prototype-badge">
          <span class="pulse-dot"></span>
          PROTOTYPE v0.1
        </div>
        <h1 class="hero-title">
          Le Futur de la <br>
          <span class="text-gradient text-glow">Traduction Africaine</span>
        </h1>
        <p class="hero-subtitle">
          Propulsé par <span class="highlight-tech">Gemini AI</span>. En route vers notre propre modèle souverain.
          <br>
          Traduisez instantanément : <strong>Bété, Baoulé, Mooré, Agni.</strong>
        </p>
        
        <div class="hero-actions">
          <GetStartedButton variant="primary" size="lg" @click="handleGetStarted" class="glow-button">
            Tester le Prototype
          </GetStartedButton>
          <button class="btn btn-outline btn-lg neon-border" @click="router.push('/about')">
            Contribuer au Dataset
          </button>
        </div>
      </div>

      <!-- 3D Element Placeholder (CSS Representation) -->
      <div class="hero-visual">
        <div class="orbit-system">
          <div class="core-sphere"></div>
          <div class="orbit orbit-1"></div>
          <div class="orbit orbit-2"></div>
          <div class="orbit orbit-3"></div>
          <div class="floating-icon icon-1"><Database /></div>
          <div class="floating-icon icon-2"><Cpu /></div>
          <div class="floating-icon icon-3"><Globe /></div>
        </div>
      </div>
    </section>

    <!-- SECTION ROADMAP / FEATURES -->
    <section class="roadmap-section">
      <h2 class="section-title text-center">Notre <span class="text-gradient">Trajectoire</span></h2>
      <div class="roadmap-grid">
        <div class="roadmap-card glass-panel active">
          <div class="step-number">01</div>
          <h3>Prototype (Actuel)</h3>
          <p>Validation du concept avec Gemini AI. Traduction et synthèse vocale fonctionnelles.</p>
        </div>
        <div class="roadmap-card glass-panel">
          <div class="step-number">02</div>
          <h3>Collecte de Données</h3>
          <p>Crowdsourcing massif de phrases et audios pour constituer le dataset Kumajala.</p>
        </div>
        <div class="roadmap-card glass-panel">
          <div class="step-number">03</div>
          <h3>Modèle Souverain</h3>
          <p>Entraînement de notre propre LLM spécialisé sur les langues africaines.</p>
        </div>
      </div>
    </section>

    <!-- SECTION CALL TO ACTION INVESTORS -->
    <section class="cta-section">
      <div class="cta-content glass-panel neon-border">
        <h2>Devenez Pionnier</h2>
        <p>Nous construisons l'infrastructure linguistique de demain. Rejoignez l'aventure en tant qu'investisseur ou contributeur technique.</p>
        <button class="btn btn-primary btn-lg glow-button" @click="router.push('/about')">
          Nous Contacter
        </button>
      </div>
    </section>

    <Footer />
  </div>
</template>

<style scoped>
.page-wrapper {
  background-color: var(--cl-bg-dark);
  min-height: 100vh;
  overflow-x: hidden;
}

/* --- HERO --- */
.hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 120px 5%;
  min-height: 90vh;
  position: relative;
  gap: 4rem;
}

.hero-bg-glow {
  position: absolute;
  top: -20%;
  left: -10%;
  width: 50%;
  height: 50%;
  background: radial-gradient(circle, rgba(0, 240, 255, 0.15) 0%, transparent 70%);
  filter: blur(80px);
  z-index: 0;
  pointer-events: none;
}

.hero-content {
  flex: 1;
  z-index: 1;
  max-width: 600px;
}

.prototype-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: rgba(0, 240, 255, 0.1);
  border: 1px solid var(--cl-primary);
  border-radius: 20px;
  color: var(--cl-primary);
  font-family: var(--font-display);
  font-size: 0.9rem;
  letter-spacing: 1px;
  margin-bottom: 2rem;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background-color: var(--cl-primary);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--cl-primary);
  animation: pulse 2s infinite;
}

.hero-title {
  font-size: 4rem;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  color: var(--cl-white);
}

.hero-subtitle {
  font-size: 1.25rem;
  color: var(--cl-gray-600);
  margin-bottom: 3rem;
  line-height: 1.6;
}

.highlight-tech {
  color: var(--cl-secondary);
  font-weight: bold;
}

.hero-actions {
  display: flex;
  gap: 1.5rem;
}

.glow-button {
  box-shadow: 0 0 20px rgba(0, 240, 255, 0.3);
  transition: all 0.3s ease;
}

.glow-button:hover {
  box-shadow: 0 0 30px rgba(0, 240, 255, 0.6);
  transform: translateY(-2px);
}

/* --- HERO VISUAL (3D ORBIT) --- */
.hero-visual {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  height: 500px;
}

.orbit-system {
  position: relative;
  width: 400px;
  height: 400px;
  transform-style: preserve-3d;
  animation: float 6s ease-in-out infinite;
}

.core-sphere {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100px;
  height: 100px;
  background: radial-gradient(circle at 30% 30%, var(--cl-primary), #000);
  border-radius: 50%;
  box-shadow: 0 0 50px var(--cl-primary);
  z-index: 10;
}

.orbit {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
}

.orbit-1 { width: 200px; height: 200px; animation: rotate 10s linear infinite; border-color: rgba(0, 240, 255, 0.3); }
.orbit-2 { width: 300px; height: 300px; animation: rotate 15s linear infinite reverse; border-color: rgba(112, 0, 255, 0.3); }
.orbit-3 { width: 400px; height: 400px; animation: rotate 20s linear infinite; }

.floating-icon {
  position: absolute;
  color: var(--cl-white);
  background: rgba(10, 10, 31, 0.8);
  padding: 10px;
  border-radius: 50%;
  border: 1px solid var(--cl-gray-700);
  backdrop-filter: blur(5px);
}

.icon-1 { top: 20%; left: 20%; animation: float 4s ease-in-out infinite 1s; color: var(--cl-primary); }
.icon-2 { bottom: 20%; right: 20%; animation: float 5s ease-in-out infinite 2s; color: var(--cl-secondary); }
.icon-3 { top: 10%; right: 30%; animation: float 6s ease-in-out infinite 0s; color: var(--cl-tertiary); }

/* --- ROADMAP --- */
.roadmap-section {
  padding: 100px 5%;
  background: linear-gradient(to bottom, var(--cl-bg-dark), #0a0a15);
}

.section-title {
  font-size: 3rem;
  margin-bottom: 4rem;
  color: var(--cl-white);
}

.roadmap-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.roadmap-card {
  padding: 2rem;
  border-radius: 16px;
  position: relative;
  transition: transform 0.3s ease;
}

.roadmap-card:hover {
  transform: translateY(-10px);
  border-color: var(--cl-primary);
}

.roadmap-card.active {
  border-color: var(--cl-primary);
  box-shadow: 0 0 20px rgba(0, 240, 255, 0.1);
}

.step-number {
  font-family: var(--font-display);
  font-size: 4rem;
  color: rgba(255, 255, 255, 0.05);
  position: absolute;
  top: 10px;
  right: 20px;
  font-weight: 900;
}

.roadmap-card h3 {
  color: var(--cl-primary);
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.roadmap-card p {
  color: var(--cl-gray-500);
}

/* --- CTA --- */
.cta-section {
  padding: 100px 5%;
  display: flex;
  justify-content: center;
}

.cta-content {
  text-align: center;
  padding: 4rem;
  border-radius: 24px;
  max-width: 800px;
  width: 100%;
  background: linear-gradient(135deg, rgba(10, 10, 31, 0.9), rgba(20, 20, 40, 0.9));
}

.cta-content h2 {
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
  color: var(--cl-white);
}

.cta-content p {
  font-size: 1.2rem;
  color: var(--cl-gray-500);
  margin-bottom: 2.5rem;
}

/* ANIMATIONS */
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(0, 240, 255, 0.7); }
  70% { box-shadow: 0 0 0 10px rgba(0, 240, 255, 0); }
  100% { box-shadow: 0 0 0 0 rgba(0, 240, 255, 0); }
}

@keyframes rotate {
  from { transform: translate(-50%, -50%) rotate(0deg); }
  to { transform: translate(-50%, -50%) rotate(360deg); }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

/* ===== RESPONSIVE DESIGN ===== */

/* Tablet (768px - 1023px) */
@media (min-width: 768px) and (max-width: 1023px) {
  .hero {
    padding: 100px 40px;
  }
  
  .hero-title {
    font-size: 3rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .orbit-system {
    transform: scale(0.85);
  }
  
  .roadmap-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Mobile (max-width: 767px) */
@media (max-width: 767px) {
  .hero {
    flex-direction: column;
    text-align: center;
    padding: 60px 20px;
    gap: 2rem;
  }
  
  .hero-content {
    max-width: 100%;
  }
  
  .hero-title {
    font-size: 2.25rem;
    line-height: 1.2;
  }
  
  .hero-subtitle {
    font-size: 1rem;
    margin-bottom: 2rem;
  }
  
  .hero-actions {
    flex-direction: column;
    gap: 1rem;
    width: 100%;
  }
  
  .hero-actions button,
  .hero-actions a {
    width: 100%;
    justify-content: center;
  }
  
  .hero-visual {
    height: 250px;
    width: 100%;
  }
  
  .orbit-system {
    transform: scale(0.6);
  }
  
  .orbit-icon {
    width: 30px;
    height: 30px;
  }
  
  /* Roadmap Section */
  .roadmap {
    padding: 60px 20px;
  }
  
  .roadmap h2 {
    font-size: 2rem;
  }
  
  .roadmap-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .roadmap-card {
    padding: 1.5rem;
  }
  
  .step-number {
    font-size: 2rem;
  }
  
  /* CTA Section */
  .cta-section {
    padding: 60px 20px;
  }
  
  .cta-section h2 {
    font-size: 2rem;
  }
  
  .cta-section p {
    font-size: 1rem;
  }
  
  .cta-buttons {
    flex-direction: column;
    gap: 1rem;
  }
  
  .cta-buttons button,
  .cta-buttons a {
    width: 100%;
  }
}

/* Small Mobile (max-width: 480px) */
@media (max-width: 480px) {
  .hero-title {
    font-size: 1.75rem;
  }
  
  .hero-subtitle {
    font-size: 0.9rem;
  }
  
  .orbit-system {
    transform: scale(0.5);
  }
  
  .roadmap h2,
  .cta-section h2 {
    font-size: 1.5rem;
  }
}
</style>
