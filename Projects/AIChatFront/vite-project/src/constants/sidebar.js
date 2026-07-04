import {
  LayoutDashboard,
  MessageSquare,
  Database,
  Users,
  Settings2,
  BarChart3,
  ClipboardList,
  User,
  Bot,
} from "lucide-react";

export const adminSidebar = [
  {
    title: "Dashboard",
    icon: LayoutDashboard,
    path: "/admin/dashboard",
  },
  {
    title: "Company Chat",
    icon: MessageSquare,
    path: "/admin/company-chat",
  },
  {
    title: "Knowledge Base",
    icon: Database,
    path: "/admin/knowledge-base",
  },
  {
    title: "User Management",
    icon: Users,
    path: "/admin/user-management",
  },
  {
    title: "Prompt Management",
    icon: Settings2,
    path: "/admin/prompt-management",
  },
  {
    title: "Analytics",
    icon: BarChart3,
    path: "/admin/analytics",
  },
  {
    title: "Audit Logs",
    icon: ClipboardList,
    path: "/admin/audit-logs",
  },
];

export const employeeSidebar = [
  {
    title: "Company Chat",
    icon: MessageSquare,
    path: "/employee/company-chat",
  },
  {
    title: "Personal Chat",
    icon: MessageSquare,
    path: "/employee/personal-chat",
  },
  {
    title: "AI Settings",
    icon: Bot,
    path: "/employee/ai-settings",
  },
  {
    title: "Profile",
    icon: User,
    path: "/employee/profile",
  },
];