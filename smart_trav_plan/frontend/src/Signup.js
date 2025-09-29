import { useState } from "react";
import { supabase } from "./supabaseClient"; // ✅ make sure you have supabaseClient.js

export default function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(""); // ✅ added success state

  // Check if email format is correct
  const validateEmail = (email) =>
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!email || !password || !confirmPassword) {
      return setError("All fields are required.");
    }
    if (!validateEmail(email)) {
      return setError("Please enter a valid email address.");
    }
    if (password !== confirmPassword) {
      return setError("Passwords do not match.");
    }

    setError("");
    setSuccess("");

    // ✅ Call Supabase
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
    });

    if (error) {
      console.error("Supabase Error:", error);
      setError(error.message);
    } else {
      console.log("Supabase Data:", data);
      setSuccess("Signup successful! 🎉 Check your Supabase Auth tab.");
    }
  };

  return (
    <div style={{ maxWidth: "300px", margin: "auto" }}>
      <h2>Sign Up</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {success && <p style={{ color: "green" }}>{success}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        /><br /><br />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        /><br /><br />
        <input
          type="password"
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        /><br /><br />
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}
