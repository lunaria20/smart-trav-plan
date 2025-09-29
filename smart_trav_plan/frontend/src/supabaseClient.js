import { createClient } from "@supabase/supabase-js";

// replace with your project values
const supabaseUrl = "https://eofmoyekhoqxzgzmlvcc.supabase.co";
const supabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVvZm1veWVraG9xeHpnem1sdmNjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkxNTcxNjYsImV4cCI6MjA3NDczMzE2Nn0.xb1U1axIBd3_HcAWkOPedoZHiA9XGb5wte8JjZaS31A";

export const supabase = createClient(supabaseUrl, supabaseKey);
