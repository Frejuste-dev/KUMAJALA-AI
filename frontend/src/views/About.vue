<script setup>
import EnhancedHeader from '@/components/topBar.vue';
import AfricanPatterns from '@/components/AfricanPatterns.vue';
import { Home as HomeIcon, Info as InfoIcon, Languages as LanguagesIcon, Settings as SettingsIcon, Target, Users, Zap } from 'lucide-vue-next'; 
import Footer from '@/components/Footer.vue'; 

const navigationItems = [
    { name: 'Accueil', path: '/', icon: HomeIcon }, 
    { name: 'À Propos', path: '/about', icon: InfoIcon },
    { name: 'Traducteur', path: '/translator', icon: LanguagesIcon },
    { name: 'Paramètres', path: '/settings', icon: SettingsIcon }
];

const handleLogoClick = () => {
    console.log('Logo clicked!');
};

const handleNavClick = (item) => {
    console.log('Nav item clicked:', item.name);
};
</script>

<template>
  <div class="page-wrapper">
    <EnhancedHeader
      :nav-items="navigationItems"
      variant="blur"
      position="sticky"
      :shrink-on-scroll="true"
      @logo-click="handleLogoClick"
      @nav-item-click="handleNavClick"
    />

    <!-- SECTION HERO ABOUT -->
    <section class="about-hero">
      <!-- Mudcloth Pattern Background -->
      <AfricanPatterns type="mudcloth" colorVariant="secondary" />
      
      <div class="hero-content">
        <h1>La Vision <span class="text-gradient">Kumajala</span></h1>
        <p class="subtitle">De l'IA générative généraliste vers une souveraineté linguistique africaine.</p>
      </div>
    </section>

    <section class="about-content">
      <!-- MISSION / VISION GRID -->
      <div class="grid-layout">
        <div class="content-card glass-panel neon-border-hover">
          <div class="card-icon"><Target /></div>
          <h2>Le Problème</h2>
          <p>
            Les modèles actuels (LLM) sont entraînés majoritairement sur des données occidentales. Nos langues (Bété, Baoulé, etc.) sont "low-resource", ce qui entraîne des hallucinations et des traductions approximatives.
          </p>
        </div>

        <div class="content-card glass-panel neon-border-hover">
          <div class="card-icon"><Zap /></div>
          <h2>La Solution : Prototype v0.1</h2>
          <p>
            Nous utilisons actuellement <strong>Gemini 2.0 Flash</strong> comme moteur temporaire pour valider l'interface et l'usage. Ce n'est que la première étape.
          </p>
        </div>

        <div class="content-card glass-panel neon-border-hover">
          <div class="card-icon"><Users /></div>
          <h2>L'Objectif Final</h2>
          <p>
            Créer le <strong>Kumajala-1B</strong>, un petit modèle de langage (SLM) spécialisé, entraîné sur un dataset propriétaire de haute qualité, collecté auprès des locuteurs natifs.
          </p>
        </div>
      </div>

      <!-- CALL FOR DATA / INVESTMENT -->
      <div class="investment-section glass-panel">
        <div class="investment-content">
          <h2>Nous avons besoin de vous</h2>
          <p>Pour passer du prototype au produit final, nous cherchons :</p>
          <ul class="needs-list">
            <li>💾 <strong>Données</strong> : Enregistrements audio et textes traduits.</li>
            <li>💰 <strong>Investissement</strong> : Financement pour les GPU et l'équipe R&D.</li>
            <li>🤝 <strong>Partenariats</strong> : Universités et centres culturels.</li>
          </ul>
          <a class="btn btn-primary btn-lg glow-button" href="/contact">
            Contacter l'équipe Fondatrice
          </a>
        </div>
      </div>
    </section>

    <Footer />
  </div>
</template>

<style scoped>
.page-wrapper {
  background-color: var(--cl-bg-dark);
  min-height: 100vh;
  color: var(--cl-white);
}

.about-hero {
  padding: 120px 20px;
  text-align: center;
  background: radial-gradient(circle at center, rgba(112, 0, 255, 0.1) 0%, transparent 70%);
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-content {
  max-width: 800px;
}

.about-hero h1 {
  font-size: 3.5rem;
  margin-bottom: 1.5rem;
  font-weight: 800;
  color: var(--cl-white);
}

.subtitle {
  font-size: 1.5rem;
  color: var(--cl-gray-500);
  line-height: 1.6;
}

.about-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 80px 20px;
}

.grid-layout {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 6rem;
}

.content-card {
  padding: 2.5rem;
  border-radius: 16px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.neon-border-hover:hover {
  border-color: var(--cl-secondary);
  box-shadow: 0 0 20px rgba(112, 0, 255, 0.2);
  transform: translateY(-5px);
}

.card-icon {
  font-size: 2rem;
  color: var(--cl-primary);
  margin-bottom: 1.5rem;
  background: rgba(0, 240, 255, 0.1);
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.content-card h2 {
  font-size: 1.5rem;
  color: var(--cl-white);
  margin-bottom: 1rem;
}

.content-card p {
  font-size: 1.1rem;
  line-height: 1.7;
  color: var(--cl-gray-500);
}

.investment-section {
  border-radius: 24px;
  padding: 4rem;
  border: 1px solid var(--cl-primary);
  box-shadow: 0 0 30px rgba(0, 240, 255, 0.1);
  text-align: center;
}

.investment-content h2 {
  font-size: 2.5rem;
  margin-bottom: 2rem;
  color: var(--cl-white);
}

.needs-list {
  list-style: none;
  padding: 0;
  display: flex;
  justify-content: center;
  gap: 3rem;
  margin-bottom: 3rem;
  flex-wrap: wrap;
}

.needs-list li {
  font-size: 1.2rem;
  color: var(--cl-gray-400);
  background: rgba(255, 255, 255, 0.05);
  padding: 1rem 2rem;
  border-radius: 50px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.needs-list strong {
  color: var(--cl-primary);
}

.glow-button {
  box-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
}

/* ===== RESPONSIVE DESIGN ===== */

/* Tablet (768px - 1023px) */
@media (min-width: 768px) and (max-width: 1023px) {
  .about-hero {
    padding: 100px 40px;
  }
  
  .about-hero h1 {
    font-size: 3rem;
  }
  
  .content-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}

/* Mobile (max-width: 767px) */
@media (max-width: 767px) {
  .about-hero {
    padding: 60px 20px;
  }
  
  .about-hero h1 {
    font-size: 2.25rem;
  }
  
  .about-hero p {
    font-size: 1rem;
  }
  
  .content-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .content-card {
    padding: 1.5rem;
  }
  
  .content-card h2 {
    font-size: 1.5rem;
  }
  
  .needs-list {
    flex-direction: column;
    gap: 1rem;
  }
  
  .need-item {
    width: 100%;
  }
  
  .investment-section {
    padding: 2rem 1.5rem;
  }
  
  .investment-section h3 {
    font-size: 1.5rem;
  }
  
  .glow-button {
    width: 100%;
    justify-content: center;
  }
}

/* Small Mobile (max-width: 480px) */
@media (max-width: 480px) {
  .about-hero h1 {
    font-size: 1.75rem;
  }
  
  .about-hero p {
    font-size: 0.9rem;
  }
  
  .content-card h2 {
    font-size: 1.25rem;
  }
  
  .investment-section h3 {
    font-size: 1.25rem;
  }
}
</style>
