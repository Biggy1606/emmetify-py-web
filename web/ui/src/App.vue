<template>
  <div id="app">
    <h1>Emmetify</h1>
    <div class="container">
      <div class="panel">
        <h2>HTML to Emmet</h2>
        <div class="input-group">
          <label for="url">URL</label>
          <input type="text" id="url" v-model="urlInput" placeholder="Enter URL and press Enter" @keyup.enter="convertUrlToEmmet">
        </div>
        <div class="input-group">
          <label for="html-input">HTML</label>
          <textarea id="html-input" v-model="htmlInput" placeholder="Paste HTML here and click Convert"></textarea>
          <button @click="convertHtmlToEmmet" :disabled="isLoading">
            {{ isLoading ? 'Converting...' : 'Convert to Emmet' }}
          </button>
        </div>
        <div class="input-group" v-if="emmetOutput">
            <label for="emmet-output">Emmet Output</label>
            <div class="output-wrapper">
              <textarea id="emmet-output" :value="emmetOutput.result" readonly></textarea>
              <button @click="copyToClipboard(emmetOutput.result, 'emmet')" class="copy-btn">
                {{ copyButtonText.emmet }}
              </button>
            </div>
        </div>
        <div class="options">
          <input type="checkbox" id="compact-checkbox" v-model="useCompact">
          <label for="compact-checkbox">Use Compact Conversion</label>
        </div>
      </div>
      <div class="panel">
        <h2>Emmet to HTML</h2>
        <div class="input-group">
          <label for="emmet-input">Emmet</label>
          <textarea id="emmet-input" v-model="emmetInput" placeholder="Enter Emmet here and click Convert"></textarea>
          <button @click="convertEmmetToHtml">Convert to HTML</button>
        </div>
        <div class="input-group" v-if="htmlOutput">
            <label for="html-output">HTML Output</label>
            <div class="output-wrapper">
              <textarea id="html-output" :value="htmlOutput" readonly></textarea>
              <button @click="copyToClipboard(htmlOutput, 'html')" class="copy-btn">
                {{ copyButtonText.html }}
              </button>
            </div>
        </div>
      </div>
    </div>
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';

const urlInput = ref('');
const htmlInput = ref('');
const emmetOutput = ref('');
const emmetInput = ref('');
const htmlOutput = ref('');
const isLoading = ref(false);
const error = ref(null);
const useCompact = ref(true);

const copyButtonText = ref({
  emmet: 'Copy',
  html: 'Copy'
});

const copyToClipboard = async (text, type) => {
  try {
    await navigator.clipboard.writeText(text);
    copyButtonText.value[type] = 'Copied!';
    setTimeout(() => {
      copyButtonText.value[type] = 'Copy';
    }, 2000);
  } catch (err) {
    console.error('Failed to copy: ', err);
    error.value = 'Failed to copy to clipboard.';
  }
};

const convertUrlToEmmet = async () => {
  error.value = '';
  emmetOutput.value = '';
  isLoading.value = true;
  try {
    const response = await axios.post('http://localhost:8000/api/v1/url', {
      url: urlInput.value,
      compact: useCompact.value
    });
    emmetOutput.value = response.data.emmet;
  } catch (err) {
    error.value = err.response ? err.response.data.detail : err.message;
  } finally {
    isLoading.value = false;
  }
};

const convertHtmlToEmmet = async () => {
  error.value = '';
  emmetOutput.value = '';
  isLoading.value = true;
  try {
    const response = await axios.post('http://localhost:8000/api/v1/html', {
      html: htmlInput.value,
      compact: useCompact.value
    });
    emmetOutput.value = response.data.emmet;
  } catch (err) {
    error.value = err.response ? err.response.data.detail : err.message;
  } finally {
    isLoading.value = false;
  }
};

const convertEmmetToHtml = async () => {
  error.value = '';
  htmlOutput.value = '';
  isLoading.value = true;
  try {
    const response = await axios.post('http://localhost:8000/api/v1/emmet', { emmet: emmetInput.value });
    htmlOutput.value = response.data.html;
  } catch (err) {
    error.value = err.response ? err.response.data.detail : err.message;
  } finally {
    isLoading.value = false;
  }
};
</script>

<style>
/* General Body Styles */
body {
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background-color: #f8f9fa;
  color: #343a40;
}

/* App Container */
#app {
  max-width: 1600px;
  margin: 0 auto;
  
}

/* Main Title */
h1 {
  text-align: center;
  font-size: 3rem;
  font-weight: 700;
  color: #212529;
  margin-bottom: 3rem;
}

/* Layout Container */
.container {
  display: flex;
  gap: 2rem;
  align-items: stretch;
}

/* Panel Styles */
.panel {
  flex: 1;
  background-color: #ffffff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
}

.panel h2 {
  text-align: center;
  font-size: 1.75rem;
  font-weight: 600;
  color: #495057;
  margin-top: 0;
  margin-bottom: 2rem;
}

/* Input Group Styles */
.input-group {
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.input-group label {
  margin-bottom: 0.75rem;
  font-weight: 600;
  color: #495057;
}

.input-group input[type="text"],
.input-group textarea {
  width: 100%;
  padding: 1rem;
  border: 1px solid #ced4da;
  border-radius: 8px;
  font-size: 1rem;
  box-sizing: border-box;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.input-group input[type="text"]:focus,
.input-group textarea:focus {
  outline: none;
  border-color: #80bdff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25);
}

.input-group textarea {
  flex-grow: 1;
  resize: vertical;
  min-height: 250px;
}

.output-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.copy-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 0.5rem 0.75rem;
  background: #6c757d;
  font-size: 0.8rem;
  min-height: auto;
  margin-top: 0;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.copy-btn:hover {
  background: #5a6268;
}

/* Button Styles */
button {
  padding: 1rem 1.5rem;
  border: none;
  background: linear-gradient(145deg, #007bff, #0056b3);
  color: white;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: transform 0.2s, box-shadow 0.2s;
  margin-top: auto;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 123, 255, 0.3);
}

/* Error Message Styles */
.error-message {
  margin-top: 2rem;
  padding: 1rem;
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 8px;
  text-align: center;
}

/* Options Styles */
.options {
  display: flex;
  align-items: center;
  margin-top: 10px;
}

.options input[type="checkbox"] {
  margin-right: 8px;
  width: 16px;
  height: 16px;
}

.options label {
  font-size: 0.9rem;
  color: #495057;
}

/* Responsive Design */
@media (max-width: 992px) {
  .container {
    flex-direction: column;
  }

  h1 {
    font-size: 2.5rem;
  }

  .panel h2 {
    font-size: 1.5rem;
  }
}

@media (max-width: 576px) {
  #app {
    padding: 1rem;
  }

  h1 {
    font-size: 2rem;
  }

  .panel {
    padding: 1.5rem;
  }
}
</style>
