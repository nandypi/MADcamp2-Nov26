
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Authentication
const token = ref(localStorage.getItem('access_token'))
const role = ref(localStorage.getItem('user_role'))

// API
const API_URL = 'http://localhost:5000'

// State
const items = ref([])
const loading = ref(false)
const error = ref('')
const success = ref('')

// Form state
const showForm = ref(false)
const editingItem = ref(null)

const form = ref({
  name: '',
  url: ''
})

// Selected item
const selectedItem = ref(null)

// Role-based permissions
const isAdmin = computed(() => role.value === 'admin')
const isUser = computed(() => role.value === 'user')

// Authentication headers
const headers = computed(() => ({
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${token.value}`
}))

// Fetch all items
const fetchItems = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await fetch(`${API_URL}/items`, {
      method: 'GET',
      headers: headers.value
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || 'Failed to fetch items')
    }

    items.value = data

  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

// View individual item
const viewItem = async (id) => {
  error.value = ''
  success.value = ''

  try {
    const response = await fetch(`${API_URL}/items/${id}`, {
      headers: headers.value
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || 'Failed to fetch item')
    }

    selectedItem.value = data

  } catch (err) {
    error.value = err.message
  }
}

// Open create form
const openCreateForm = () => {
  if (!isAdmin.value) return

  editingItem.value = null

  form.value = {
    name: '',
    url: ''
  }

  showForm.value = true
}

// Open update form
const openEditForm = (item) => {
  if (!isAdmin.value) return

  editingItem.value = item.id

  form.value = {
    name: item.name,
    url: item.url
  }

  showForm.value = true
}

// Create or update item
const saveItem = async () => {
  if (!isAdmin.value) return

  error.value = ''
  success.value = ''

  const isEditing = editingItem.value !== null

  const endpoint = isEditing
    ? `${API_URL}/items/${editingItem.value}`
    : `${API_URL}/items`

  const method = isEditing ? 'PUT' : 'POST'

  try {
    const response = await fetch(endpoint, {
      method,
      headers: headers.value,
      body: JSON.stringify(form.value)
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || 'Operation failed')
    }

    success.value = data.message

    showForm.value = false
    editingItem.value = null

    await fetchItems()

  } catch (err) {
    error.value = err.message
  }
}

// Delete item
const deleteItem = async (id) => {
  if (!isAdmin.value) return

  const confirmed = window.confirm(
    'Are you sure you want to delete this item?'
  )

  if (!confirmed) return

  error.value = ''
  success.value = ''

  try {
    const response = await fetch(`${API_URL}/items/${id}`, {
      method: 'DELETE',
      headers: headers.value
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || 'Failed to delete item')
    }

    success.value = data.message

    if (selectedItem.value?.id === id) {
      selectedItem.value = null
    }

    await fetchItems()

  } catch (err) {
    error.value = err.message
  }
}

// Close form
const closeForm = () => {
  showForm.value = false
  editingItem.value = null
}

// Logout
const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user_role')

  router.push('/login')
}

// Initialize dashboard
onMounted(() => {
  if (!token.value || !['user', 'admin'].includes(role.value)) {
    logout()
    return
  }

  fetchItems()
})
</script>

<template>
  <div class="dashboard">

    <!-- Header -->
    <header class="header">
      <div>
        <h1>Items Dashboard</h1>
        <p>Manage and view your items</p>
      </div>

      <div class="user-info">
        <span class="role" :class="role">
          {{ role?.toUpperCase() }}
        </span>

        <button class="logout-btn" @click="logout">
          Logout
        </button>
      </div>
    </header>

    <!-- Dashboard Summary -->
    <section class="summary">
      <div class="summary-card">
        <h3>Total Items</h3>
        <p>{{ items.length }}</p>
      </div>

      <div class="summary-card">
        <h3>Your Role</h3>
        <p>{{ role }}</p>
      </div>

      <div class="summary-card">
        <h3>Permissions</h3>
        <p>{{ isAdmin ? 'Full Access' : 'Read Only' }}</p>
      </div>
    </section>

    <!-- Notifications -->
    <div v-if="error" class="alert error">
      {{ error }}
    </div>

    <div v-if="success" class="alert success">
      {{ success }}
    </div>

    <!-- Items Section -->
    <section class="items-section">

      <div class="section-header">
        <div>
          <h2>Items</h2>
          <p>Available items in the database</p>
        </div>

        <button
          v-if="isAdmin"
          class="primary-btn"
          @click="openCreateForm"
        >
          + Create Item
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="empty">
        Loading items...
      </div>

      <!-- Items Table -->
      <div v-else-if="items.length" class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>URL</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="item in items" :key="item.id">
              <td>{{ item.id }}</td>

              <td>{{ item.name }}</td>

              <td>
                <a
                  :href="item.url"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {{ item.url }}
                </a>
              </td>

              <td class="actions">

                <button
                  class="view-btn"
                  @click="viewItem(item.id)"
                >
                  View
                </button>

                <template v-if="isAdmin">
                  <button
                    class="edit-btn"
                    @click="openEditForm(item)"
                  >
                    Edit
                  </button>

                  <button
                    class="delete-btn"
                    @click="deleteItem(item.id)"
                  >
                    Delete
                  </button>
                </template>

              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="empty">
        No items found.
      </div>

    </section>

    <!-- Create / Update Form -->
    <section v-if="showForm" class="form-section">

      <h2>
        {{ editingItem !== null ? 'Update Item' : 'Create Item' }}
      </h2>

      <form @submit.prevent="saveItem">

        <div class="form-group">
          <label for="name">Item Name</label>

          <input
            id="name"
            v-model.trim="form.name"
            type="text"
            placeholder="Enter item name"
            required
          />
        </div>

        <div class="form-group">
          <label for="url">Item URL</label>

          <input
            id="url"
            v-model.trim="form.url"
            type="url"
            placeholder="https://example.com"
            required
          />
        </div>

        <div class="form-actions">
          <button type="submit" class="primary-btn">
            {{ editingItem !== null ? 'Update' : 'Create' }}
          </button>

          <button
            type="button"
            class="cancel-btn"
            @click="closeForm"
          >
            Cancel
          </button>
        </div>

      </form>
    </section>

    <!-- Individual Item Details -->
    <section v-if="selectedItem" class="details-section">

      <div class="section-header">
        <h2>Item Details</h2>

        <button
          class="cancel-btn"
          @click="selectedItem = null"
        >
          Close
        </button>
      </div>

      <p><strong>ID:</strong> {{ selectedItem.id }}</p>
      <p><strong>Name:</strong> {{ selectedItem.name }}</p>
      <p><strong>URL:</strong> {{ selectedItem.url }}</p>

    </section>

  </div>
</template>

<style scoped>
* {
  box-sizing: border-box;
}

.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px;
  font-family: Arial, sans-serif;
  color: #1f2937;
}

.header,
.section-header,
.user-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 15px;
}

.header {
  margin-bottom: 30px;
}

.header h1 {
  margin-bottom: 5px;
}

.header p,
.section-header p {
  color: #6b7280;
  margin-top: 5px;
}

.role {
  padding: 7px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
}

.role.admin {
  background: #ede9fe;
  color: #6d28d9;
}

.role.user {
  background: #dbeafe;
  color: #1d4ed8;
}

button {
  padding: 9px 14px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.logout-btn,
.cancel-btn {
  background: #e5e7eb;
  color: #374151;
}

.summary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 35px;
}

.summary-card {
  padding: 22px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  background: #fff;
}

.summary-card h3 {
  color: #6b7280;
  font-size: 14px;
}

.summary-card p {
  font-size: 25px;
  font-weight: bold;
  text-transform: capitalize;
}

.items-section,
.form-section,
.details-section {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 22px;
  margin-bottom: 25px;
}

.primary-btn {
  background: #2563eb;
  color: white;
}

.view-btn {
  background: #dbeafe;
  color: #1d4ed8;
}

.edit-btn {
  background: #fef3c7;
  color: #92400e;
}

.delete-btn {
  background: #fee2e2;
  color: #b91c1c;
}

.table-wrapper {
  overflow-x: auto;
  margin-top: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

th,
td {
  padding: 14px;
  border-bottom: 1px solid #e5e7eb;
}

th {
  background: #f9fafb;
}

td a {
  color: #2563eb;
  overflow-wrap: anywhere;
}

.actions {
  display: flex;
  gap: 7px;
  flex-wrap: wrap;
}

.form-section {
  max-width: 600px;
}

.form-group {
  margin-bottom: 18px;
}

.form-group label {
  display: block;
  margin-bottom: 7px;
  font-weight: 600;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
}

.form-actions {
  display: flex;
  gap: 10px;
}

.alert {
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 15px;
}

.error {
  background: #fee2e2;
  color: #991b1b;
}

.success {
  background: #dcfce7;
  color: #166534;
}

.empty {
  padding: 30px;
  text-align: center;
  color: #6b7280;
}

@media (max-width: 700px) {
  .dashboard {
    padding: 15px;
  }

  .summary {
    grid-template-columns: 1fr;
  }

  .header {
    align-items: flex-start;
  }

  .section-header {
    align-items: flex-start;
  }
}
</style>
