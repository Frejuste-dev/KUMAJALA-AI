<template>
  <div class="african-patterns-container">
    <!-- Kente Pattern Border -->
    <div v-if="type === 'kente'" class="kente-pattern">
      <div class="kente-stripe" v-for="i in 8" :key="i" :style="{ animationDelay: `${i * 0.1}s` }"></div>
    </div>

    <!-- Adinkra Symbols (Floating) -->
    <div v-if="type === 'adinkra'" class="adinkra-symbols">
      <!-- Sankofa: "Return and get it" - Learning from the past -->
      <svg class="adinkra-symbol sankofa" viewBox="0 0 100 100">
        <path d="M50 10 Q30 30 50 50 Q70 30 50 10 M50 50 L50 90 M40 70 Q50 80 60 70" 
              stroke="currentColor" fill="none" stroke-width="3"/>
      </svg>
      
      <!-- Gye Nyame: "Except God" - Supremacy of God -->
      <svg class="adinkra-symbol gye-nyame" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="30" stroke="currentColor" fill="none" stroke-width="3"/>
        <path d="M50 20 L50 80 M20 50 L80 50" stroke="currentColor" stroke-width="3"/>
      </svg>
      
      <!-- Dwennimmen: "Ram's horns" - Strength and humility -->
      <svg class="adinkra-symbol dwennimmen" viewBox="0 0 100 100">
        <path d="M30 30 Q50 10 70 30 Q90 50 70 70 Q50 90 30 70 Q10 50 30 30" 
              stroke="currentColor" fill="none" stroke-width="3"/>
      </svg>
      
      <!-- Nkyinkyim: "Twisting" - Initiative, dynamism -->
      <svg class="adinkra-symbol nkyinkyim" viewBox="0 0 100 100">
        <path d="M20 50 Q30 30 50 50 Q70 70 80 50 M50 20 Q50 40 50 50 Q50 60 50 80" 
              stroke="currentColor" fill="none" stroke-width="3"/>
      </svg>
      
      <!-- Aya: "Fern" - Endurance and resourcefulness -->
      <svg class="adinkra-symbol aya" viewBox="0 0 100 100">
        <path d="M50 20 L50 80 M30 40 L50 40 M30 60 L50 60 M70 40 L50 40 M70 60 L50 60" 
              stroke="currentColor" fill="none" stroke-width="3"/>
        <circle cx="30" cy="40" r="3" fill="currentColor"/>
        <circle cx="70" cy="40" r="3" fill="currentColor"/>
        <circle cx="30" cy="60" r="3" fill="currentColor"/>
        <circle cx="70" cy="60" r="3" fill="currentColor"/>
      </svg>
      
      <!-- Funtunfunefu Denkyemfunefu: "Siamese crocodiles" - Unity in diversity -->
      <svg class="adinkra-symbol funtun" viewBox="0 0 100 100">
        <ellipse cx="35" cy="50" rx="15" ry="25" stroke="currentColor" fill="none" stroke-width="2"/>
        <ellipse cx="65" cy="50" rx="15" ry="25" stroke="currentColor" fill="none" stroke-width="2"/>
        <circle cx="50" cy="50" r="5" fill="currentColor"/>
      </svg>
    </div>

    <!-- Mudcloth Pattern -->
    <div v-if="type === 'mudcloth'" class="mudcloth-pattern">
      <svg class="mudcloth-bg" viewBox="0 0 200 200">
        <defs>
          <pattern id="mudcloth" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
            <line x1="0" y1="20" x2="40" y2="20" stroke="currentColor" stroke-width="2" opacity="0.3"/>
            <line x1="20" y1="0" x2="20" y2="40" stroke="currentColor" stroke-width="2" opacity="0.3"/>
            <circle cx="10" cy="10" r="2" fill="currentColor" opacity="0.5"/>
            <circle cx="30" cy="30" r="2" fill="currentColor" opacity="0.5"/>
          </pattern>
        </defs>
        <rect width="200" height="200" fill="url(#mudcloth)"/>
      </svg>
    </div>

    <!-- African Map Outline -->
    <div v-if="type === 'africa-map'" class="africa-map">
      <svg class="africa-outline" viewBox="0 0 300 400" preserveAspectRatio="xMidYMid meet">
        <path class="continent-path" 
              d="M150 50 L180 60 L200 80 L210 100 L220 130 L230 160 L235 190 L230 220 L220 250 L200 280 L180 310 L160 340 L140 360 L120 370 L100 360 L80 340 L60 310 L50 280 L45 250 L50 220 L60 190 L70 160 L80 130 L90 100 L110 70 L130 55 Z"
              fill="none" 
              stroke="currentColor" 
              stroke-width="3"/>
        <!-- Pulse effect -->
        <circle class="pulse-dot" cx="150" cy="200" r="5" fill="var(--cl-primary)"/>
      </svg>
    </div>
  </div>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    default: 'kente',
    validator: (value) => ['kente', 'adinkra', 'mudcloth', 'africa-map'].includes(value)
  },
  colorVariant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'mixed'].includes(value)
  }
});
</script>

<style scoped>
.african-patterns-container {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
  opacity: 0.15;
}

/* KENTE PATTERN */
.kente-pattern {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  gap: 10px;
}

.kente-stripe {
  flex: 1;
  background: linear-gradient(
    180deg,
    var(--cl-primary) 0%,
    var(--cl-secondary) 50%,
    var(--cl-tertiary) 100%
  );
  animation: kente-slide 8s ease-in-out infinite;
}

@keyframes kente-slide {
  0%, 100% { transform: translateY(0); opacity: 0.3; }
  50% { transform: translateY(-20px); opacity: 0.6; }
}

/* ADINKRA SYMBOLS */
.adinkra-symbols {
  position: relative;
  width: 100%;
  height: 100%;
}

.adinkra-symbol {
  position: absolute;
  width: 80px;
  height: 80px;
  color: var(--cl-primary);
  animation: float 6s ease-in-out infinite;
}

.sankofa {
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.gye-nyame {
  top: 50%;
  right: 15%;
  animation-delay: 2s;
}

.dwennimmen {
  bottom: 20%;
  left: 20%;
  animation-delay: 4s;
}

.nkyinkyim {
  top: 30%;
  left: 50%;
  animation-delay: 1s;
}

.aya {
  bottom: 10%;
  right: 30%;
  animation-delay: 3s;
}

.funtun {
  top: 70%;
  left: 60%;
  animation-delay: 5s;
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-30px) rotate(10deg); }
}

/* MUDCLOTH PATTERN */
.mudcloth-pattern {
  position: absolute;
  inset: 0;
}

.mudcloth-bg {
  width: 100%;
  height: 100%;
  color: var(--cl-primary);
}

/* AFRICA MAP */
.africa-map {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 300px;
  height: 400px;
}

.africa-outline {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 0 20px var(--cl-primary));
}

.continent-path {
  color: var(--cl-primary);
  animation: draw-continent 3s ease-in-out infinite alternate;
}

@keyframes draw-continent {
  0% { 
    stroke-dasharray: 1000;
    stroke-dashoffset: 1000;
    opacity: 0.3;
  }
  100% { 
    stroke-dasharray: 1000;
    stroke-dashoffset: 0;
    opacity: 0.8;
  }
}

.pulse-dot {
  animation: pulse-grow 2s ease-in-out infinite;
}

@keyframes pulse-grow {
  0%, 100% { 
    r: 5;
    opacity: 1;
  }
  50% { 
    r: 15;
    opacity: 0.3;
  }
}

/* Accessibility: Reduce motion */
@media (prefers-reduced-motion: reduce) {
  .kente-stripe,
  .adinkra-symbol,
  .continent-path,
  .pulse-dot {
    animation: none;
  }
}
</style>
