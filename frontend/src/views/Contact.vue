<script setup>
import { ref } from 'vue';
import axios from 'axios';
import TopBar from '@/components/topBar.vue';
import Footer from '@/components/Footer.vue';
import { Home as HomeIcon, Info as InfoIcon, Languages as LanguagesIcon, Settings as SettingsIcon, Mail as MailIcon, MapPin as MapPinIcon, Phone as PhoneIcon, Send as SendIcon } from 'lucide-vue-next';

const navigationItems = [
    { name: 'Accueil', path: '/', icon: HomeIcon },
    { name: 'À Propos', path: '/about', icon: InfoIcon },
    { name: 'Traducteur', path: '/translator', icon: LanguagesIcon },
    { name: 'Contact', path: '/contact', icon: MailIcon },
    { name: 'Paramètres', path: '/settings', icon: SettingsIcon }
];

// Form data
const formData = ref({
  name: '',
  email: '',
  subject: 'Investissement',
  message: ''
});

const isSubmitting = ref(false);
const submitMessage = ref('');
const submitError = ref('');

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const handleSubmit = async () => {
  isSubmitting.value = true;
  submitMessage.value = '';
  submitError.value = '';

  try {
    const response = await axios.post(`${API_URL}/kumajala-api/v1/contact`, formData.value);
    
    if (response.data.success) {
      submitMessage.value = 'Message envoyé avec succès ! Nous vous répondrons bientôt.';
      // Reset form
      formData.value = {
        name: '',
        email: '',
        subject: 'Investissement',
        message: ''
      };
    }
  } catch (error) {
    console.error('Erreur lors de l\'envoi:', error);
    submitError.value = error.response?.data?.error || 'Erreur lors de l\'envoi du message. Veuillez réessayer.';
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<template>
  <div class="contact-page page-wrapper">
    <TopBar
      :nav-items="navigationItems"
      variant="blur"
      position="sticky"
      :shrink-on-scroll="true"
    />

    <section class="contact-hero">
      <div class="container">
        <h1 class="page-title">
          Contactez <span class="text-gradient">l'Équipe</span>
        </h1>
        <p class="page-subtitle">
          Rejoignez l'aventure Kumajala. Investisseurs, contributeurs, développeurs.
        </p>

        <div class="contact-grid">
          <!-- Contact Info Card -->
          <div class="info-card glass-panel neon-border-hover">
            <h3>Nos Coordonnées</h3>
            <div class="info-item">
              <div class="icon-box"><MailIcon /></div>
              <div>
                <span class="label">Email</span>
                <p>contact@kumajala.africa</p>
              </div>
            </div>
            <div class="info-item">
              <div class="icon-box"><PhoneIcon /></div>
              <div>
                <span class="label">Téléphone</span>
                <p>+225 07 00 00 00 00</p>
              </div>
            </div>
            <div class="info-item">
              <div class="icon-box"><MapPinIcon /></div>
              <div>
                <span class="label">Siège</span>
                <p>Abidjan, Côte d'Ivoire</p>
              </div>
            </div>
          </div>

          <!-- Contact Form -->
          <div class="form-card glass-panel neon-border-bottom">
            <form @submit.prevent="handleSubmit" class="contact-form">
              <!-- Success/Error Messages -->
              <div v-if="submitMessage" class="alert alert-success">
                {{ submitMessage }}
              </div>
              <div v-if="submitError" class="alert alert-error">
                {{ submitError }}
              </div>

              <div class="form-group">
                <label>Nom Complet</label>
                <input v-model="formData.name" type="text" placeholder="Votre nom" class="tech-input" required :disabled="isSubmitting" />
              </div>
              <div class="form-group">
                <label>Email</label>
                <input v-model="formData.email" type="email" placeholder="votre@email.com" class="tech-input" required :disabled="isSubmitting" />
              </div>
              <div class="form-group">
                <label>Sujet</label>
                <select v-model="formData.subject" class="tech-input" :disabled="isSubmitting">
                  <option>Investissement</option>
                  <option>Contribution Données</option>
                  <option>Partenariat Technique</option>
                  <option>Autre</option>
                </select>
              </div>
              <div class="form-group">
                <label>Message</label>
                <textarea v-model="formData.message" placeholder="Votre message..." class="tech-input textarea" rows="5" required :disabled="isSubmitting"></textarea>
              </div>
              
              <button type="submit" class="glow-button submit-btn" :disabled="isSubmitting">
                <SendIcon class="btn-icon" />
                <span>{{ isSubmitting ? 'Envoi en cours...' : 'Envoyer le Message' }}</span>
              </button>
            </form>
          </div>
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
  display: flex;
  flex-direction: column;
}

.contact-hero {
  padding: 80px 20px;
  flex: 1;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-size: 3.5rem;
  text-align: center;
  margin-bottom: 1rem;
}

.page-subtitle {
  text-align: center;
  color: var(--cl-gray-500);
  font-size: 1.2rem;
  margin-bottom: 4rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.contact-grid {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 3rem;
}

/* INFO CARD */
.info-card {
  padding: 2.5rem;
  border-radius: 24px;
  height: fit-content;
}

.info-card h3 {
  font-size: 1.5rem;
  margin-bottom: 2rem;
  color: var(--cl-primary);
}

.info-item {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.icon-box {
  width: 50px;
  height: 50px;
  background: rgba(241, 137, 14, 0.1);
  border: 1px solid var(--cl-primary);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--cl-primary);
}

.label {
  display: block;
  font-size: 0.8rem;
  color: var(--cl-gray-500);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 0.2rem;
}

.info-item p {
  font-size: 1.1rem;
  font-weight: 600;
}

/* FORM CARD */
.form-card {
  padding: 3rem;
  border-radius: 24px;
}

.contact-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.9rem;
  color: var(--cl-gray-400);
  font-family: var(--font-display);
}

.tech-input {
  background: var(--cl-bg-input);
  border: 1px solid var(--cl-gray-200);
  padding: 1rem;
  border-radius: 12px;
  color: var(--cl-white);
  font-family: var(--font-primary);
  font-size: 1rem;
  transition: all 0.3s ease;
}

.tech-input:focus {
  outline: none;
  border-color: var(--cl-primary);
  box-shadow: 0 0 15px rgba(241, 137, 14, 0.2);
}

.textarea {
  resize: vertical;
}

.submit-btn {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* ALERTS */
.alert {
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 0.95rem;
}

.alert-success {
  background: rgba(0, 255, 157, 0.1);
  border: 1px solid #00FF9D;
  color: #00FF9D;
}

.alert-error {
  background: rgba(255, 0, 60, 0.1);
  border: 1px solid #FF003C;
  color: #FF003C;
}

/* ===== RESPONSIVE DESIGN ===== */

/* Tablet (768px - 1023px) */
@media (min-width: 768px) and (max-width: 1023px) {
  .contact-hero {
    padding: 100px 40px;
  }
  
  .page-title {
    font-size: 3rem;
  }
  
  .contact-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}

/* Mobile (max-width: 767px) */
@media (max-width: 767px) {
  .contact-hero {
    padding: 60px 20px;
  }
  
  .page-title {
    font-size: 2.25rem;
  }
  
  .page-subtitle {
    font-size: 1rem;
    margin-bottom: 3rem;
  }
  
  .contact-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .info-card {
    padding: 2rem;
  }
  
  .info-card h3 {
    font-size: 1.25rem;
  }
  
  .info-item {
    gap: 1rem;
  }
  
  .icon-box {
    width: 45px;
    height: 45px;
  }
  
  .info-item p {
    font-size: 1rem;
  }
  
  .form-card {
    padding: 2rem;
  }
  
  .contact-form {
    gap: 1.25rem;
  }
  
  .form-group label {
    font-size: 0.85rem;
  }
  
  .tech-input {
    padding: 0.875rem;
    font-size: 0.95rem;
  }
  
  .submit-btn {
    padding: 0.875rem;
    font-size: 1rem;
  }
  
  .alert {
    font-size: 0.9rem;
    padding: 0.875rem;
  }
}

/* Small Mobile (max-width: 480px) */
@media (max-width: 480px) {
  .page-title {
    font-size: 1.75rem;
  }
  
  .page-subtitle {
    font-size: 0.9rem;
  }
  
  .info-card,
  .form-card {
    padding: 1.5rem;
  }
  
  .info-card h3 {
    font-size: 1.1rem;
  }
  
  .submit-btn {
    font-size: 0.9rem;
  }
}
</style>
