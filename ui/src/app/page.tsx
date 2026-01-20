import { StatsCard } from "@/components/dashboard/StatsCard";
import { RequestsChart } from "@/components/dashboard/RequestsChart";
import { Activity, Server, Zap, Clock } from "lucide-react";

export default function Home() {
  return (
    <div className="p-8 space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-gray-100">Dashboard</h1>
        <p className="text-muted-foreground text-gray-500 dark:text-gray-400 mt-2">
          Overview of Nexus AI Platform performance
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatsCard
          title="Total Requests"
          value="1,284,332"
          change="+12.5% from last month"
          trend="up"
          icon={Activity}
        />
        <StatsCard
          title="Active Models"
          value="4"
          change="All systems healthy"
          trend="neutral"
          icon={Server}
        />
        <StatsCard
          title="Avg Latency"
          value="124ms"
          change="-18ms improvement"
          trend="up"
          icon={Zap}
        />
        <StatsCard
          title="Uptime"
          value="99.99%"
          change="Last 30 days"
          trend="neutral"
          icon={Clock}
        />
      </div>

      <div className="grid gap-4 md:grid-cols-7">
        <div className="col-span-4">
          <RequestsChart />
        </div>
        <div className="col-span-3 rounded-xl border bg-card p-6 shadow-sm bg-white dark:bg-zinc-900 border-gray-200 dark:border-zinc-800">
          <div className="mb-4">
            <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100">
              Active Models
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Current loaded inference engines
            </p>
          </div>
          <div className="space-y-4">
            {[
              { name: "Llama 3 8B", status: "Running", load: "78%" },
              { name: "Mistral 7B", status: "Running", load: "45%" },
              { name: "GPT-4 Proxy", status: "Idle", load: "0%" },
              { name: "Claude 3.5 Sonnet Proxy", status: "Running", load: "12%" },
            ].map((model) => (
              <div key={model.name} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-green-500" />
                  <span className="font-medium text-sm text-gray-700 dark:text-gray-300">{model.name}</span>
                </div>
                <div className="text-sm text-gray-500 dark:text-gray-400">
                  {model.load} load
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
