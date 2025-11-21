<template>
  <div class="container">
    <div class="card">
      <h2>Create a New Note</h2>
      
      <div v-if="successMessage" class="alert alert-success">
        {{ successMessage }}
        <br><br>
        <strong>Share Link:</strong>
        <div class="share-link">
          <input type="text" :value="shareLink" readonly ref="shareLinkInput">
          <button @click="copyShareLink" class="btn btn-secondary">Copy</button>
        </div>
      </div>
      
      <div v-if="errorMessage" class="alert alert-error">
        {{ errorMessage }}
      </div>
      
      <form @submit.prevent="createNote" v-if="!successMessage">
        <div class="form-group">
          <label for="content">Note Content (Markdown supported)</label>
          <textarea 
            id="content" 
            v-model="noteContent"
            placeholder="Write your note here... You can use markdown syntax!
            
Examples:
# Heading
**bold** or *italic*
- List item
[Link](https://example.com)"
            required
          ></textarea>
        </div>
        
        <div class="form-group">
          <label for="password">Password Protection (Optional)</label>
          <input 
            type="password" 
            id="password"
            v-model="password"
            placeholder="Leave empty for no password"
          >
          <small style="color: #666; display: block; margin-top: 0.5rem;">
            Add a password to protect your note from unauthorized access
          </small>
        </div>
        
        <div class="form-group">
          <label for="expire">Auto-Expire (Optional)</label>
          <select id="expire" v-model="expireHours">
            <option value="">Never expire</option>
            <option value="1">1 hour</option>
            <option value="6">6 hours</option>
            <option value="24">24 hours (1 day)</option>
            <option value="168">7 days</option>
            <option value="720">30 days</option>
          </select>
          <small style="color: #666; display: block; margin-top: 0.5rem;">
            The note will be automatically deleted after this time
          </small>
        </div>
        
        <div style="display: flex; gap: 1rem;">
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Creating...' : 'Create Note' }}
          </button>
          <button type="button" @click="clearForm" class="btn btn-secondary">
            Clear
          </button>
        </div>
      </form>
      
      <div v-if="successMessage" style="margin-top: 2rem;">
        <button @click="createAnother" class="btn btn-primary">
          Create Another Note
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CreateNote',
  data() {
    return {
      noteContent: '',
      password: '',
      expireHours: '',
      loading: false,
      successMessage: '',
      errorMessage: '',
      shareLink: ''
    }
  },
  methods: {
    async createNote() {
      this.loading = true
      this.errorMessage = ''
      this.successMessage = ''
      
      try {
        const response = await axios.post('/api/notes', {
          content: this.noteContent,
          password: this.password || undefined,
          expire_hours: this.expireHours || undefined
        })
        
        const noteId = response.data.id
        this.shareLink = `${window.location.origin}/note/${noteId}`
        
        let expiryInfo = ''
        if (response.data.expires_at) {
          const expiryDate = new Date(response.data.expires_at)
          expiryInfo = ` It will expire on ${expiryDate.toLocaleString()}.`
        }
        
        this.successMessage = `Note created successfully!${expiryInfo}`
        
      } catch (error) {
        this.errorMessage = error.response?.data?.error || 'Failed to create note. Please try again.'
      } finally {
        this.loading = false
      }
    },
    
    copyShareLink() {
      const input = this.$refs.shareLinkInput
      input.select()
      
      // Use modern Clipboard API with fallback
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(this.shareLink)
          .then(() => alert('Link copied to clipboard!'))
          .catch(() => {
            // Fallback for older browsers
            document.execCommand('copy')
            alert('Link copied to clipboard!')
          })
      } else {
        // Fallback for browsers without Clipboard API
        document.execCommand('copy')
        alert('Link copied to clipboard!')
      }
    },
    
    clearForm() {
      this.noteContent = ''
      this.password = ''
      this.expireHours = ''
    },
    
    createAnother() {
      this.noteContent = ''
      this.password = ''
      this.expireHours = ''
      this.successMessage = ''
      this.shareLink = ''
    }
  }
}
</script>

<style scoped>
h2 {
  margin-bottom: 1.5rem;
  color: #333;
}

.share-link {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.share-link input {
  flex: 1;
  font-family: monospace;
  font-size: 0.9rem;
}

.share-link button {
  flex-shrink: 0;
}

small {
  font-size: 0.875rem;
}
</style>
