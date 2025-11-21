<template>
  <div class="container">
    <div class="card">
      <div v-if="loading" class="loading">
        Loading note...
      </div>
      
      <div v-else-if="errorMessage" class="alert alert-error">
        {{ errorMessage }}
        <br><br>
        <button @click="goHome" class="btn btn-secondary">Create New Note</button>
      </div>
      
      <div v-else-if="requiresPassword && !noteContent">
        <h2>🔒 Password Protected Note</h2>
        <p style="margin: 1rem 0;">This note is password protected. Please enter the password to view it.</p>
        
        <form @submit.prevent="fetchNote">
          <div class="form-group">
            <label for="password">Password</label>
            <input 
              type="password" 
              id="password"
              v-model="password"
              placeholder="Enter password"
              required
              autofocus
            >
          </div>
          
          <button type="submit" class="btn btn-primary" :disabled="loading">
            Unlock Note
          </button>
        </form>
      </div>
      
      <div v-else-if="noteContent">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
          <h2>Note</h2>
          <div class="note-meta">
            <span v-if="expiresAt" class="meta-item">
              ⏰ Expires: {{ formatDate(expiresAt) }}
            </span>
            <span class="meta-item">
              👁️ Views: {{ views }}
            </span>
          </div>
        </div>
        
        <div class="note-actions">
          <button @click="toggleView" class="btn btn-secondary">
            {{ showRaw ? 'Show Rendered' : 'Show Raw' }}
          </button>
          <button @click="copyContent" class="btn btn-secondary">
            Copy Content
          </button>
          <button @click="goHome" class="btn btn-primary">
            Create New Note
          </button>
        </div>
        
        <div v-if="showRaw" class="raw-content">
          <textarea readonly :value="noteContent"></textarea>
        </div>
        
        <div v-else class="rendered-content" v-html="renderedContent"></div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { marked } from 'marked'

export default {
  name: 'ViewNote',
  data() {
    return {
      noteContent: '',
      password: '',
      loading: true,
      errorMessage: '',
      requiresPassword: false,
      showRaw: false,
      views: 0,
      expiresAt: null,
      createdAt: null
    }
  },
  computed: {
    renderedContent() {
      if (!this.noteContent) return ''
      return marked(this.noteContent)
    }
  },
  mounted() {
    this.checkNote()
  },
  methods: {
    async checkNote() {
      const noteId = this.$route.params.id
      
      try {
        const response = await axios.get(`/api/notes/${noteId}/check`)
        this.requiresPassword = response.data.requires_password
        
        if (!this.requiresPassword) {
          await this.fetchNote()
        } else {
          this.loading = false
        }
      } catch (error) {
        this.loading = false
        if (error.response?.status === 404) {
          this.errorMessage = 'Note not found. It may have been deleted or expired.'
        } else if (error.response?.status === 410) {
          this.errorMessage = 'This note has expired and has been deleted.'
        } else {
          this.errorMessage = 'Failed to load note. Please try again.'
        }
      }
    },
    
    async fetchNote() {
      this.loading = true
      this.errorMessage = ''
      const noteId = this.$route.params.id
      
      try {
        const params = this.password ? { password: this.password } : {}
        const response = await axios.get(`/api/notes/${noteId}`, { params })
        
        this.noteContent = response.data.content
        this.views = response.data.views
        this.expiresAt = response.data.expires_at
        this.createdAt = response.data.created_at
        
      } catch (error) {
        if (error.response?.status === 403) {
          this.errorMessage = 'Invalid password. Please try again.'
          this.password = ''
        } else if (error.response?.status === 404) {
          this.errorMessage = 'Note not found. It may have been deleted or expired.'
        } else if (error.response?.status === 410) {
          this.errorMessage = 'This note has expired and has been deleted.'
        } else {
          this.errorMessage = 'Failed to load note. Please try again.'
        }
      } finally {
        this.loading = false
      }
    },
    
    toggleView() {
      this.showRaw = !this.showRaw
    },
    
    copyContent() {
      navigator.clipboard.writeText(this.noteContent)
        .then(() => alert('Content copied to clipboard!'))
        .catch(() => {
          const textarea = document.createElement('textarea')
          textarea.value = this.noteContent
          document.body.appendChild(textarea)
          textarea.select()
          document.execCommand('copy')
          document.body.removeChild(textarea)
          alert('Content copied to clipboard!')
        })
    },
    
    goHome() {
      this.$router.push('/')
    },
    
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString()
    }
  }
}
</script>

<style scoped>
h2 {
  color: #333;
  margin: 0;
}

.loading {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #666;
}

.note-meta {
  display: flex;
  gap: 1.5rem;
  font-size: 0.9rem;
  color: #666;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.note-actions {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.raw-content textarea {
  width: 100%;
  min-height: 400px;
  font-family: 'Courier New', monospace;
  padding: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.rendered-content {
  padding: 1.5rem;
  background-color: #f9f9f9;
  border-radius: 5px;
  border: 2px solid #e0e0e0;
  min-height: 200px;
  line-height: 1.6;
}

.rendered-content h1,
.rendered-content h2,
.rendered-content h3,
.rendered-content h4,
.rendered-content h5,
.rendered-content h6 {
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
  color: #333;
}

.rendered-content h1 { font-size: 2rem; }
.rendered-content h2 { font-size: 1.75rem; }
.rendered-content h3 { font-size: 1.5rem; }
.rendered-content h4 { font-size: 1.25rem; }
.rendered-content h5 { font-size: 1.1rem; }
.rendered-content h6 { font-size: 1rem; }

.rendered-content p {
  margin-bottom: 1rem;
}

.rendered-content ul,
.rendered-content ol {
  margin-left: 2rem;
  margin-bottom: 1rem;
}

.rendered-content li {
  margin-bottom: 0.5rem;
}

.rendered-content code {
  background-color: #f0f0f0;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
}

.rendered-content pre {
  background-color: #f0f0f0;
  padding: 1rem;
  border-radius: 5px;
  overflow-x: auto;
  margin-bottom: 1rem;
}

.rendered-content pre code {
  background-color: transparent;
  padding: 0;
}

.rendered-content blockquote {
  border-left: 4px solid #667eea;
  padding-left: 1rem;
  margin-left: 0;
  margin-bottom: 1rem;
  color: #666;
  font-style: italic;
}

.rendered-content a {
  color: #667eea;
  text-decoration: none;
}

.rendered-content a:hover {
  text-decoration: underline;
}

.rendered-content img {
  max-width: 100%;
  height: auto;
  border-radius: 5px;
}

.rendered-content table {
  border-collapse: collapse;
  width: 100%;
  margin-bottom: 1rem;
}

.rendered-content th,
.rendered-content td {
  border: 1px solid #ddd;
  padding: 0.75rem;
  text-align: left;
}

.rendered-content th {
  background-color: #f0f0f0;
  font-weight: bold;
}
</style>
