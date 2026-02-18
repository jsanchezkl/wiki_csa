<template>
  <div class="fixed right-2 sm:right-4 bottom-4 sm:bottom-6 z-50 flex flex-col items-end gap-2 sm:gap-3">
    <!-- Chat Window -->
    <Transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="opacity-0 translate-y-4 scale-95"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="opacity-100 translate-y-0 scale-100"
      leave-to-class="opacity-0 translate-y-4 scale-95"
    >
      <div 
        v-show="isOpen"
        class="w-[calc(100vw-1rem)] sm:w-96 h-[70vh] sm:h-[32rem] max-h-[600px] bg-white dark:bg-slate-900 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-700 flex flex-col overflow-hidden"
      >
        <!-- Header -->
        <div class="bg-gradient-to-r from-primary to-indigo-600 p-4 text-white">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="p-2 bg-white/20 rounded-xl">
                <span class="material-symbols-outlined">smart_toy</span>
              </div>
              <div>
                <h3 class="font-bold">Wiki Assistant</h3>
                <p class="text-xs text-white/80">Pregúntame sobre la Wiki</p>
              </div>
            </div>
            <button 
              @click="isOpen = false"
              class="p-1 hover:bg-white/20 rounded-lg transition-colors"
            >
              <span class="material-symbols-outlined">close</span>
            </button>
          </div>
        </div>

        <!-- Messages -->
        <div 
          ref="messagesContainer"
          class="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50 dark:bg-slate-800/50"
        >
          <!-- Welcome message -->
          <div v-if="messages.length === 0" class="text-center py-8">
            <div class="inline-flex p-4 bg-primary/10 rounded-full mb-4">
              <span class="material-symbols-outlined text-4xl text-primary">psychology</span>
            </div>
            <h4 class="font-bold text-slate-900 dark:text-white mb-2">¡Hola! Soy tu asistente</h4>
            <p class="text-sm text-slate-500 dark:text-slate-400 max-w-xs mx-auto">
              Puedo responder preguntas sobre políticas, beneficios, procesos y todo el contenido de la Wiki.
            </p>
            <div class="mt-4 space-y-2">
              <button 
                v-for="suggestion in suggestions" 
                :key="suggestion"
                @click="sendMessage(suggestion)"
                class="block w-full text-left px-4 py-2 text-sm bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 hover:border-primary hover:text-primary transition-colors"
              >
                {{ suggestion }}
              </button>
            </div>
          </div>

          <!-- Messages list -->
          <div 
            v-for="(msg, index) in messages" 
            :key="index"
            :class="[
              'flex gap-3',
              msg.role === 'user' ? 'flex-row-reverse' : ''
            ]"
          >
            <!-- Avatar -->
            <div 
              :class="[
                'w-8 h-8 rounded-full flex items-center justify-center shrink-0',
                msg.role === 'user' ? 'bg-primary text-white' : 'bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-300'
              ]"
            >
              <span class="material-symbols-outlined text-lg">
                {{ msg.role === 'user' ? 'person' : 'smart_toy' }}
              </span>
            </div>

            <!-- Message bubble -->
            <div 
              :class="[
                'max-w-[80%] rounded-2xl px-4 py-3',
                msg.role === 'user' 
                  ? 'bg-primary text-white rounded-br-md' 
                  : 'bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 rounded-bl-md'
              ]"
            >
              <p class="text-sm whitespace-pre-wrap">{{ msg.content }}</p>
              
              <!-- Sources -->
              <div v-if="msg.sources && msg.sources.length > 0" class="mt-2 pt-2 border-t border-slate-200 dark:border-slate-600">
                <p class="text-xs text-slate-500 dark:text-slate-400 mb-1">Fuentes:</p>
                <div class="flex flex-wrap gap-1">
                  <router-link
                    v-for="source in msg.sources"
                    :key="source.page_id"
                    :to="`/wiki/${source.title?.toLowerCase().replace(/\s+/g, '-')}`"
                    @click="isOpen = false"
                    class="text-xs px-2 py-1 bg-slate-100 dark:bg-slate-700 rounded-lg text-primary hover:bg-primary/10 transition-colors"
                  >
                    {{ source.title }}
                  </router-link>
                </div>
              </div>
            </div>
          </div>

          <!-- Loading indicator -->
          <div v-if="isLoading" class="flex gap-3">
            <div class="w-8 h-8 rounded-full bg-slate-200 dark:bg-slate-700 flex items-center justify-center">
              <span class="material-symbols-outlined text-lg text-slate-600 dark:text-slate-300 animate-pulse">smart_toy</span>
            </div>
            <div class="bg-white dark:bg-slate-800 rounded-2xl rounded-bl-md px-4 py-3 border border-slate-200 dark:border-slate-700">
              <div class="flex gap-1">
                <div class="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
                <div class="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 150ms"></div>
                <div class="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 300ms"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Input -->
        <div class="p-4 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-700">
          <form @submit.prevent="sendMessage()" class="flex gap-2">
            <input 
              v-model="inputMessage"
              type="text"
              placeholder="Escribe tu pregunta..."
              class="flex-1 px-4 py-3 bg-slate-100 dark:bg-slate-800 rounded-xl text-sm text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-primary/20"
              :disabled="isLoading"
            />
            <button 
              type="submit"
              :disabled="!inputMessage.trim() || isLoading"
              class="px-4 py-3 bg-primary text-white rounded-xl hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <span class="material-symbols-outlined">send</span>
            </button>
          </form>
        </div>
      </div>
    </Transition>

    <!-- Toggle Button -->
    <div class="flex flex-col items-end gap-2">
      <!-- Tooltip -->
      <Transition
        enter-active-class="transition-all duration-200"
        enter-from-class="opacity-0 translate-x-2"
        enter-to-class="opacity-100 translate-x-0"
        leave-active-class="transition-all duration-150"
        leave-from-class="opacity-100 translate-x-0"
        leave-to-class="opacity-0 translate-x-2"
      >
        <div 
          v-show="!isOpen && showTooltip"
          class="bg-slate-900 text-white text-xs font-medium py-2 px-4 rounded-lg shadow-xl relative"
        >
          ¿En qué puedo ayudarte?
          <div class="absolute w-2 h-2 bg-slate-900 rotate-45 -right-1 top-1/2 -translate-y-1/2"></div>
        </div>
      </Transition>

      <!-- FAB Button -->
      <button 
        @click="toggleChat"
        :class="[
          'size-12 sm:size-14 rounded-full shadow-2xl flex items-center justify-center transition-all duration-300',
          isOpen 
            ? 'bg-slate-700 hover:bg-slate-800 rotate-0' 
            : 'bg-primary hover:scale-110 active:scale-95'
        ]"
      >
        <span class="material-symbols-outlined text-2xl sm:text-3xl text-white">
          {{ isOpen ? 'close' : 'smart_toy' }}
        </span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onUnmounted } from 'vue'
import { sendChatMessage, getChatHistory } from '../api'

const isOpen = ref(false)
const showTooltip = ref(true)
const inputMessage = ref('')
const messages = ref([])
const isLoading = ref(false)
const sessionId = ref(null)
const messagesContainer = ref(null)

const suggestions = [
  '¿Cuáles proyectos Google tiene IA?',
  '¿Qué requisitos debo considerar para ABCD detector?',
  '¿De que trata el proyecto Dreamboard?'
]

// Generar o recuperar session ID
onMounted(() => {
  sessionId.value = localStorage.getItem('chat_session_id')
  if (!sessionId.value) {
    sessionId.value = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
    localStorage.setItem('chat_session_id', sessionId.value)
  }
  
  // Cargar historial
  loadHistory()
  
  // Ocultar tooltip después de 5 segundos
  setTimeout(() => {
    showTooltip.value = false
  }, 5000)
})

const loadHistory = async () => {
  try {
    const response = await getChatHistory(sessionId.value)
    if (response.data.messages) {
      messages.value = response.data.messages
      scrollToBottom()
    }
  } catch (error) {
    console.error('Error loading chat history:', error)
  }
}

const toggleChat = () => {
  isOpen.value = !isOpen.value
  showTooltip.value = false
  if (isOpen.value) {
    nextTick(() => scrollToBottom())
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const sendMessage = async (text = null) => {
  const messageText = text || inputMessage.value.trim()
  
  if (!messageText || isLoading.value) return
  
  // Agregar mensaje del usuario
  messages.value.push({
    role: 'user',
    content: messageText
  })
  
  inputMessage.value = ''
  isLoading.value = true
  scrollToBottom()
  
  try {
    const response = await sendChatMessage(messageText, sessionId.value)
    
    // Agregar respuesta del asistente
    messages.value.push({
      role: 'assistant',
      content: response.data.response,
      sources: response.data.sources || []
    })
    
    // Actualizar session ID si es nuevo
    if (response.data.session_id) {
      sessionId.value = response.data.session_id
      localStorage.setItem('chat_session_id', sessionId.value)
    }
    
  } catch (error) {
    console.error('Error sending message:', error)
    messages.value.push({
      role: 'assistant',
      content: 'Lo siento, ocurrió un error al procesar tu mensaje. Por favor, intenta de nuevo.'
    })
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}
</script>

<style scoped>
/* Custom scrollbar for messages */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>




