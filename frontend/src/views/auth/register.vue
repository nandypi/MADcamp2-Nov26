<script>
import { RouterLink } from 'vue-router'

export default {
    name: 'RegisterView',
    data() {
        return {
            name: '',
            email: '',
            password: ''
        }
    },
    components: {
        RouterLink
    },
    methods: {
        async registerUser() {
            // Implement registration logic here
            const resp = await fetch('http://localhost:5000/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: this.name,
                    email: this.email,
                    password: this.password
                })
            })
            const data = await resp.json()
            console.log(data)
        }
    }
}

</script>

<template>
    <div>
        <h1>Register</h1>
        <p>Create a new account</p>
        <pre>{{ name }}</pre>
        <pre>{{ email }}</pre>
        <pre>{{ password }}</pre>
        <form @submit.prevent="registerUser">
            <div>
                <label for="name">Username:</label>
                <input v-model="name" type="text" id="name" name="name" required>
            </div>
            <div>
                <label for="email">Email:</label>
                <input v-model="email" type="email" id="email" name="email" required>
            </div>
            <div>
                <label for="password">Password:</label>
                <input v-model="password" type="password" id="password" name="password" required>
            </div>
            <button type="submit">Register</button>
        </form>
    </div>
    <RouterLink to="/login">Have an account? Login</RouterLink>
    <br>
    <RouterLink to="/">Go to Home</RouterLink>
</template>