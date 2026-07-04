import Sidebar from "../../components/layout/Sidebar";
import Header from "../../components/layout/Header";
import { adminSidebar } from "../../constants/sidebar";
import StatCard from "../../components/dashboard/StatCard";
import { FileText, MessageSquare, Timer, Users } from "lucide-react";
import ActivityChart from "../../components/dashboard/ActivityChart";
import RecentActivity from "../../components/dashboard/RecentActivity";
import RecentDocuments from "../../components/dashboard/RecentDocuments";
import SystemHealth from "../../components/dashboard/SystemHealth";

function Dashboard() {
  return (
    <div className="flex h-screen bg-[var(--bg-primary)]">
      {/* Sidebar */}
      <Sidebar menuItems={adminSidebar} />

      {/* Right Section */}
      <div className="flex flex-col flex-1">
        {/* Header */}
        <Header title="Dashboard" />

        {/* Dashboard Content */}
        <main className="flex-1 overflow-y-auto p-8">
          <div>
            <h2 className="text-4xl font-bold mb-8">Dashboard</h2>

            <div className="grid grid-cols-4 gap-6">
              <StatCard
                title="Documents"
                value="1,250"
                icon={<FileText size={28} />}
              />

              <StatCard title="Users" value="42" icon={<Users size={28} />} />

              <StatCard
                title="Chats"
                value="15,432"
                icon={<MessageSquare size={28} />}
              />

              <StatCard
                title="Avg Response"
                value="1.8s"
                icon={<Timer size={28} />}
              />

              
            </div>

            <div className="grid grid-cols-3 gap-6 mt-8">

  <div className="col-span-2">
    <ActivityChart />
  </div>

  <RecentActivity />

</div>

<div className="grid grid-cols-2 gap-6 mt-6">

  <RecentDocuments />

  <SystemHealth />

</div>

            
          </div>
        </main>
      </div>
    </div>
  );
}

export default Dashboard;
