<template>
  <div class="rich-text-editor border border-slate-200 dark:border-slate-700 rounded-xl overflow-hidden">
    <!-- Toolbar -->
    <div class="toolbar bg-slate-50 dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 p-2 flex flex-wrap gap-1">
      <!-- Text formatting -->
      <div class="flex items-center gap-1 px-1 border-r border-slate-200 dark:border-slate-700">
        <button
          @click="editor?.chain().focus().toggleBold().run()"
          :class="{ 'bg-primary/20 text-primary': editor?.isActive('bold') }"
          class="p-2 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
          title="Negrita"
        >
          <span class="material-symbols-outlined text-lg">format_bold</span>
        </button>
        <button
          @click="editor?.chain().focus().toggleItalic().run()"
          :class="{ 'bg-primary/20 text-primary': editor?.isActive('italic') }"
          class="p-2 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
          title="Cursiva"
        >
          <span class="material-symbols-outlined text-lg">format_italic</span>
        </button>
        <button
          @click="editor?.chain().focus().toggleUnderline().run()"
          :class="{ 'bg-primary/20 text-primary': editor?.isActive('underline') }"
          class="p-2 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
          title="Subrayado"
        >
          <span class="material-symbols-outlined text-lg">format_underlined</span>
        </button>
        <button
          @click="editor?.chain().focus().toggleStrike().run()"
          :class="{ 'bg-primary/20 text-primary': editor?.isActive('strike') }"
          class="p-2 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
          title="Tachado"
        >
          <span class="material-symbols-outlined text-lg">strikethrough_s</span>
        </button>
      </div>

      <!-- Headings -->
      <div class="flex items-center gap-1 px-1 border-r border-slate-200 dark:border-slate-700">
        <button
          @click="editor?.chain().focus().toggleHeading({ level: 2 }).run()"
          :class="{ 'bg-primary/20 text-primary': editor?.isActive('heading', { level: 2 }) }"
          class="p-2 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors text-sm font-bold"
          title="Título 2"
        >
          H2
        </button>
        <button
          @click="editor?.chain().focus().toggleHeading({ level: 3 }).run()"
          :class="{ 'bg-primary/20 text-primary': editor?.isActive('heading', { level: 3 }) }"
          class="p-2 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors text-sm font-bold"
          title="Título 3"
        >
          H3
        </button>
        <button
          @click="editor?.chain().focus().toggleHeading({ level: 4 }).run()"
          :class="{ 'bg-primary/20 text-primary': editor?.isActive('heading', { level: 4 }) }"
          class="p-2 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors text-sm font-bold"
          title="Título 4"
        >
          H4
        </button>
        <button
          @click="editor?.chain().focus().setParagraph().run()"
          :class="{ 'bg-primary/20 text-primary': editor?.isActive('paragraph') }"
          class="p-2 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
          title="Párrafo"
        >
          <span class="material-symbols-outlined text-lg">format_paragraph</span>
        </button>
      </div>

      <!-- Lists -->
      <div class="flex items-center gap-1 px-1 border-r border-slate-200 dark:border-slate-700">
        <button
          @click="editor?.chain().focus().toggleBulletList().run()"
          :class="{ 'bg-primary/20 text-primary': editor?.isActive('bulletList') }"
          class="p-2 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
          title="Lista con viñetas"
        >
          <span class="material-symbols-outlined text-lg">format_list_bulleted</span>
        </button>
        <button
          @click="editor?.chain().focus().toggleOrderedList().run()"
          :class="{ 'bg-primary/20 text-primary': editor?.isActive('orderedList') }"
          class="p-2 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
          title="Lista numerada"
        >
          <span class="material-symbols-outlined text-lg">format_list_numbered</span>
        </button>
      </div>

      <!-- Alignment -->
      <div class="flex items-center gap-1 px-1 border-r border-slate-200 dark:border-slate-700">
        <button
          @click="editor?.chain().focus().setTextAlign('left').run()"
          :class="{ 'bg-primary/20 text-primary': editor?.isActive({ textAlign: 'left' }) }"
          class="p-2 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
          title="Alinear izquierda"
        >
          <span class="material-symbols-outlined text-lg">format_align_left</span>
        </button>
        <button
          @click="editor?.chain().focus().setTextAlign('center').run()"
          :class="{ 'bg-primary/20 text-primary': editor?.isActive({ textAlign: 'center' }) }"
          class="p-2 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
          title="Centrar"
        >
          <span class="material-symbols-outlined text-lg">format_align_center</span>
        </button>
        <button
          @click="editor?.chain().focus().setTextAlign('right').run()"
          :class="{ 'bg-primary/20 text-primary': editor?.isActive({ textAlign: 'right' }) }"
          class="p-2 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
          title="Alinear derecha"
        >
          <span class="material-symbols-outlined text-lg">format_align_right</span>
        </button>
      </div>

      <!-- Media -->
      <div class="flex items-center gap-1 px-1 border-r border-slate-200 dark:border-slate-700">
        <button
          @click="addLink"
          :class="{ 'bg-primary/20 text-primary': editor?.isActive('link') }"
          class="p-2 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
          title="Insertar enlace"
        >
          <span class="material-symbols-outlined text-lg">link</span>
        </button>
        <button
          @click="addImage"
          class="p-2 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
          title="Insertar imagen"
        >
          <span class="material-symbols-outlined text-lg">image</span>
        </button>
      </div>

      <!-- Blocks -->
      <div class="flex items-center gap-1 px-1 border-r border-slate-200 dark:border-slate-700">
        <button
          @click="editor?.chain().focus().toggleBlockquote().run()"
          :class="{ 'bg-primary/20 text-primary': editor?.isActive('blockquote') }"
          class="p-2 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
          title="Cita"
        >
          <span class="material-symbols-outlined text-lg">format_quote</span>
        </button>
        <button
          @click="editor?.chain().focus().setHorizontalRule().run()"
          class="p-2 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
          title="Línea horizontal"
        >
          <span class="material-symbols-outlined text-lg">horizontal_rule</span>
        </button>
        <button
          @click="editor?.chain().focus().toggleCodeBlock().run()"
          :class="{ 'bg-primary/20 text-primary': editor?.isActive('codeBlock') }"
          class="p-2 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
          title="Bloque de código"
        >
          <span class="material-symbols-outlined text-lg">code</span>
        </button>
      </div>

      <!-- Undo/Redo -->
      <div class="flex items-center gap-1 px-1">
        <button
          @click="editor?.chain().focus().undo().run()"
          :disabled="!editor?.can().undo()"
          class="p-2 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors disabled:opacity-40"
          title="Deshacer"
        >
          <span class="material-symbols-outlined text-lg">undo</span>
        </button>
        <button
          @click="editor?.chain().focus().redo().run()"
          :disabled="!editor?.can().redo()"
          class="p-2 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors disabled:opacity-40"
          title="Rehacer"
        >
          <span class="material-symbols-outlined text-lg">redo</span>
        </button>
      </div>
    </div>

    <!-- Editor content -->
    <editor-content 
      :editor="editor" 
      class="prose prose-slate dark:prose-invert max-w-none p-6 min-h-[400px] focus:outline-none bg-white dark:bg-slate-900"
    />
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Image from '@tiptap/extension-image'
import Link from '@tiptap/extension-link'
import Placeholder from '@tiptap/extension-placeholder'
import TextAlign from '@tiptap/extension-text-align'
import Underline from '@tiptap/extension-underline'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Escribe tu contenido aquí...'
  }
})

const emit = defineEmits(['update:modelValue'])

const editor = useEditor({
  content: props.modelValue,
  extensions: [
    StarterKit,
    Image.configure({
      inline: true,
      allowBase64: true,
    }),
    Link.configure({
      openOnClick: false,
      HTMLAttributes: {
        class: 'text-primary underline',
      },
    }),
    Placeholder.configure({
      placeholder: props.placeholder,
    }),
    TextAlign.configure({
      types: ['heading', 'paragraph'],
    }),
    Underline,
  ],
  onUpdate: ({ editor }) => {
    emit('update:modelValue', editor.getHTML())
  },
})

watch(() => props.modelValue, (newValue) => {
  const isSame = editor.value?.getHTML() === newValue
  if (!isSame) {
    editor.value?.commands.setContent(newValue, false)
  }
})

const addLink = () => {
  const url = window.prompt('URL del enlace:')
  if (url) {
    editor.value?.chain().focus().setLink({ href: url }).run()
  }
}

const addImage = () => {
  const url = window.prompt('URL de la imagen:')
  if (url) {
    editor.value?.chain().focus().setImage({ src: url }).run()
  }
}

onBeforeUnmount(() => {
  editor.value?.destroy()
})
</script>

<style>
.ProseMirror {
  outline: none;
  min-height: 400px;
}

.ProseMirror p.is-editor-empty:first-child::before {
  color: #adb5bd;
  content: attr(data-placeholder);
  float: left;
  height: 0;
  pointer-events: none;
}

.ProseMirror img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 1rem 0;
}

.ProseMirror blockquote {
  border-left: 4px solid #3b82f6;
  padding-left: 1rem;
  margin: 1rem 0;
  color: #64748b;
  font-style: italic;
}

.ProseMirror pre {
  background: #1e293b;
  color: #e2e8f0;
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
}

.ProseMirror code {
  background: #f1f5f9;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-size: 0.9em;
}

.ProseMirror hr {
  border: none;
  border-top: 2px solid #e2e8f0;
  margin: 2rem 0;
}

.ProseMirror ul {
  list-style-type: disc;
  padding-left: 1.5rem;
}

.ProseMirror ol {
  list-style-type: decimal;
  padding-left: 1.5rem;
}

.ProseMirror h2 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.ProseMirror h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

.ProseMirror h4 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-top: 1.25rem;
  margin-bottom: 0.5rem;
}
</style>




