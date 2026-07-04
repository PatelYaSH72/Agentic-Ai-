import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "../pages/auth/Login";

// Admin Pages
import Dashboard from "../pages/admin/Dashboard";
import CompanyChat from "../pages/admin/CompanyChat";
import KnowledgeBase from "../pages/admin/KnowledgeBase";
import UserManagement from "../pages/admin/UserManagement";
import PromptManagement from "../pages/admin/PromptManagement";
import Analytics from "../pages/admin/Analytics";
import AuditLogs from "../pages/admin/AuditLogs";

// Employee Pages
import EmployeeCompanyChat from "../pages/employee/CompanyChat";
import PersonalChat from "../pages/employee/PersonalChat";
import AISettings from "../pages/employee/AISettings";
import Profile from "../pages/employee/Profile";

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Auth */}
        <Route path="/" element={<Login />} />

        {/* Admin */}
        <Route path="/admin/dashboard" element={<Dashboard />} />
        <Route path="/admin/company-chat" element={<CompanyChat />} />
        <Route path="/admin/knowledge-base" element={<KnowledgeBase />} />
        <Route path="/admin/user-management" element={<UserManagement />} />
        <Route path="/admin/prompt-management" element={<PromptManagement />} />
        <Route path="/admin/analytics" element={<Analytics />} />
        <Route path="/admin/audit-logs" element={<AuditLogs />} />

        {/* Employee */}
        <Route path="/employee/company-chat" element={<EmployeeCompanyChat />} />
        <Route path="/employee/personal-chat" element={<PersonalChat />} />
        <Route path="/employee/ai-settings" element={<AISettings />} />
        <Route path="/employee/profile" element={<Profile />} />

      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;