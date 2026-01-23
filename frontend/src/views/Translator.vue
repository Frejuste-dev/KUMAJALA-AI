<script setup>
import { onMounted } from 'vue';
import TopBar from '@/components/topBar.vue';
import GetStartedButton from '@/components/getStartedButton.vue';
import SelectLang from '@/components/SelectLang.vue';
import { Volume2 as Volume2Icon, Send as SendIcon, RefreshCw as SwapIcon, Copy as CopyIcon, Download as DownloadIcon, Trash2 as ClearIcon, ArrowRightLeft as ArrowRightLeftIcon, Languages as LanguagesIcon, Info as InfoIcon, Home as HomeIcon, Settings as SettingsIcon, Sparkles } from 'lucide-vue-next';
import { useTranslator } from '@/composables/useTranslator';

const {
  inputText,
  translatedText,
  sourceLanguage,
  targetLanguage,
  languages,
  availableTargetLanguages,
  sourceLanguageInfo,
  targetLanguageInfo,
  isLoadingTranslate,
  isLoadingSpeak,
  isLoadingLanguages,
  translationSource,
  processingTime,
  canTranslate,
  canSpeak,
  loadLanguages,
  translate,
  speak,
  swapLanguages,
  copyTranslation,
  downloadAudio,
  clearAll
} = useTranslator();

const navigationItems = [
    { name: 'Accueil', path: '/', icon: HomeIcon },
    { name: 'À Propos', path: '/about', icon: InfoIcon },
    { name: 'Traducteur', path: '/translator', icon: LanguagesIcon },
    { name: 'Paramètres', path: '/settings', icon: SettingsIcon }
];

onMounted(() => {
  loadLanguages();
});
</script>

<template>
  <div class="translator-page page-wrapper">
    <TopBar
      :nav-items="navigationItems"
      variant="blur"
      position="sticky"
      :shrink-on-scroll="true"
      :show-actions="false"
    />

    <section class="translator-section">
      <div class="translator-container">
        <!-- Header -->
        <div class="header-section">
          <h1 class="page-title">
            <span class="icon-box"><Sparkles class="title-icon" /></span>
            Traducteur <span class="text-gradient">Kumajala</span>
          </h1>
          <p class="page-subtitle">
            Interface de traduction neuronale v0.1
          </p>
        </div>

        <!-- Language Controls -->
        <div class="controls-panel glass-panel neon-border-bottom">
          <div class="controls-grid">
            <div class="lang-group">
              <SelectLang
                label="Source"
                v-model="sourceLanguage"
                :options="languages"
                :disabled="isLoadingLanguages"
                class="tech-select"
              />
            </div>

            <button
              class="swap-button glow-effect"
              @click="swapLanguages"
              :disabled="isLoadingTranslate"
              aria-label="Échanger"
            >
              <ArrowRightLeftIcon class="swap-icon" />
            </button>

            <div class="lang-group">
              <SelectLang
                label="Cible"
                v-model="targetLanguage"
                :options="availableTargetLanguages"
                :disabled="isLoadingLanguages"
                class="tech-select"
              />
            </div>
          </div>
        </div>

        <!-- Workspace -->
        <div class="translation-workspace">
          <!-- Input Panel -->
          <div class="translation-panel glass-panel input-panel">
            <div class="panel-header">
              <span class="lang-badge">{{ sourceLanguageInfo?.name || 'Français' }}</span>
              <button class="clear-btn" @click="clearAll" :disabled="!inputText" title="Effacer">
                <ClearIcon width="16" />
              </button>
            </div>
            <div class="panel-body">
              <textarea
                v-model="inputText"
                placeholder="Entrez le texte à analyser..."
                class="tech-textarea"
                :disabled="isLoadingTranslate"
              />
              <div class="char-counter">{{ inputText.length }} chars</div>
            </div>
          </div>

          <!-- Output Panel -->
          <div class="translation-panel glass-panel output-panel" :class="{ 'processing': isLoadingTranslate }">
            <div class="panel-header">
              <span class="lang-badge target">{{ targetLanguageInfo?.name || 'Cible' }}</span>
              <div class="output-actions">
                <button class="action-icon-btn" @click="copyTranslation" :disabled="!translatedText" title="Copier">
                  <CopyIcon width="16" />
                </button>
                <button class="action-icon-btn" @click="downloadAudio" :disabled="!translatedText" title="Audio">
                  <DownloadIcon width="16" />
                </button>
              </div>
            </div>
            <div class="panel-body relative">
              <div v-if="isLoadingTranslate" class="scanning-overlay">
                <div class="scan-line"></div>
                <p class="scan-text">TRAITEMENT EN COURS...</p>
              </div>
              
              <div v-else-if="translatedText" class="result-content">
                <p class="translated-text">{{ translatedText }}</p>
              </div>
              
              <div v-else class="empty-state">
                <LanguagesIcon class="empty-icon" />
                <p>En attente de données...</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions Footer -->
        <div class="action-bar">
          <button 
            class="main-action-btn translate-btn glow-button" 
            @click="translate" 
            :disabled="!canTranslate || isLoadingTranslate"
          >
            <SendIcon class="btn-icon" />
            <span>INITIALISER LA TRADUCTION</span>
          </button>

          <button 
            class="main-action-btn speak-btn neon-border" 
            @click="speak" 
            :disabled="!canSpeak || isLoadingSpeak"
          >
            <Volume2Icon class="btn-icon" />
            <span>SYNTHÈSE VOCALE</span>
          </button>
        </div>

        <!-- Metadata -->
        <div v-if="translatedText && translationSource" class="meta-panel glass-panel">
          <div class="meta-item">
            <span class="label">MOTEUR:</span>
            <span class="value">{{ translationSource }}</span>
          </div>
          <div class="meta-item">
            <span class="label">LATENCE:</span>
            <span class="value">{{ processingTime }}</span>
          </div>
        </div>

      </div>
    </section>
  </div>
</template>

<style scoped>
.page-wrapper {
  background-color: var(--cl-bg-dark);
  min-height: 100vh;
  color: var(--cl-white);
}

.translator-section {
  padding: 40px 20px;
  min-height: calc(100vh - 80px);
}

.translator-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* HEADER */
.header-section {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  font-size: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.icon-box {
  background: rgba(0, 240, 255, 0.1);
  padding: 10px;
  border-radius: 12px;
  border: 1px solid var(--cl-primary);
  display: flex;
}

.title-icon {
  color: var(--cl-primary);
  width: 32px;
  height: 32px;
}

.page-subtitle {
  color: var(--cl-gray-500);
  font-family: var(--font-primary);
  letter-spacing: 2px;
  text-transform: uppercase;
  font-size: 0.9rem;
}

/* CONTROLS */
.controls-panel {
  padding: 1.5rem;
  border-radius: 16px;
  margin-bottom: 2rem;
}

.controls-grid {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.lang-group {
  flex: 1;
}

.swap-button {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--cl-gray-700);
  color: var(--cl-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.swap-button:hover:not(:disabled) {
  background: var(--cl-primary);
  color: var(--cl-bg-dark);
  transform: rotate(180deg);
}

/* WORKSPACE */
.translation-workspace {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

.translation-panel {
  border-radius: 16px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 400px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.translation-panel:focus-within {
  border-color: var(--cl-primary);
  box-shadow: 0 0 15px rgba(0, 240, 255, 0.1);
}

.panel-header {
  padding: 1rem;
  background: rgba(0, 0, 0, 0.2);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.lang-badge {
  font-family: var(--font-display);
  font-size: 0.8rem;
  color: var(--cl-gray-400);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.lang-badge.target {
  color: var(--cl-primary);
}

.panel-body {
  flex: 1;
  padding: 1.5rem;
  position: relative;
}

.tech-textarea {
  width: 100%;
  height: 100%;
  background: transparent;
  border: none;
  color: var(--cl-white);
  font-family: var(--font-primary);
  font-size: 1.2rem;
  resize: none;
  outline: none;
}

.tech-textarea::placeholder {
  color: var(--cl-gray-600);
}

.char-counter {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  font-size: 0.7rem;
  color: var(--cl-gray-600);
}

/* OUTPUT STYLES */
.translated-text {
  font-size: 1.2rem;
  color: var(--cl-primary);
  line-height: 1.6;
}

.empty-state {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--cl-gray-700);
  gap: 1rem;
}

.empty-icon {
  width: 48px;
  height: 48px;
  opacity: 0.2;
}

/* SCANNING ANIMATION */
.scanning-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.scan-line {
  width: 100%;
  height: 2px;
  background: var(--cl-primary);
  box-shadow: 0 0 10px var(--cl-primary);
  animation: scan 1.5s ease-in-out infinite;
}

.scan-text {
  margin-top: 1rem;
  font-family: var(--font-display);
  color: var(--cl-primary);
  font-size: 0.8rem;
  letter-spacing: 2px;
  animation: blink 1s infinite;
}

@keyframes scan {
  0% { transform: translateY(-100px); opacity: 0; }
  50% { opacity: 1; }
  100% { transform: translateY(100px); opacity: 0; }
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* ACTIONS */
.action-bar {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  margin-bottom: 2rem;
}

.main-action-btn {
  padding: 1rem 2rem;
  border-radius: 8px;
  font-family: var(--font-display);
  font-weight: bold;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.translate-btn {
  background: var(--cl-primary);
  color: var(--cl-bg-dark);
}

.translate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 0 30px rgba(0, 240, 255, 0.4);
}

.speak-btn {
  background: transparent;
  border: 1px solid var(--cl-primary);
  color: var(--cl-primary);
}

.speak-btn:hover:not(:disabled) {
  background: rgba(0, 240, 255, 0.1);
}

.main-action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  filter: grayscale(1);
}

/* META PANEL */
.meta-panel {
  display: flex;
  justify-content: center;
  gap: 2rem;
  padding: 1rem;
  border-radius: 50px;
  width: fit-content;
  margin: 0 auto;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.meta-item {
  display: flex;
  gap: 0.5rem;
  font-size: 0.8rem;
}

.meta-item .label {
  color: var(--cl-gray-500);
}

.meta-item .value {
  color: var(--cl-secondary);
  font-family: var(--font-display);
}

/* ===== RESPONSIVE DESIGN ===== */

/* Tablet (768px - 1023px) */
@media (min-width: 768px) and (max-width: 1023px) {
  .translator-section {
    padding: 60px 30px;
  }
  
  .page-title {
    font-size: 2.5rem;
  }
  
  .translation-workspace {
    gap: 1.5rem;
  }
}

/* Mobile (max-width: 767px) */
@media (max-width: 767px) {
  .translator-section {
    padding: 40px 20px;
  }
  
  .page-title {
    font-size: 2rem;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .icon-box {
    padding: 8px;
  }
  
  .title-icon {
    width: 24px;
    height: 24px;
  }
  
  .page-subtitle {
    font-size: 0.8rem;
  }
  
  .controls-panel {
    padding: 1rem;
  }
  
  .controls-grid {
    flex-direction: column;
    gap: 1rem;
  }
  
  .swap-button {
    width: 40px;
    height: 40px;
    margin: 0 auto;
  }
  
  .translation-workspace {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .translation-panel {
    height: 350px;
  }
  
  .panel-header {
    padding: 0.75rem;
  }
  
  .panel-body {
    padding: 1rem;
  }
  
  .action-bar {
    flex-direction: column;
    gap: 1rem;
  }
  
  .main-action-btn {
    width: 100%;
    padding: 0.875rem 1.5rem;
    font-size: 0.95rem;
  }
  
  .meta-panel {
    flex-direction: column;
    gap: 0.5rem;
    padding: 0.75rem;
  }
}

/* Small Mobile (max-width: 480px) */
@media (max-width: 480px) {
  .page-title {
    font-size: 1.5rem;
  }
  
  .translation-panel {
    height: 300px;
  }
  
  .main-action-btn {
    font-size: 0.85rem;
    padding: 0.75rem 1rem;
  }
}
</style>
