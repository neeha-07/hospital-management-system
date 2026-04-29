import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./components/Login.js";
import PatientRegister from "./components/PatientRegister.js";
import DoctorRegister from "./components/DoctorRegister.js";
import ForgotPassword from "./components/ForgotPassword.js";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/patient-register" element={<PatientRegister />} />
        <Route path="/doctor-register" element={<DoctorRegister />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
      </Routes>
    </BrowserRouter>
  );
}