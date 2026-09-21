"use strict";

const form = document.getElementById("registration-form");
const button = document.getElementById("register-button");
const status = document.getElementById("registration-status");

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const email = document.getElementById("email").value.trim();
    const confirmEmail = document.getElementById("confirmEmail").value.trim();
    if (!form.reportValidity()) return;
    if (email.toLowerCase() !== confirmEmail.toLowerCase()) {
        status.dataset.kind = "error";
        status.textContent = "Confirm Email must match your email address.";
        document.getElementById("confirmEmail").focus();
        return;
    }

    button.disabled = true;
    status.textContent = "Creating your account...";
    status.dataset.kind = "pending";

    const payload = {
        firstName: document.getElementById("firstName").value.trim(),
        lastName: document.getElementById("lastName").value.trim(),
        age: Number(document.getElementById("age").value),
        email,
        confirmEmail
    };

    try {
        const response = await fetch("/api/registrations", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const result = await response.json();
        if (!response.ok) {
            const messages = result.errors ? Object.values(result.errors).flat().join(" ") : null;
            throw new Error(messages || result.message || "Registration failed. Please try again.");
        }
        status.dataset.kind = "success";
        status.textContent = result.message + " Your customer ID is " + result.customerId + ".";
        form.reset();
    } catch (error) {
        status.dataset.kind = "error";
        status.textContent = error.message || "Could not connect. Please try again.";
    } finally {
        button.disabled = false;
    }
});
