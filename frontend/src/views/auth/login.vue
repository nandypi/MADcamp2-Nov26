<script>
import { RouterLink } from 'vue-router'

export default {
    name: 'LoginView',
    data() {
        return {
            email: 'user@gmail.com',
            password: 'password'
        }
    },
    components: {
        RouterLink
    },
    methods: {
        async loginUser() {
            // Implement login logic here
            const resp = await fetch('http://localhost:5000/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: this.email,
                    password: this.password
                })
            })
            const data = await resp.json()
            console.log(resp)
            if (resp.ok) {
                // Handle successful login, e.g., store token, redirect, etc.
                console.log('Login successful:', data)
                localStorage.setItem('access_token', data.access_token)
                localStorage.setItem('user_role', data.role)
            } else {
                // Handle login error
                console.error('Login failed:', data)
            }
        }
    }
}

</script>

<template>
    <div>
        <h1>Login</h1>
        <p>Login to your account</p>
        <pre>{{ email }}</pre>
        <pre>{{ password }}</pre>
        <form @submit.prevent="loginUser">
            <div>
                <label for="email">Email:</label>
                <input v-model="email" type="email" id="email" name="email" required>
            </div>
            <div>
                <label for="password">Password:</label>
                <input v-model="password" type="password" id="password" name="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
    </div>
    <RouterLink to="/register">Don't have an account? Register</RouterLink>
    <br>
    <RouterLink to="/">Go to Home</RouterLink>
</template>